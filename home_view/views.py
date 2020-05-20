from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm,SignupForm

# Create your views here.

def index(response):
    if response.method == "POST":
        form = LoginForm(response.POST)
    else:
        form = LoginForm()
    
    return render(response, "home_view/login.html",{"form":form})

def signup(response):
    if response.method == "POST":
        signupForm = SignupForm(response.POST)
    else:
        signupForm = SignupForm()
    
    return render(response, "home_view/signup.html",{"form":signupForm})