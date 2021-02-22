from users.forms import UserSignUpForm, EditorSignUpForm, DataAdminSignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def user_is_data_admin(user):
    return user.is_data_admin


def user_is_editor(user):
    return user.is_editor


def user_is_data_admin_or_editor(user):
    return user.is_data_admin or user.is_editor


def index(request):
    return render(request, 'index.html')


def signup(request):
    return render(request, 'users/signup.html')


def normal_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(
                request, "Normal account created! You have been logged in.")
            return redirect('index')
    else:
        form = UserSignUpForm()
    return render(request, 'users/normal_signup.html', {'form': form})


def editor_signup(request):
    if request.method == 'POST':
        form = EditorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(
                request, "Editor account created! You have been logged in.")
            return redirect('index')
    else:
        form = EditorSignUpForm()
    return render(request, 'users/editor_signup.html', {'form': form})


def data_admin_signup(request):
    if request.method == 'POST':
        form = DataAdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(
                request, "Data admin account created! You have been logged in.")
            return redirect('index')
    else:
        form = DataAdminSignUpForm()
    return render(request, 'users/data_admin_signup.html', {'form': form})
