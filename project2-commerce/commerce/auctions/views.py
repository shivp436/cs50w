from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import NewListingForm
from .models import ListingModel, User, category_choices


def index(request):
    return render(
        request,
        "auctions/index.html",
        {
            "listings": ListingModel.objects.all(),
            "user": request.user,
        },
    )


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
        return render(
            request,
            "auctions/login.html",
            {"message": "Invalid username and/or password."},
        )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    """
    create a listing
    """
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            i_bid = form.cleaned_data["i_bid"]
            custom_category = form.cleaned_data["custom_category"]
            category = (
                custom_category if custom_category else form.cleaned_data["category"]
            )
            owner = request.user

            new_listing = ListingModel(
                title=title,
                description=description,
                i_bid=i_bid,
                owner=owner,
                category=category,
            )
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))

        return render(
            request,
            "auctions/create_listing.html",
            {
                "form": form,
            },
        )

    return render(
        request,
        "auctions/create_listing.html",
        {
            "form": NewListingForm(),
        },
    )


def listing_view(request, listing_id):
    """
    listing view
    """
    item = ListingModel.objects.get(id=listing_id)
    return render(
        request,
        "auctions/listing.html",
        {
            "item": item,
        },
    )


@login_required
def watchlist(request):
    """
    View the watchlist
    """
    user = request.user
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listing = ListingModel.objects.get(id=listing_id)
        action = request.POST.get("action")
        if action == "add":
            user.watchlist.add(listing)
        elif action == "remove":
            user.watchlist.remove(listing)

        # redirect the user back to their original location
        return redirect(request.POST.get("next", "index"))

    listed_items = ListingModel.objects.filter(interested_users=user)
    return render(
        request,
        "auctions/watchlist.html",
        {
            "items": listed_items,
        },
    )
