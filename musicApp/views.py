from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm,MusicForm
from .models import Music
from django.urls import reverse


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


def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required
def upload_music(request):
    form = MusicForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        music = form.save(commit=False)
        music.user = request.user
        music.save()
        return redirect('profile')
    return render(request, 'upload.html', {'form': form})

@login_required
def profile(request):
    public_music = Music.objects.filter(visibility='public')
    protected_music = Music.objects.filter(visibility='protected', allowed_emails__contains=request.user.email)
    user_music = Music.objects.filter(user=request.user)
    return render(request, 'profile.html', {'public_music': public_music, 'protected_music': protected_music, 'user_music': user_music})