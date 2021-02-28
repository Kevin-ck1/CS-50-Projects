from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bid, Comment, Category, Info


def index(request):
    auction_listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html",{
        "listings": auction_listings
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

def create(request):
    if request.method == "POST":
        title = request.POST['listing_title']
        description = request.POST['listing_description']
        price = request.POST['start_bid']
        photo = request.POST['listing_image']
        creator = request.user
        if request.POST['listing_category']:
            listing_category = Category.objects.get(pk=int(request.POST['listing_category']))
        else:
            listing_category = Category.objects.get(pk=1)
        
        new_listing = AuctionListing(title=title, description=description, start_price=price, current_bid=price, photo=photo, creator=creator, listing_category=listing_category)
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html",{
        "categories": Category.objects.exclude(pk=1)
    })

def listing_page(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    min_bid = listing.current_bid + 5
    
    return render(request, "auctions/listing.html",{
        "listing": listing,
        "status": listing.listing_open,
        "min_bid": min_bid, 
    })

def watchlist(request):
    if request.method == "POST":
        wList = request.POST['wList']
        watch_list = AuctionListing.objects.get(pk=wList)
        watch_list.watchBidder = request.user
        watch_list.save()
    
        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":request.POST['wList']}))
    else:
        wList_listings = request.user.listing_watchBidder.all()
        return render(request, "auctions/index.html",{
            "listings": wList_listings
        })

def bidlist(request):
    if request.method == "POST":
        bItem = request.POST['bItem']
        bid_list = AuctionListing.objects.get(pk=bItem)
        bid_list.watchBidder = request.user
        bid_list.current_bid = request.POST["bid_price"]
        bid_list.save()
        
        bid_item = Bid(bid_item=bid_list, bid_price=bid_list.current_bid, bidder=request.user)
        bid_item.save()

        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":bItem}))
    
    else:
        bid_listings = request.user.listing_bidder.all()
        return render(request, "auctions/index.html",{
            "listings": bid_listings
        })

def close_lisiting(request):
    if request.method == "POST":
        bItem = request.POST['lastBid']
        listing = AuctionListing.objects.get(pk=bItem)
        listing.listing_open = False
        listing.save()

        last_bid = Bid.objects.get(bid_item=listing, bid_price=listing.current_bid)
        winner = last_bid.bidder

        a_info = User.objects.get(username=listing.creator)
        w_info = User.objects.get(username=winner)

        closing_info = Info(won_listing=listing, author_Username=listing.creator,author_Email = a_info.email, winner_Username = last_bid.bidder,winner_Email = w_info.email)
        closing_info.save()
        #return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":bItem}))
        return render(request, "auctions/listing.html",{
            "listing": listing,
            "status": listing.listing_open,
            "winner": winner,
            "info": closing_info,
            "closed" : "Closed"
        })








        