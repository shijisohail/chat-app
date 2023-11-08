from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.hashers import make_password, check_password
from .models import User


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)

            if user is not None and check_password(password, user.password):
                django_login(request, user)  # Log in the user
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return JsonResponse({'access_token': access_token})

    else:  # Handle GET requests to render the login page
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            return redirect('registration_success')
    else:
        form = UserRegistrationForm()
    return render(request, '../templates/user_creation.html', {'form': form})


def registration_success(request):
    return render(request, '../templates/creation_success.html')


