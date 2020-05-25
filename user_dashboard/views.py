from django.shortcuts import render
from pymongo import MongoClient

try:
    client = MongoClient("mongodb+srv://benura:Benura123@clust1-tn0nm.mongodb.net/test?ssl=true&retryWrites=true&w=majority")
    db = client.save_password
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