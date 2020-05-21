from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm,SignupForm
from .models import Users
import bcrypt
# Create your views here.

#Login View
def index(response):
    if response.method == "POST":
        form = LoginForm(response.POST)
    else:
        form = LoginForm()
    
    return render(response, "home_view/login.html",{"form":form})

# Signup View
def signup(response):
    if response.method == "POST":
        signupForm = SignupForm(response.POST)
        user_name = signupForm['name'].value()
        email = signupForm['email'].value()
        password = signupForm['password'].value()
        re_password = signupForm['rePassword'].value()

        if(password != re_password):
            print("Password not matched!")
            hasError = True
        else:
            hasError = False
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode(), salt)
            print(hashed_password)
            model = Users(user_name=user_name,user_email=email,password=hashed_password)
            model.save()
            return redirect('/')
    else:
        signupForm = SignupForm()
        hasError = False
    
    return render(response, "home_view/signup.html",{"form":signupForm,"hasError":hasError})