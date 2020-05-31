from django.shortcuts import render,redirect
from pymongo import MongoClient
from django.http import FileResponse
import os
from django.http import JsonResponse,HttpResponseBadRequest,HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
import json
import bcrypt
from .forms import ChangeCredentialsForm,ProfileDataForm,FeedBackForm,LoginForm
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import jwt
import base64
import requests

JWT_SECRET = 'save_password'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600

cur_path = os.path.dirname(__file__)
print(cur_path)
print(os.path.dirname(os.path.relpath('..\\save_password_exe.tar.gz', cur_path)))

try:
    client = MongoClient("mongodb+srv://benura:Benura123@clust1-tn0nm.mongodb.net/test?ssl=true&retryWrites=true&w=majority")
    db = client.save_password
    #email = response.session['email']
except:
    print("Connection Error!")

# Create your views here.

def index(response,token):
    try:
        jwt_token = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=JWT_ALGORITHM)
        email = jwt_token['user_email']
    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.ExpiredSignature):
        try:
            email = db.sessions.find_one({'type': 'session_data', 'token': token})['email']
            db.sessions.update_one({'type': 'session_data', 'token': token, 'email': email}, {"$set": {'isExpired': True}})
            db.users.update_one({'type': 'user_credentials', 'email': email}, {"$set": {'isLoggedIn': False}})
        except BaseException as e:
            print(e)
            return redirect('/error')
        url = f"/{token}"
        return redirect(url)
    return render(response,"user_dashboard/user_home.html", {'isCron': False, 'token': token})



def machine_details(response,token):
    #email = response.session['email']
    #print(token.encode('utf-8'))
    
    #print(jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM))
    try:
        jwt_token = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=JWT_ALGORITHM)
        email = jwt_token['user_email']
        if(db.machine_details.find_one({'type': 'machine_details', 'email': email})): 
            machine_data = db.machine_details.find({'type': 'machine_details', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
            print("Test1")
        else:
            machine_data = list()
            machine_data.append(list())
            isEmpty = True
            print("Test2")
        return render(response, "user_dashboard/machine_details.html", {'machine_data': machine_data[0], 'isEmpty': isEmpty, 'token': token})
    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.ExpiredSignature):
        print('Token Expired!')
        try:
            email = db.sessions.find_one({'type': 'session_data', 'token': token})['email']
            db.sessions.update_one({'type': 'session_data', 'email': email, 'token': token}, {"$set": {'isExpired': True}})
            db.users.update_one({'type': 'user_credentials', 'email': email}, {"$set": {'isLoggedIn': False}})
        except BaseException as e:
            print(e)
            return redirect('/error')
        # has_error_param = True
        # error_message_param = "Token Expired!"
        #url = f"/session_expired/{has_error_param}/{error_message_param}"
        url = f"/{token}"
        return redirect(url)
    except BaseException as e:
        print(e)
        return redirect('/error')



def history(response, token):
    #email = response.session['email']
    try:
        jwt_token = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=JWT_ALGORITHM)
        email = jwt_token['user_email']
        if(db.history.find_one({'type':'history', 'email': email})):
            history = db.history.find({'type': 'history', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            history = list()
            history.append(list())
            isEmpty = True
        return render(response, "user_dashboard/history.html", {'history_array': history[0], 'isEmpty': isEmpty, 'token': token})
    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.ExpiredSignature):
        print('Token Expired!')
        try:
            email = db.sessions.find_one({'type': 'session_data', 'token': token})['email']
            db.sessions.update_one({'type': 'session_data', 'email': email, 'token': token}, {"$set": {'isExpired': True}})
            db.users.update_one({'type': 'user_credentials', 'email': email}, {"$set": {'isLoggedIn': False}})
        except BaseException as e:
            print(e)
            return redirect('/error')
        # has_error_param = True
        # error_message_param = "Token Expired!"
        #url = f"/session_expired/{has_error_param}/{error_message_param}"
        url = f"/{token}"
        return redirect(url)
    except BaseException as e:
        print(e)
        return redirect('/error')



def login_data(response,token):
    try:
        jwt_token = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=JWT_ALGORITHM)
        email = jwt_token['user_email']
    except (jwt.exceptions.ExpiredSignature, jwt.exceptions.ExpiredSignatureError):
        print('Token Expired!')
        try:
            email = db.sessions.find_one({'type': 'session_data', 'token': token})['email']
            db.sessions.update_one({'type': 'session_data', 'email': email, 'token': token}, {"$set": {'isExpired': True}})
            db.users.update_one({'type': 'user_credentials', 'email': email}, {"$set": {'isLoggedIn': False}})
        except BaseException as e:
            print(e)
            return redirect('/error')
        # has_error_param = True
        # error_message_param = "Token Expired!"
        # url = f"/session_expired/{has_error_param}/{error_message_param}"
        url = f"/{token}"
        return redirect(url)

    log_in_data_list = list()
    #form = ChangeCredentialsForm()
    if(response.is_ajax()):
        user_name = response.POST.get('user_name', None)
        password = response.POST.get('user_password', None)
        url = response.POST.get('url', None)
        # salt = bcrypt.gensalt()
        # hashed_password = bcrypt.hashpw(password.encode(), salt)
        password = password.encode() # Convert to type bytes
        salt = os.urandom(16) # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
        fernet = Fernet(key)
        encrypt_password = fernet.encrypt(password)
        print(encrypt_password)
        #form = ChangeCredentialsForm(initial={'email': email_data })
        if(user_name == '' or password == ''):
            status = 500
            return JsonResponse({'status': status})
        else:
            status = 200
            login_data = db.login_data.find({'type': 'login_data', 'email': email}).max_await_time_ms(5000)
            login_array = login_data[0]
            #print(login_array)
            for data in login_array["login"]:
                if(data[0] == url):
                    data[1] = user_name
                    try:
                        data[2] = encrypt_password
                        data[3] = key
                    except:
                        print("Not Exists!")
                        data.append(encrypt_password)
                        data.append(key)
                   # print(data)
                log_in_data_list.append(data)
                print(log_in_data_list)
            try:
                db.login_data.update_one({'type': 'login_data', 'email': email}, {"$set": {'login': log_in_data_list}})
            except BaseException as e:
                print(e)
                status = 500
            finally:
                return JsonResponse({'status': status})

    try:
        if(db.login_data.find_one({'type': 'login_data', 'email': email})):
            login_data = db.login_data.find({'type': 'login_data', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            login_data = list()
            login_data.append(list())
            isEmpty = True
        #print(form)
        return render(response, "user_dashboard/login_data.html", {'login_data': login_data[0], 'isEmpty': isEmpty, 'token': token}, status=200)
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html",status=500)



def bookmarks(response,token):
    try:
        jwt_token = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=JWT_ALGORITHM)
        email = jwt_token['user_email']
        if(db.bookmarks.find({'type': 'bookmarks', 'email': email}).count()>0):
            bookmark_data = db.bookmarks.find({'type': 'bookmarks', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            bookmark_data = list()
            bookmark_data.append(list())
            isEmpty = True
        return render(response, "user_dashboard/bookmarks.html", {'bookmark_data': bookmark_data[0], 'isEmpty': isEmpty, 'token': token}, status=200)
    except (jwt.exceptions.ExpiredSignature, jwt.exceptions.ExpiredSignatureError):
        print('Token Expired!')
        try:
            email = db.sessions.find_one({'type': 'session_data', 'token': token})['email']
            db.sessions.update_one({'type': 'session_data', 'email': email, 'token': token}, {"$set": {'isExpired': True}})
            db.users.update_one({'type': 'user_credentials', 'email': email}, {"$set": {'isLoggedIn': False}})
        except BaseException as e:
            print(e)
            return redirect('/error')
        # has_error_param = True
        # error_message_param = "Token Expired!"
        # url = f"/session_expired/{has_error_param}/{error_message_param}"
        url = f"/{token}"
        return redirect(url)
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html", status=500)



def top_sites(response,token):
    try:
        jwt_token = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=JWT_ALGORITHM)
        email = jwt_token['user_email']
        if(db.top_sites.find({'type': 'top_sites', 'email': email}).count()>0):
            top_sites_data = db.top_sites.find({'type': 'top_sites', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            top_sites_data = list()
            top_sites_data.append(list())
            isEmpty = True
        return render(response, "user_dashboard/top_sites.html", {'top_sites_data': top_sites_data[0], 'isEmpty': isEmpty, 'token': token}, status=200)
    except (jwt.exceptions.ExpiredSignature, jwt.exceptions.ExpiredSignatureError):
        print('Token Expired!')
        try:
            email = db.sessions.find_one({'type': 'session_data', 'token': token})['email']
            db.sessions.update_one({'type': 'session_data', 'email': email, 'token': token}, {"$set": {'isExpired': True}})
            db.users.update_one({'type': 'user_credentials', 'email': email}, {"$set": {'isLoggedIn': False}})
        except BaseException as e:
            print(e)
            return redirect('/error')
        # has_error_param = True
        # error_message_param = "Token Expired!"
        # url = f"/session_expired/{has_error_param}/{error_message_param}"
        url = f"/{token}"
        return redirect(url)
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html", status=500)



def download_zip(response):
    path = "/Download-ZIP/save_password_exe.tar.gz"
    zip_file = open(path, 'rb')
    return FileResponse(zip_file)



def settings(response,token):
    try:
        jwt_token = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=JWT_ALGORITHM)
        email = jwt_token['user_email']
        user_name = jwt_token['user_name']
    except (jwt.exceptions.ExpiredSignature, jwt.exceptions.ExpiredSignatureError):
        print('Token Expired!')
        try:
            email = db.sessions.find_one({'type': 'session_data', 'token': token})['email']
            db.sessions.update_one({'type': 'session_data', 'email': email, 'token': token}, {"$set": {'isExpired': True}})
            db.users.update_one({'type': 'user_credentials', 'email': email}, {"$set": {'isLoggedIn': False}})
        except BaseException as e:
            print(e)
            return redirect('/error')
        # has_error_param = True
        # error_message_param = "Token Expired!"
        url = f"/{token}"
        return redirect(url)

    message = None
    has_error = None
    error_type = None

    if response.method == "POST":
        try:
            form = ChangeCredentialsForm(response.POST)
            user_email = form['email'].value()
            password = form['password'].value()
            print(email,password)
            if(email is not None or password is not None):
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
                user_data = db.users.find_one_and_update({"type": 'user_credentials', 'email': user_email},{"$set": {'password': hashed_password, 'salt': salt}})
                if(user_data is not None):
                    print("Success")
                    message  = "Success"
                    has_error = False
                else:
                    print("Not Successed")
                    message = "Not Success"
                    has_error = True
                error_type = "Credentials"
        except BaseException as e:
            print(e)
        finally:
            try:
                profile_data_form = ProfileDataForm(response.POST)
                user_name = profile_data_form['user_name'].value()
                timer = profile_data_form['timer'].value()
                print(timer)
                if(timer is not None or user_name is not None):
                    user_data = db.users.find_one_and_update({'type': 'user_credentials', 'email': email}, {"$set": {"user_name": user_name}})
                    if(user_data is not None):
                        print("Success")
                        message = "Success"
                        has_error = False
                    else:
                        print("Not Success")
                        message = "Not Success"
                        has_error = True
                    error_type = "Profile"
            except BaseException as e:
                print(e)
            finally:
                try:
                    feedback_form = FeedBackForm(response.POST)
                    reason = feedback_form['reason'].value()
                    print(reason)
                    if(reason is not None):
                        if("feedback" in db.list_collection_names()):
                            user_data_input = db.users.find_one_and_update({'type': 'user_credentials', 'email': email}, {"$set": {'isActive': False}})
                            user_data = db.feedback.find_one_and_update({"type":"feedback", "email": email}, {"$set": {'reason': reason}})
                            if(user_data is not None and user_data_input is not None):
                                print("Success")
                                has_error = False
                                message = "Success"
                            else:
                                print("Not Success")
                                has_error = True
                                message = "Not Success"
                            error_type = "Feedback"
                        else:
                            db.feedback.insert_one({'type': 'feedback', 'email': email, 'reason': reason})
                except BaseException as e:
                    print(e)

    form = ChangeCredentialsForm(initial={'email':email})
    profile_data_form = ProfileDataForm(initial={'user_name': user_name, 'email': email})
    feedback_form = FeedBackForm()

    return render(response, "user_dashboard/settings.html", {'form': form, 'profile_form': profile_data_form, 'feedback_form': feedback_form, 'token': token, 'message': message, 'has_error': has_error, 'error_type': error_type})


def error(response):
    return render(response, "user_dashboard/error.html")