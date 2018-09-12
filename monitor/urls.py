from django.urls import path
from . import views


app_name = 'monitor'
urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.start, name='start'),
    path('stop', views.stop, name='stop'),
    path('stream', views.stream, name='stream')
]