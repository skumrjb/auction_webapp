from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing>", views.listing, name="listing"),
    path("bid/<str:listing>", views.bidding, name="bid"),
    path("watchlist", views.user_watchlist, name="user_watchlist"),
    path("add_watchlist/<str:listing>", views.add_to_watchlist, name="add_watchlist"),
    path("add_comment/<str:listing>", views.add_comments, name="add_comment"),
    path("close_listing/<str:listing>", views.close_listing, name="close_listing"),
    path("category", views.category_view, name="category"),
    path("category/<str:category>", views.category_listing, name="category_listing"),
    path("user_listings/<str:listing>", views.user_listings, name="user_listings"),
    path("my_listings", views.my_listings, name="your_listings"),
    path("closed_auction", views.closed_auction, name="closed_auction")
]
