from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_registration, name='user_registration'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('login/', views.login, name='login'),

]
