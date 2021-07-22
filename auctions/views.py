from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ListingForm, BidForm, CommentForm
from django.core.exceptions import ValidationError
from django.db.models import Count, Q

from .models import User, AuctionListing, Bid, Comment, WatchList


def index(request):
    user = request.user
    if user.id is None:
        return redirect('login')

    auction_listing = AuctionListing.objects.filter(closed=False).order_by('-created_on')
    return render(request, "auctions/index.html",{
        'active_listings': auction_listing,
         })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    # Fetch user details, if not let user login
    user = request.user
    if user.id is None:
        return redirect('login')

    # Aggregate the watchlist Items
    # watchlist = WatchList.objects.get(user=request.user)
    # watchlist_bid_count = watchlist.listing.count()

    if request.method == 'GET':
        context = {
            'form': ListingForm(),
            # 'total_watchlist' : watchlist_bid_count
        }
        return render(request, 'auctions/create_listing.html', context)

    else:
        form = ListingForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            img = form.cleaned_data['img']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            category = form.cleaned_data['category']

            # Saving data into the model-form
            listing_created = AuctionListing.objects.create(
                user= request.user,
                category=category,
                title=title,
                img=img,
                starting_bid=starting_bid,
                description=description
            )

            return redirect('index')

def listing(request, listing):
    user = request.user
    if user.id is None:
        return redirect('login')
    
    # instantiate watchlist
    # watchlist count

    listing = AuctionListing.objects.get(id=listing)

    data = {
        'listing' : listing
    }
    return render(request, 'auctions/listing.html', data)

def bidding(request, listing):

    bidding_for_listing = AuctionListing.objects.get(id=listing)
    
    if request.method == 'POST':
        form = BidForm(request.POST)

        if form.is_valid():
            bid_price = form.cleaned_data['bid_price']
        
            if not bidding_for_listing.last_bid :
                if bid_price < bidding_for_listing.starting_bid:
                    raise ValidationError('Bid value is less than starting bid ')
            else:
                if bid_price < bidding_for_listing.last_bid.bid_price :
                    raise ValidationError('Bid value is less than last bid')

            bid_created = Bid.objects.create(
                user= request.user,
                listing= bidding_for_listing,
                bid_price= bid_price
            )

            bidding_for_listing.bids.add(bid_created)
            bidding_for_listing.last_bid = bid_created
            bidding_for_listing.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def user_watchlist(request):
    # Fetch user details, if not user should login
    user = request.user
    if user.id is None:
        return redirect('login')

    try:
        watchlist = WatchList.objects.get(user=user)
        
        return render(request, "auctions/watchlist.html", {
        'watchlist': watchlist,
        'listing': listing
        })
    except:
        watchlist = None
        create_watchlist_user = WatchList.objects.create(
            user= user
        )
        create_watchlist_user.save()
        return render(request, "auctions/watchlist.html", {
        'watchlist': watchlist
        })

def add_to_watchlist(request, listing):

    if request.method == 'POST':
        # Retrieve the listing id from page and the user's watchlist
        listing_to_add = AuctionListing.objects.get(id=listing)
        user_watchlist = WatchList.objects.get(user=request.user)

        # If listing is already present in the list, remove it
        if listing_to_add in user_watchlist.listing.all():
            user_watchlist.listing.remove(listing_to_add)
            user_watchlist.save()
        # If listing is not present in the watchlist , add it
        else:
            user_watchlist.listing.add(listing_to_add)
            user_watchlist.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_comments(request, listing):
    # Fetch user details, if not user should login
    user = request.user
    if user.id is None:
        return redirect('login')

    listing_comment = AuctionListing.objects.get(id=listing)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.cleaned_data['comment']

            user_comment_created = Comment.objects.create(
                user=user,
                comment= comment
            )

            listing_comment.comments.add(user_comment_created)
            listing_comment.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def close_listing(request, listing):

    user = request.user
    if user.id is None:
        return redirect('login')

    listing_to_close = AuctionListing.objects.get(id=listing)

    if user == listing_to_close.user :
        if request.method == 'POST':
            listing_to_close.closed = True
            listing_to_close.save()
        
        data = {
            'user': user
        }

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), data)

    else:
        data = {
            'user' : user,
            'message' : 'Sorry, you are not authorised to close the bid'
        }
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), data)

    
def category_view(request):
    user = request.user
    if user.id is None:
        return redirect('login')
    category_listing = AuctionListing.objects.values('category')
    # Create a set of unique values from the category_listing dict
    category = set( val for dic in category_listing for val in dic.values())
    return render(request, "auctions/category.html", {
        'category': category
    })

def category_listing(request, category):
    user = request.user
    if user.id is None:
        return redirect('login')

    listings = AuctionListing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        'listings': listings,
        'cat':category,
    })

def my_listings(request):
    user = request.user
    if user.id is None:
        return redirect('login')

    listings = AuctionListing.objects.filter(user=user)
    return render(request, "auctions/user_listings.html", {
        'listings': listings,
        'user': user
    })

def user_listings(request, listing):
    user = request.user
    if user.id is None:
        return redirect('login')

    listings = AuctionListing.objects.get(id=listing)
    
    if listings.user != user:
        listing_filter = AuctionListing.objects.filter(user=listings.user)
        return render(request, "auctions/user_listings.html", {
            'listings': listing_filter,
            'listings_creator': listings.user,
            'visitor_user': user
        })
    
    else:
        return my_listings(request)

def closed_auction(request):
    closed_listing = AuctionListing.objects.filter(closed=True)
    return render(request, "auctions/index.html", {
        'closed_listings': closed_listing
    })

def search(request):
    if request.method == "POST":
        query = request.POST.get('q')
        search = AuctionListing.objects.filter(Q(title__icontains=query))
        return render(request, "auctions/search.html", {
        'search': search,
        'query' : query
        })
    else:
        return redirect('index')
