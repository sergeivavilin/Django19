from django import forms


class UserRegister(forms.Form):
    username = forms.CharField(label='Введите логин', max_length=30)
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, min_length=8)
    age = forms.IntegerField(label='Введите свой возраст', min_value=7, max_value=150)