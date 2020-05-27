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
    return render(response,"user_dashboard/user_home.html", {'isCron': False})

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
            isEmpty = True
        return render(response, "user_dashboard/machine_details.html", {'machine_data': machine_data[0], 'isEmpty': isEmpty}, status=200)
    except:
        print("Collection not exists!")
        return render(response, "user_dashboard/error.html", status=500)

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
        return render(response, "user_dashboard/history.html", {'history_array': history[0], 'isEmpty': isEmpty}, status=200)
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html", status=500)

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
            isEmpty = True
        return render(response, "user_dashboard/login_data.html", {'login_data': login_data[0], 'isEmpty': isEmpty}, status=200)
    except:
        print("Not Found!")
        return render(response, "user_dashboard/error.html", status=500)

def bookmarks(response):
    email = "benuraab@gmail.com"
    try:
        if(db[email].find({'type': 'bookmarks'}).count()>0):
            bookmark_data = db[email].find({'type': 'bookmarks'}).max_await_time_ms(5000)
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
        if(db[email].find({'type': 'top_sites'}).count()>0):
            top_sites_data = db[email].find({'type': 'top_sites'}).max_await_time_ms(5000)
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
