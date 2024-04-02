from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import AuthenticationForm
from .models import User, ProfilePic
from .forms import RegisterForm, EditRegisterForm
from django.http import JsonResponse

from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            rform = form.save(commit=False)
            rform.role = "USER"
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
           
            image = f"default/lg/avatar2.jpg"
            propic = ProfilePic.objects.create(user=user, image=image)
            propic.save()
            login(request, user)
            messages.success(request, f"New account created: {email}")
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def profile(request, uid):
    person = get_object_or_404(User, uid=uid)
    return render(request, 'account/index.html', {'person':person})

@login_required
def editprofile(request):
    if request.method == 'POST':
        form = EditRegisterForm(request.POST, instance = request.user)
        if form.is_valid():
            rform = form.save(commit=False)
            form.save()
            return redirect('profile', uid=request.user.uid)
    else:
        form = EditRegisterForm( instance = request.user)
    return render(request, 'account/edit.html', {'form': form})


from .forms import ProfileForm
@login_required
def add_profilepic(request):
    if request.method == "POST":
        try:
            request.user.profilepic
            if request.user.profilepic:
                form =  ProfileForm(request.POST, request.FILES, instance=request.user.profilepic)
                if form.is_valid():
                    c_form = form.save(commit=False)
                    c_form.user = request.user
                    form.save()
        except:
            form =  ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                c_form = form.save(commit=False)
                c_form.user = request.user
                form.save()
    else:
        form =  ProfileForm()
    return redirect('profile', request.user.username)


from .forms import BioForm
from .models import About

@login_required
def addAbout(request):
    if request.method == "POST":
        form = BioForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            form.save()
            return redirect('profile', uid=request.user.uid)
    else:
        form = BioForm()
    return render(request, 'account/BioForm.html', {'form': form})


@login_required
def EditAbout(request):
    about = About.objects.get(user=request.user)
    if request.method == "POST":
        form = BioForm(request.POST, instance=about)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            form.save()
            return redirect('profile', uid=request.user.uid)
    else:
        form = BioForm(instance=about)
    return render(request, 'account/BioForm.html', {'form': form})
