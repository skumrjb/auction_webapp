from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing>", views.listing, name="listing"),
    path("bid/<str:listing>", views.bidding, name="bid"),
    path("watchlist", views.user_watchlist, name="user_watchlist"),
    path("add_watchlist/<str:listing>", views.add_to_watchlist, name="add_watchlist"),
    path("add_comment/<str:listing>", views.add_comments, name="add_comment"),
    
]
