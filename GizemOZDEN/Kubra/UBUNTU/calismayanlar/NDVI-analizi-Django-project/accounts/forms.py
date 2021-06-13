from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(max_length=100, label="kullanıcı adi")
    password= forms.CharField(max_length=100, label="şifre", widget=forms.PasswordInput)
