from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from .forms import CustomUserCreationFrom
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationFrom()
    context = {
        'form': form
    }
    return render(request,'accounts/signup.html', context)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:choice')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request,'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:login')