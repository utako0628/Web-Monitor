from django import forms

class user_form(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)

class change_form(forms.Form):
    username = forms.CharField(label='用户名', max_length=128)
    old_password = forms.CharField(label='原密码', max_length=256, widget=forms.PasswordInput)
    new_password = forms.CharField(label='新密码', max_length=256, widget=forms.PasswordInput)
