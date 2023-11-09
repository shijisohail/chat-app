from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, login as django_login
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from django.contrib.sessions.models import Session


@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.get(username=username)

                if user is not None and check_password(password, user.password):
                    custom_login(request, user)
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    return JsonResponse({'access_token': access_token})

        else:
            form = LoginForm()

        return render(request, 'login.html', {'form': form})
    except Exception as ex:
        print("LOGIN EXC: ", ex)


def custom_login(request, user):
    User = get_user_model()
    if isinstance(user, User):
        user_id = user.pk
    else:
        user_id = user
    request.session['user_id'] = str(user_id)


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
