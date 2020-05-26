from django.shortcuts import render
from pymongo import MongoClient
from django.http import FileResponse
import os
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
    return render(response,"user_dashboard/user_home.html")

def machine_details(response):
    #email = response.session['email']
    email = 'benuraab@gmail.com'
    print(email)
    try:
        if(db[email].find({'type': 'machine_details'}).count()>0):  
            machine_data = db[email].find({'type': 'machine_details'}).max_await_time_ms(5000)
            isEmpty = False
        else:
            machine_data = list()
            machine_data.append(list())
            isEmpty = False
        return render(response, "user_dashboard/machine_details.html", {'machine_data': machine_data[0], 'isEmpty': isEmpty})
    except:
        print("Collection not exists!")
        return render(response, "user_dashboard/error.html")

def history(response):
    #email = response.session['email']
    email = 'benuraab@gmail.com'
    try:
        if(db[email].find({'type':'history'}).count()>0):
            history = db[email].find({'type': 'history'}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            history = list()
            history.append(list())
            isEmpty = True
        return render(response, "user_dashboard/history.html", {'history_array': history[0], 'isEmpty': isEmpty})
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html")

def login_data(response):
    email = "benuraab@gmail.com"
    try:
        if(db[email].find({'type': 'login_data'}).count()>0):
            login_data = db[email].find({'type': 'login_data'}).max_await_time_ms(5000)
            isEmpty = False
        else:
            print("Empty")
            login_data = list()
            login_data.append(list())
            isEmpty = False
        return render(response, "user_dashboard/login_data.html", {'login_data': login_data[0], 'isEmpty': isEmpty})
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html")

def download_zip(response):
    path = "/Download-ZIP/save_password_exe.tar.gz"
    zip_file = open(path, 'rb')
    return FileResponse(zip_file)

