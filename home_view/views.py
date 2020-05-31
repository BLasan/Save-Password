import bcrypt
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from .models import Users
import requests
from pymongo import MongoClient
from datetime import date,datetime,timedelta
import jwt
import base64
import requests
# Create your views here.

JWT_SECRET = 'save_password'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600

try:
    client = MongoClient("mongodb+srv://benura:Benura123@clust1-tn0nm.mongodb.net/test?ssl=true&retryWrites=true&w=majority")
    db = client.save_password
    users = db['users']
    sessions = db['sessions']
    #email = response.session['email']
except:
    print("Connection Error!")

#Login View
def index(response,token=None):
    if response.method == "POST":
        form = LoginForm(response.POST)
        email = form['email'].value()
        password = form['password'].value()
        try:
            #user_data = Users.objects.filter(user_email=email).values()[0]
            user_data = users.find_one({'type': 'user_credentials', 'email': email})
            if(user_data != None):
                isExists = True
            else:
                isExists = False
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
            payload = {
                'user_id': str(user_data['_id']),
                'user_email': user_data['email'],
                'user_name': user_data['user_name'],
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
            print(jwt_token)
            # hashed_password = bcrypt.hashpw(password.encode(),salt)
            # print(hashed_password)
            is_equal = bcrypt.checkpw(password.encode(), user_data['password'])
            if(is_equal):
                print("Login Success!")
                print(users.find_one({'type': 'user_credentials', 'email': email, 'isLoggedIn': False}))
                if(users.find_one({'type': 'user_credentials', 'email': email, 'isLoggedIn': False})):
                    try:
                        users.update_one({'type': 'user_credentials', 'email': email}, {"$set": {'isLoggedIn': True}})
                        if(token is not None):
                            sessions.update_one({'type': 'session_data', 'email': email},{"$set": {'last_login': datetime.today(), 'token': jwt_token.decode('utf-8'), 'isExpired': False}})
                        sessions.update_one({'type': 'session_data', 'email': email},{"$set": {'last_login': datetime.today(), 'token': jwt_token.decode('utf-8')}})
                    except BaseException as e:
                        print(e)
                        return redirect('/error')
                    #requests.Session['email'] = email
                    url = f"/dashboard/{jwt_token.decode('utf-8')}"
                    dashboard_response = redirect(url)
                    #dashboard_response.setdefault('Authorization', f"Bearer {jwt_token.decode('utf-8')}")
                    #dashboard_response['Authorization'] = f"Bearer {jwt_token.decode('utf-8')}"
                    #dashboard_response['Access-Control-Expose-Headers'] = "*"
                    #print(dashboard_response._headers)
                    return dashboard_response
                else:
                    print("Already LoggedIn")
                    token = jwt_token.decode('utf-8')
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
    print(token,"Token")
    if(token is not None):
        is_expired = sessions.find_one({'type': 'session_data', 'token': token})['isExpired']
        if(is_expired):
            has_error = True
            error_message = "Token Expired!"
    print(error_message)
    return render(response, "home_view/login.html",{"form":form, 'has_error': has_error, 'error_message': error_message, 'token': token })

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
                sessions.insert_one({'type': 'session_data', 'last_login': datetime.today(), 'token': None, 'email': email,'isExpired': False})
                return redirect('/')
    else:
        signupForm = SignupForm()
        has_error = False
        error_message = None
    
    return render(response, "home_view/signup.html",{"form":signupForm,"hasError":has_error, "error_message": error_message})

def logout(response):
    users.update_one({'type': 'user_credentials', 'email': 'benuraab@gmail.com', 'isLoggedIn': True}, {"$set": {'isLoggedIn': False}})
    return redirect('/')


def session_expired(response, has_error_param, error_message_param):
    form  = LoginForm()
    has_error = has_error_param
    error_message = error_message_param
    print(has_error)
    return render(response, "home_view/login.html",{"form":form, 'has_error': has_error, 'error_message': error_message})