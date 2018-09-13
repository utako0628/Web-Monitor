from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django import forms
from web.models import User
from web.videoCamera import gen, VideoCamera
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
from . import models
from . forms import user_form
from . forms import change_form

# Create your views here.

def index(request):
    return render(request, 'index.html')

def show(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera('web/deploy.prototxt', 'web/MobileNetSSD_deploy.caffemodel')),
                                     content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")


def login(request):
    if request.method == 'POST':
        f1 = user_form(request.POST)
        if f1.is_valid():
            username = f1.cleaned_data['username']
            password = f1.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    #return redirect('/index/')
                    #return render_to_response('http://127.0.0.1:8000/index/show')
                    return redirect('http://127.0.0.1:8000/index/show')
                    #return render(request, '/index/show')
                else:
                    message = '密码不正确，请重新输入'
            except:
                message = '用户不存在'
        return render(request, 'login.html', locals())
    f1 = user_form()
    return render(request, 'login.html', locals())

def changepassword(request):
    if request.method == 'POST':
        f1 = change_form(request.POST)
        if f1.is_valid():
            username = f1.cleaned_data['username']
            old_password = f1.cleaned_data['old_password']
            new_password = f1.cleaned_data['new_password']
            user = User.objects.filter(name=username)
            if user:
                pw = User.objects.filter(name=username, password=old_password)
                if pw:
                    User.objects.filter(name=username, password=old_password).update(password=new_password)
                    return redirect('/index/')
                else:
                    message = '原密码不正确，请重新输入'
            else:
                message = '用户不存在'
            return render(request, 'changepassword.html', locals())

    f1 = change_form()
    return render(request,'changepassword.html', locals())