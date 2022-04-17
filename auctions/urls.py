from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category-list/<str:category>", views.category_list, name="category_list"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/<int:good_bid>", views.listing, name="listing"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("toggle_watchlist/<int:listing_id>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("close-auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
]
