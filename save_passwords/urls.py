"""save_passwords URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home_view import views
from user_dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('signup/',views.signup, name="signup"),
    path('dashboard/',dashboard_views.index, name="index"),
    path('machine_details/', dashboard_views.machine_details, name="machine_details"),
    path('history/', dashboard_views.history, name='history'),
    path('login_data/', dashboard_views.login_data, name='login_data'),
    path('download_zip/', dashboard_views.download_zip, name="download_zip"),
    path('bookmarks/', dashboard_views.bookmarks, name="bookmarks"),
    path('top_sites/', dashboard_views.top_sites, name="top_sites"),
    path('settings/', dashboard_views.settings, name="settings")
]
