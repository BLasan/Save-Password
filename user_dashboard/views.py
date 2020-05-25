from django.shortcuts import render

# Create your views here.

def index(response):
    return render(response,"user_dashboard/user_home.html")