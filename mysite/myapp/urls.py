from django.urls import path
from myapp.views import *

urlpatterns = [
    path("", homepage, name=""),
    path("register/", register, name="register"),
    path("login/", my_login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", user_logout, name="logout"),
]