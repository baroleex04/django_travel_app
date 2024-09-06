from django.urls import path
from myapp.views import *

app_name="myapp"
urlpatterns = [
    path("", homepage, name=""),
    path("register/", register, name="register"),
    path("login/", my_login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("search/", search, name="search"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/<int:dish_id>", detail, name="detail")
]