from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer,CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealers_by_state
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context={}
    if request.method == "GET":
        url = "/api/dealership/api/dealership"
        # Get dealers from the URL
        #print("url views: " +url)
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context["dealership_list"]=dealerships
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

def get_dealerships_by_state(request,state):
    context={}
    if request.method == "GET":
        url = "/api/dealership/api/dealership"
        # Get dealers from the URL
        #print("url views: " +url)
        dealerships = get_dealers_by_state(url,state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context={}
    if request.method == "GET":
        url = "/api/review/api/review"
        reviews = get_dealer_reviews_from_cf(url,dealer_id)
        # Concat all dealer's short name
        dealers_reviews = ' '.join([review.review for review in reviews])
        context["reviews_list"]=reviews
        context["dealer_id"]=dealer_id
        dealers_reviews_NLU=""
        for review in reviews:
            dealers_reviews_NLU= dealers_reviews_NLU + "<p>Review: " + review.review+ " Sentiment: "+ review.sentiment+ "</p>"
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context={}
    context["dealer_id"]=dealer_id
    if request.method == "GET":
        context['cars'] = CarModel.objects.filter(dealerid=dealer_id)
        return render(request, 'djangoapp/add_review.html', context)      
    elif request.method == 'POST':
        url = "/api/review/api/review"
        reviews = get_dealer_reviews_from_cf(url,0)
        top_id = max([review.id for review in reviews])
        new_id= top_id + 1
        new_review={}
        car = CarModel.objects.get(id=request.POST["car"])
        #print("car: ",car)
        new_review["id"] = new_id
        new_review["dealership"] = dealer_id
        new_review["car_year"] = str(car.year)
        new_review["car_make"] = car.carmake.name
        new_review["car_model"] = car.name
        new_review["review"] = request.POST["content"]
        if 'purchasecheck' in request.POST :
            new_review["purchase"] = True
            new_review["purchase_date"] = request.POST["purchasedate"]
        else:
            new_review["purchase"] = False
            new_review["purchase_date"] = ""
        new_review["name"] = request.user.get_full_name()
        json_payload={}
        json_payload["review"]=new_review
        print("payload: ",json.dumps(json_payload))
        post_request(url, json.dumps(json_payload))
        context={}
        url = "/api/dealership/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"]=dealerships
        return render(request, 'djangoapp/index.html', context)
