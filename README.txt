Create virtual environment
Run the activate script which lead to the virenv
Install django
Create a django project: django-admin startproject mysite
Point to the mysite directory and run the project by: python3 manage.py runserver
Make the migration from mysite: python3 manage.py migrate
Create an app from mysite: django-admin startapp myapp
Add the app created inside mysite, setting.py: 'myapp'
In 'myapp', create a file named 'urls.py' and write some code to connect the urls.py in 'myapp' to urls.py in 'mysite'
Connect by using include keyword in urls.py in mysite
Configure views.py and map the function in views.py with the url pattern in urls.py
Create 'templates' folder in 'myapp' and in templates, create a folder name 'myapp' for containing html files
Create html files in folder 'templates/myapp' and refer to them by 'render' keyword in 'views.py'
Create a module 'form.py' in 'myapp', use the UserCreationForm and User default from django
Create a class named 'CreateUserForm' inheriting from UserCreationForm
Inside CreateUserForm, create class 'Meta' for storing the Metadata of the user. Inside class 'Meta', specify the model, fields
Modify the 'views.py' by importing 'CreateUserForm' from 'forms.py'; 
- modify the register function by identifying when to send a POST request to the database
- after saving to the database, redirect to login page
- the form passed in the views.py is used as a parameter for the form in the html file so that no need to hard code
Create a superuser for seeing the users created

In 'forms.py', import 'AuthenticationForm' for creating the class to authenticate a user
Also, import the 'forms' from 'django', 'TextInput' and 'PasswordInput' from 'django.forms.widget'

In 'views.py', import the 'auth', 'authenticate', 'login', 'logout'
Modify the my_login by the LoginForm
Add the logout feature using 'auth.logout' and modify 'urls.py'. On the dashboard can logout and redirect to the homepage

Protecting the dashboard from unauthenticated user
- use the LoginRequired
--------------------------------
Create the database with 2 classes including Dish, Address
- Setup the unique constraint for Address
- Setup the ManyToManyFields in Dish
--------------------------------
Set up the dashboard with the most 5 favorite dishes (sort by total_like)
Setup the like and dislike system by checking the user exist in the like list
Setup the search engine, however only search for exactly keyword
---------------------------------
Generate a google map location from an address of a dish
Generate a search by city and search by district