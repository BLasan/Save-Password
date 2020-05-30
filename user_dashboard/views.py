from django.shortcuts import render
from pymongo import MongoClient
from django.http import FileResponse
import os
from django.http import JsonResponse,HttpResponseBadRequest,HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
import json
import bcrypt
from .forms import ChangeCredentialsForm,ProfileDataForm,FeedBackForm

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

def index(response):
    return render(response,"user_dashboard/user_home.html", {'isCron': False})

def machine_details(response):
    #email = response.session['email']
    email = 'benuraab@gmail.com'
    print(email)
    try:
        if(db.machine_details.find_one({'type': 'machine_details', 'email': email})):  
            machine_data = db.machine_details.find({'type': 'machine_details', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
        else:
            machine_data = list()
            machine_data.append(list())
            isEmpty = True
        return render(response, "user_dashboard/machine_details.html", {'machine_data': machine_data[0], 'isEmpty': isEmpty}, status=200)
    except:
        print("Collection not exists!")
        return render(response, "user_dashboard/error.html", status=500)

def history(response):
    #email = response.session['email']
    email = 'benuraab@gmail.com'
    try:
        if(db.history.find_one({'type':'history', 'email': email})):
            history = db.history.find({'type': 'history', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            history = list()
            history.append(list())
            isEmpty = True
        return render(response, "user_dashboard/history.html", {'history_array': history[0], 'isEmpty': isEmpty}, status=200)
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html", status=500)

def login_data(response):
    email = "benuraab@gmail.com"
    log_in_data_list = list()
    #form = ChangeCredentialsForm()
    if(response.is_ajax()):
        user_name = response.POST.get('user_name', None)
        password = response.POST.get('user_password', None)
        url = response.POST.get('url', None)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        print(hashed_password)
        #form = ChangeCredentialsForm(initial={'email': email_data })
        if(user_name == '' or password == ''):
            status = 500
            return JsonResponse({'status': status})
        else:
            status = 200
            login_data = db.login_data.find({'type': 'login_data', 'email': email}).max_await_time_ms(5000)
            login_array = login_data[0]
            print(login_array)
            for data in login_array["login"]:
                if(data[0] == url):
                    data[1] = user_name
                    try:
                        data[2] = hashed_password
                        data[3] = salt
                    except:
                        print("Not Exists!")
                    finally:
                        data.append(hashed_password)
                        data.append(salt)
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
            login_data = db[email].find({'type': 'login_data', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            login_data = list()
            login_data.append(list())
            isEmpty = True
        #print(form)
        return render(response, "user_dashboard/login_data.html", {'login_data': login_data[0], 'isEmpty': isEmpty}, status=200)
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html",status=500)

def bookmarks(response):
    email = "benuraab@gmail.com"
    try:
        if(db.bookmarks.find({'type': 'bookmarks', 'email': email}).count()>0):
            bookmark_data = db.bookmarks.find({'type': 'bookmarks', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            bookmark_data = list()
            bookmark_data.append(list())
            isEmpty = True
        return render(response, "user_dashboard/bookmarks.html", {'bookmark_data': bookmark_data[0], 'isEmpty': isEmpty}, status=200)
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html", status=500)

def top_sites(response):
    email = "benuraab@gmail.com"
    try:
        if(db.top_sites.find({'type': 'top_sites', 'email': email}).count()>0):
            top_sites_data = db.top_sites.find({'type': 'top_sites', 'email': email}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            top_sites_data = list()
            top_sites_data.append(list())
            isEmpty = True
        return render(response, "user_dashboard/top_sites.html", {'top_sites_data': top_sites_data[0], 'isEmpty': isEmpty}, status=200)
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html", status=500)


def download_zip(response):
    path = "/Download-ZIP/save_password_exe.tar.gz"
    zip_file = open(path, 'rb')
    return FileResponse(zip_file)

def settings(response):
    email = 'benuraab@gmail.com'
    user_name = 'Benura'
    form = ChangeCredentialsForm(initial={'email':email})
    profile_data_form = ProfileDataForm(initial={'user_name': user_name})
    feedback_form = FeedBackForm()
    return render(response, "user_dashboard/settings.html", {'form': form, 'profile_form': profile_data_form, 'feedback_form': feedback_form})