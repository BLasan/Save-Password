import bcrypt
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from .models import Users
# Create your views here.

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
            else:
                print('Credentials Invalid!')
        else:  
            print("User Not Exists!")
    
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
            model = Users(user_name=user_name,user_email=email,password=hashed_password,salt=salt)
            model.save()
            return redirect('/')
    else:
        signupForm = SignupForm()
        hasError = False
    
    return render(response, "home_view/signup.html",{"form":signupForm,"hasError":hasError})