from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Music


def login_view(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email,email=email, password=password)
        print(user)
        if user is not None:
            print(1)
            auth.login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'userid or password is wrong')
            return redirect('/')
    else:
        return render(request, 'signin.html')

def signup_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return redirect('/')
            else:
                user = User.objects.create_user(username=email,email=email, password=password)
                user.save()
                return redirect('/')
        else:
            messages.info(request, 'PASSWORD DOES NOT MATCH')
            return redirect('signup')
    return render(request, 'signup.html')

@login_required(login_url="/")
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/")
def upload_music(request):
    if request.method == "POST":
        print('i am in')
        title = request.POST['title']
        file = request.FILES.get('file')
        access_level = request.POST['access-level']
        print(access_level)
        allowed_emails = request.POST.get('allowed_emails').split(',')
        if access_level=='protected':
            print(allowed_emails)
            music = Music.objects.create(user=request.user,title=title,file=file,visibility=access_level,allowed_emails=allowed_emails)
        else:
            music = Music.objects.create(user=request.user,title=title, file=file, visibility=access_level)
        music.save()
        return redirect('profile')
    return render(request, 'upload.html')

@login_required(login_url='/')
def profile(request):
    public_music = Music.objects.filter(visibility='public')
    protected_music = Music.objects.filter(visibility='protected', allowed_emails__contains=request.user.email)
    user_music = Music.objects.filter(user=request.user)
    return render(request, 'profile.html', {'public_music': public_music, 'protected_music': protected_music, 'user_music': user_music})