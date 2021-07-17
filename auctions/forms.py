from django import forms
  
from .models import AuctionListing, Bid, Comment
  
# create a ModelForm
class ListingForm(forms.ModelForm):
    # specifying the name of model to use
    class Meta:
        model = AuctionListing
        # fields I have selected from the AuctionListing model
        fields = ['title', 'img', 'description', 'starting_bid', 'category']
        # aesthetic
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'description' : forms.TextInput(attrs={'class': 'form-control'}),
            'starting_bid' : forms.NumberInput(attrs={'class': 'form-control'}),
            'category' : forms.TextInput(attrs={'class': 'form-control'})
        }

class BidForm(forms.ModelForm):
    
    class Meta:
        model = Bid
        fields = ['bid_price']
        widgets = {
            'bid_price' : forms.NumberInput(attrs={'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment' : forms.TextInput(attrs={'class': 'form-control'})
        }

class CloseListingForm(forms.ModelForm):

    class Meta:
        model = AuctionListing
        fields = ['closed']
        widgets = {
            'closed' : forms.BooleanField()
        }