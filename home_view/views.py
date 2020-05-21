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
        password = signupForm['password'].value()
        re_password = signupForm['rePassword'].value()

        if(password != re_password):
            print("Password not matched!")
            hasError = True
        else:
            hasError = False
    else:
        signupForm = SignupForm()
        hasError = False
    
    return render(response, "home_view/signup.html",{"form":signupForm,"hasError":hasError})