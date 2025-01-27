from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.http import (HttpResponseBadRequest, HttpResponseServerError,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from channels_sockets.settings import logger

from .forms import LoginForm, UserRegistrationForm
from .models import Token, User


@csrf_exempt
def login(request):
    try:
        if request.method == "POST":
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = User.objects.filter(username=username).first()

                if user is not None and check_password(password, user.password):
                    custom_login(request, user)
                    request.session.save()

                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    Token.objects.create(user=user, token=access_token)
                    request.session["Authorization"] = access_token
                    return render(request, "user/login_success.html")
                else:
                    return render(request, "user/login_failed.html")
            else:
                logger.error(
                    f"Invalid form Clean DATA: {form.cleaned_data} \n FORM ERRORS: {form.errors}"
                )
                return HttpResponseBadRequest(f"Invalid form data: {form.errors}")

        else:
            form = LoginForm()

        return render(request, "user/login.html", {"form": form})

    except Exception as ex:
        logger.error("LOGIN EXC: ", ex)
        return HttpResponseServerError(
            "An error occurred during login."
        )  # Return a generic error response


def custom_login(request, user):
    User = get_user_model()
    if isinstance(user, User):
        user_id = user.pk
    else:
        user_id = user
    request.session["user_id"] = str(user_id)


def user_registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(
                form.cleaned_data["password"]
            )  # Hash the password
            user.save()
            return redirect("registration_success")
    else:
        form = UserRegistrationForm()
    return render(request, "../templates/user/user_creation.html", {"form": form})


def registration_success(request):
    return render(request, "../templates/user/creation_success.html")
