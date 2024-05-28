from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing-details/<int:listing_id>", views.listing_details, name="listing-details"),
    path("listing-details/<int:listing_id>/bid", views.place_bid, name="place-bid"),
    path("listing-details/<int:listing_id>/comment", views.add_comment, name="add-comment"),
    path("categories", views.categories_view, name="categories"),
    path("categories/<int:category_id>", views.categorized_listings, name="categorized-listings"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("close-listing/<int:listing_id>", views.close_listing, name="close-listing"),
]
