from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
import urllib.parse
# For authentication
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

def generate_google_maps_url(address):
    base_url = 'https://www.google.com/maps/search/?api=1&query='
    encoded_address = urllib.parse.quote(address)  # URL encode the address
    search_url = base_url + encoded_address
    return search_url

def iscontain(name, checkcontain):
    if name.__contains__(checkcontain):
        return True
    return False

def homepage(request):
    return render(request, "myapp/index.html")

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save() # save the data to the database, after that, redirect
            return redirect("login") # match with the route name
    context = {'registerform':form} # move to file html
    return render(request, "myapp/register.html" ,context=context)

def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("myapp:dashboard")
    context={'loginform':form}
    return render(request, "myapp/login.html", context)

def user_logout(request):
    auth.logout(request)
    return redirect("myapp:")

@login_required(login_url="login")
def dashboard(request):
    best_five_dishes = Dish.objects.order_by("-total_like")[:5]
    context = {
        "best_five_dishes": best_five_dishes
    }
    return render(request, "myapp/dashboard.html", context)

@login_required(login_url="login")
def detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    address = dish.address
    msg = None
    if request.user.is_authenticated:
        if dish.likers.filter(id=request.user.id).exists():
            msg = "liked"
    
    if msg == None:
        if (request.GET.get('likebtn')):
            dish.total_like = F("total_like")+1
            dish.likers.add(request.user)
            dish.save()
            return HttpResponseRedirect(reverse("myapp:detail", args=(dish.id,)))
    else:
        if (request.GET.get('dislikebtn')):
            dish.total_like = F("total_like")-1
            dish.likers.remove(request.user)
            dish.save()
            return HttpResponseRedirect(reverse("myapp:detail", args=(dish.id,)))
    context = {
        "dish": dish,
        "address": address,
        "msg": msg
    }
    return render(request, "myapp/detail.html", context)

@login_required(login_url="login")
def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        dish_list = Dish.objects.all().filter(name__icontains=search)
        context = {
            "dish_list": dish_list
        }
    return render(request, "myapp/search.html", context)

@login_required(login_url="login")
def searchcity(request):
    if request.method == 'GET':
        search = request.GET.get('searchcity')
        all_dish = Dish.objects.all()
        dish_list = []
        for dish in all_dish:
            address = dish.address.filter(is_primary=True).first()
            if iscontain(address.city, search):
                dish_list.append(dish)
        context = {
            "dish_list": dish_list
        }
    return render(request, "myapp/searchcity.html", context)

@login_required(login_url="login")
def searchdistrict(request):
    searchdistrict = request.GET.get('searchdistrict')
    dish_ids = request.GET.getlist('dish_list')  # Get the list of dish IDs
    valid_dish_ids = [int(dish_id) for dish_id in dish_ids if dish_id.isdigit()]
    dishes = Dish.objects.filter(id__in=valid_dish_ids)
    dish_list = []
    for dish in dishes:
        address = dish.address.filter(is_primary=True).first()
        if address.district == searchdistrict:
            dish_list.append(dish)
    context = {
        "dish_list": dish_list
    }
    return render(request, 'myapp/searchdistrict.html', context)

@login_required(login_url="login")
def map(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    address = dish.address.filter(is_primary=True).first()
    string_address = address.number + " đường " + address.street + ", phường " + address.ward + ", quận " + address.district + ", " + address.city
    maps_url = generate_google_maps_url(string_address)
    return HttpResponse(maps_url)