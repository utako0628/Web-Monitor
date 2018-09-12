"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('index/login_page/', views.login_page, name='login_page'),
    path('index/login/', views.login, name='login'),
    path('index/change_password_page/', views.change_password_page, name='change_password_page'),
    path('index/change_password/', views.change_password, name='change_password'),
    path('index/show/', views.show, name='show'),
    path('index/show/start/', views.start, name='start'),
    path('index/show/stop/', views.stop, name='stop'),
    path('index/show/stream/', views.stream, name='stream'),
    path('index/logout/', views.logout, name='logout')
]
