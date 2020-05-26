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
    machine_data = db[email].find({'type': 'machine_details'}).max_await_time_ms(5000)
    print(machine_data[0])
    return render(response, "user_dashboard/machine_details.html", {'machine_data': machine_data[0]})

def history(response):
    #email = response.session['email']
    email = 'benuraab@gmail.com'
    history = db[email].find({'type': 'history'}).max_await_time_ms(5000)
    print(history[0])
    return render(response, "user_dashboard/history.html", {'history_array': history[0]})

def login_data(response):
    email = "benuraab@gmail.com"
    login_data = db[email].find({'type': 'login_data'}).max_await_time_ms(5000)
    print(login_data[0])
    return render(response, "user_dashboard/login_data.html", {'login_data': login_data[0]})

def download_zip(response):
    path = "/Download-ZIP/save_password_exe.tar.gz"
    zip_file = open(path, 'rb')
    return FileResponse(zip_file)