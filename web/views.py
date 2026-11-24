from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from . models import UserData
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(request.POST)
        user = User()
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.set_password(password)
        user.save()

        data = UserData()
        data.phone = phone
        data.age = age
        data.gender = gender
        data.user = user
        data.save()
        print(user, 'user---')
        print(data, 'data---')

        return redirect('/login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
        return redirect('/home/')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')