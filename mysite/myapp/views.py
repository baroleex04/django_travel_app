from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
# For authentication
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
                return redirect("dashboard")
    context={'loginform':form}
    return render(request, "myapp/login.html", context)

def user_logout(request):
    auth.logout(request)
    return redirect("")

@login_required(login_url="login")
def dashboard(request):
    return render(request, "myapp/dashboard.html")