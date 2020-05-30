import bcrypt
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from .models import Users
import requests
from pymongo import MongoClient
from datetime import date,datetime
# Create your views here.

try:
    client = MongoClient("mongodb+srv://benura:Benura123@clust1-tn0nm.mongodb.net/test?ssl=true&retryWrites=true&w=majority")
    db = client.save_password
    users = db['users']
    #email = response.session['email']
except:
    print("Connection Error!")

#Login View
def index(response):
    if response.method == "POST":
        form = LoginForm(response.POST)
        email = form['email'].value()
        password = form['password'].value()
        try:
            user_data = Users.objects.filter(user_email=email).values()[0]
            isExists = True
        except IndexError as e:
            print(e)
            isExists = False
        except:
            isExists = False
            print("Database Error")

        if(isExists):
            print(user_data['password'])
            salt = user_data['salt']
            print(salt)
            # hashed_password = bcrypt.hashpw(password.encode(),salt)
            # print(hashed_password)
            is_equal = bcrypt.checkpw(password.encode(), user_data['password'])
            if(is_equal):
                print("Login Success!")
                print(users.find_one({'type': 'user_credentials', 'email': email, 'isLoggedIn': False}))
                if(users.find_one({'type': 'user_credentials', 'email': email, 'isLoggedIn': False})):
                    users.update_one({'type': 'user_credentials', 'email': email}, {"$set": {'isLoggedIn': True}})
                    #requests.Session['email'] = email
                    return redirect('/dashboard')
                else:
                    print("Already LoggedIn")
                    has_error = True
                    error_message = "You are already Logged In!"

            else:
                print('Credentials Invalid!')
                has_error = True
                error_message = "Credentials Invalid!"
        else:  
            print("User Not Exists!")
            has_error = True
            error_message = "User Not Exists!"
    else:
        has_error = False
        error_message = None
    form = LoginForm()
    return render(response, "home_view/login.html",{"form":form, 'has_error': has_error, 'error_message': error_message})

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
            has_error = True
            error_message = "Password Not Matched!"
        else:
            has_error = False
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode(), salt)
            print(hashed_password)
            # model = Users(user_name=user_name,user_email=email,password=hashed_password,salt=salt)
            # model.save()
            if(users.find({'email': email}).count()>0):
                has_error = True
                print("User already exists!")
                error_message = "User Already Exists!"
            else:
                users.insert_one({'type': 'user_credentials','user_name': user_name, 'email': email, 'password': hashed_password, 'salt': salt, 'date': datetime.today(), 'isVerified': False, 'avatar': None, 'isLoggedIn': False})
                return redirect('/')
    else:
        signupForm = SignupForm()
        has_error = False
        error_message = None
    
    return render(response, "home_view/signup.html",{"form":signupForm,"hasError":has_error, "error_message": error_message})

def logout(response):
    users.update_one({'type': 'user_credentials', 'email': 'benuraab@gmail.com', 'isLoggedIn': True}, {"$set": {'isLoggedIn': False}})
    return redirect('/')