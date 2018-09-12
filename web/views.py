from django.shortcuts import render, render_to_response, redirect
from django import forms
from .models import User
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from . import models
from . forms import user_form
from . forms import change_form

# Create your views here.

def index(request):
    user_cookie = request.COOKIES.get('username', '')
    if user_cookie:
        try:
            user = models.User.objects.get(name=user_cookie)
            return HttpResponseRedirect('/monitor/')
        except:
            return render(request, 'web/index.html')
    else:
        return render(request, 'web/index.html')

def login_page(request):
    user_cookie = request.COOKIES.get('username', '')
    if user_cookie:
        return HttpResponseRedirect('/monitor/')
    else:
        return render(request, 'web/login_page.html', { 'f1': user_form() })

def change_password_page(request):
    return render(request, 'web/change_password_page.html', { 'f1': change_form() })


def login(request):
    user_cookie = request.COOKIES.get('username', '')
    if user_cookie:
        return HttpResponseRedirect('/monitor/')
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
                    response =  HttpResponseRedirect('/monitor/')
                    response.set_cookie('username', username, max_age=600)
                    return response
                    #return render(request, '/index/show')
                else:
                    message = '密码不正确，请重新输入'
            except:
                message = '用户不存在'
        return render(request, 'web/login_page.html', { 'f1': f1, 'message': message })
    f1 = user_form()
    return render(request, 'web/login_page.html', { 'f1': f1 })

def change_password(request):
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
                    return redirect('/web/')
                else:
                    message = '原密码不正确，请重新输入'
            else:
                message = '用户不存在'
            return render(request, 'web/change_password_page.html', { 'f1': f1, 'message': message })

    f1 = change_form()
    return render(request,'web/change_password_page.html', { 'f1': f1 })

def logout(request):
    if request.COOKIES['username']:
        response = HttpResponseRedirect('/web/')
        response.delete_cookie('username')
        return response