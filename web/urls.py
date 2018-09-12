from django.urls import path, include
from . import views

app_name = 'web'
urlpatterns = [
    path('', views.index),
    path('login_page/', views.login_page, name='login_page'),
    path('login/', views.login, name='login'),
    path('change_password_page/', views.change_password_page, name='change_password_page'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.logout, name='logout'),
]