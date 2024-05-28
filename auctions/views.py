from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  get_object_or_404, render
from django.urls import reverse
from django.contrib import messages

from .forms import ListingForms, BidForm, CommentForm


from .models import User, AuctionListing, Bid, Comment, Watchlist, Category


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all().filter(is_active=True)      
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
    if request.method == "POST":
        form = ListingForms(request.POST)
        
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.created_by = request.user
            new_listing.save()
            
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForms()
    
    return render(request, "auctions/create_listing.html", {
        "form": form
    })
      
      
def listing_details(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing)
    max_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
    is_watching = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    
    bid_form = BidForm()
    comment_form = CommentForm()
    
    bid_url = reverse("place-bid", kwargs={'listing_id': listing.id,})
    comment_url = reverse("add-comment", kwargs={'listing_id': listing.id,})
    watchlist_url = reverse("watchlist")
    
    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "comments": comments,
        "highest_bid": max_bid,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "bid_url": bid_url,
        "comment_url": comment_url,
        "watchlist_url": watchlist_url,
        "is_watching": is_watching,
    })
    
def place_bid(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    form = BidForm(request.POST)
    
    if form.is_valid():
        bid_amount = form.cleaned_data['amount']
        startin_bid = listing.starting_bid
        current_highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
        if bid_amount > startin_bid and (current_highest_bid is None or bid_amount > current_highest_bid.amount):
            Watchlist.objects.get_or_create(user=request.user, listing=listing)
            new_bid = form.save(commit=False)
            new_bid.listing = listing
            new_bid.user = request.user
            new_bid.save()
            messages.success(request, "Your bid has been placed successfully.")
   
    messages.error(request, "Your bid must be higher than the starting bid and lower than the current highest bid.")
    return HttpResponseRedirect(reverse("listing-details", args=(listing.id, )))
    
    
def add_comment(request, listing_id): 
    listing = AuctionListing.objects.get(pk=listing_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        new_comment = form.cleaned_data['comment']
        comment = Comment(listing=listing, user=request.user, content=new_comment)
        comment.save()
        
        return HttpResponseRedirect(reverse("listing-details", args=(listing.id, )))
    
    
def categories_view(request):
    categories = Category.objects.all().filter
    return render(request, "auctions/categories.html",{
        "categories_list": categories
    })
    
    
def categorized_listings(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = AuctionListing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/categorized_listings.html", {
        "listings": listings,
        "picked_category": category
    })    
    
    
def watchlist_view(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')  
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)
        
        if created:
            watchlist.save()
        else:
            watchlist.delete()
        
        return HttpResponseRedirect(reverse("listing-details", args=(listing.id,)))
    
    watchlist = Watchlist.objects.filter(user=request.user)
    listings = [watch.listing for watch in watchlist]
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": listings
    })


def close_listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    if request.user == listing.created_by:
        highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
        if highest_bid:
            listing.winner = highest_bid.user
        listing.is_active = False
        listing.save()
    
    return HttpResponseRedirect(reverse("index"))