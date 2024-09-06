from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
# For authentication
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

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