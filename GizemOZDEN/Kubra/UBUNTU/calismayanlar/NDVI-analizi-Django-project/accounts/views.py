from django.shortcuts import render
from .forms import LoginForm
# Create your views here.

def login_view(request):
    form= LoginForm(rquest.Post or none)
    reurnt render(request)