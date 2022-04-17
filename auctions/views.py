from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *


def index(request):
    # This is checking if the user is logged in. If they are, it will display the number of items they
    # are watching. If they are not, it will not display the number of items they are watching.
    if request.user.is_authenticated:
        number = len(request.user.watching.all())
    
        # This is a query that is getting all the listings that are active.
        listing = AuctionListing.objects.filter(active=True)
        return render(request, "auctions/index.html", {
            "listings": listing,
            "number": number
        })
    else:
        # This is a query that is getting all the listings that are active.
        listing = AuctionListing.objects.filter(active=True)
        return render(request, "auctions/index.html", {
            "listings": listing
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

@login_required(login_url="login")
def create_listing(request):
    # This is checking if the user is logged in. If they are, it will display the number of items they
    # are watching. If they are not, it will not display the number of items they are watching.
    if request.user.is_authenticated:
        number = len(request.user.watching.all())

        # This is checking if the user is submitting a form. If they are, it will create a new
        # listing.
        if request.method == "POST":
            listing = CreateListing(request.POST)
            if listing.is_valid():
                title = request.POST["title"]
                description = request.POST["description"]
                image = request.POST["image"]
                starting_bid = request.POST["starting_bid"]
                category = request.POST["category"]
                seller = request.user

                NULL_BID = Bid(bid=0)
                NULL_BID.save()
                current_price = NULL_BID

                new_listing = AuctionListing(title=title, description=description, image=image, starting_bid=starting_bid, category=category, seller=seller, current_price=current_price)
                new_listing.save()

                listing = AuctionListing.objects.filter(active=True)
                return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create_listing.html", {
                "create_listing": CreateListing(),
                "number": number
            })
    else:
        # This is checking if the user is submitting a form. If they are, it will create a new
        #         listing.
        if request.method == "POST":
            listing = CreateListing(request.POST)
            if listing.is_valid():
                title = request.POST["title"]
                description = request.POST["description"]
                image = request.POST["image"]
                starting_bid = request.POST["starting_bid"]
                category = request.POST["category"]
                seller = request.user

                NULL_BID = Bid(bid=0)
                NULL_BID.save()
                current_price = NULL_BID

                new_listing = AuctionListing(title=title, description=description, image=image, starting_bid=starting_bid, category=category, seller=seller, current_price=current_price)
                new_listing.save()

                listing = AuctionListing.objects.filter(active=True)
                return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create_listing.html", {
                "create_listing": CreateListing(),
            })

def listing(request, listing_id, good_bid=1):
    # This is checking if the user is logged in. If they are, it will display the number of items they
    # are watching. If they are not, it will not display the number of items they are watching.
    if request.user.is_authenticated:
        number = len(request.user.watching.all())

        # This is getting the listing that the user is on and checking if the user is watching the
        # listing.
        listing = AuctionListing.objects.get(pk=listing_id)
        watching = request.user in listing.watchlist.all()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watching": watching,
            "good_bid": good_bid,
            "comments": listing.comment.all().order_by('?'),
            "number": number
        })
    else:
        # This is getting the listing that the user is on and checking if the user is watching the
        # listing.
        listing = AuctionListing.objects.get(pk=listing_id)
        watching = request.user in listing.watchlist.all()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watching": watching,
            "good_bid": good_bid,
            "comments": listing.comment.all().order_by('?'),
        })

def toggle_watchlist(request, listing_id):
    # This is checking if the user is submitting a form. If they are, it will either add the user to the
    # watchlist or will remove the user from the watchlist.
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        
        if request.user in listing.watchlist.all():
            listing.watchlist.remove(request.user)
        else:
            listing.watchlist.add(request.user)
    
    return HttpResponseRedirect(reverse("listing", kwargs={
        "listing_id": listing_id
    }))

def bid(request, listing_id):
    # This is checking if the user is submitting a form. If they are, it will check if the bid is
    # greater than the starting bid and the current bid. If it is, it will create a new bid and save
    # it. If it is not, it will redirect the user to the listing page and tell them that their bid is
    # not valid.
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        bid = int(request.POST["bid"])

        if bid >= listing.starting_bid and bid > int(listing.current_price.bid):
            BID = Bid(bid=bid, bidder=request.user)
            BID.save()
            listing.current_price = BID
            listing.save()
            return HttpResponseRedirect(reverse("listing", kwargs={
                "listing_id": listing_id,
                "good_bid": 2,
            }))
        else:
            return HttpResponseRedirect(reverse("listing", kwargs={
                "listing_id": listing_id,
                "good_bid": 0,
            }))

def close_auction(request, listing_id):
    # This is checking if the user is submitting a form. If they are, it will close the auction.
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", kwargs={
            "listing_id": listing_id
        }))

def comment(request, listing_id):
    # This is checking if the user is submitting a form. If they are, it will create a new comment
    # and add it to the listing.
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        comment = Comment(message=request.POST["comment"], author=request.user)
        comment.save()
        listing.comment.add(comment)
        return HttpResponseRedirect(reverse("listing", kwargs={
            "listing_id": listing_id,
        }))

def watchlist(request):
    # This is getting the user that is logged in and getting all the listings that they are watching.
    USER = request.user
    watching = USER.watching.all()
    number = len(watching)
    return render(request, "auctions/watchlist.html", {
        "watching": watching,
        "number": number
    })

def categories(request):
    # This is checking if the user is logged in. If they are, it will display the number of items they
    # are watching. If they are not, it will not display the number of items they are watching.
    if request.user.is_authenticated:
        number = len(request.user.watching.all())

        # This is getting all the categories that are active and are not empty. It is also getting rid
        # of any duplicates.
        CATEGORIES = AuctionListing.objects.values_list('category', flat=True).exclude(category='').filter(active=True).distinct().order_by('category')
        return render(request, "auctions/categories.html", {
            "categories": CATEGORIES,
            "number": number
        })
    else:
        # This is getting all the categories that are active and are not empty. It is also getting rid
        # of any duplicates.
        CATEGORIES = AuctionListing.objects.values_list('category', flat=True).exclude(category='').filter(active=True).distinct().order_by('category')
        return render(request, "auctions/categories.html", {
            "categories": CATEGORIES,
        })

def category_list(request, category):
    # This is checking if the user is logged in. If they are, it will display the number of items they
    # are watching. If they are not, it will not display the number of items they are watching.
    if request.user.is_authenticated:
        number = len(request.user.watching.all())

        # This is getting all the listings that are active and are in the category that the user is
        # looking at. It is then rendering the category_list.html page and passing in the
        # listings, category, and number of items the user is watching.
        listing = AuctionListing.objects.filter(category=category, active=True)
        return render(request, "auctions/category_list.html", {
            "listing": listing,
            "category": category,
            "number": number
        })
    else:
        # The code is filtering the AuctionListing objects by category and active.
        listing = AuctionListing.objects.filter(category=category, active=True)
        return render(request, "auctions/category_list.html", {
            "listing": listing,
            "category": category,
        })

