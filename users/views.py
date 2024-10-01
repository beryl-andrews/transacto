from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")
    #return HttpResponse("hello world")

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful!")
            
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard') 
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please enter valid credentials.")
    
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            print(User.objects.count())
            print(User.objects.count() == 0)
            if User.objects.count() == 0:
                user_type = 'admin'
            else:
                user_type = 'user'

            try:
                user = User.objects.create(username=username, email=email, password=password, user_type= user_type)
                user.save()
                messages.success(request, "Registration successful. Please log in.")
                return redirect('login')
            except IntegrityError:
                messages.error(request, "Username already taken. Please choose a different username.")
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

@login_required
def admin_dashboard(request):
    if request.user.user_type == 'admin':
        return render(request, 'admin_dashboard.html')
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')


@login_required
def user_dashboard(request):
    if request.user.user_type == 'user':
        return render(request, 'user_dashboard.html')
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')




