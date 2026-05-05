# from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .forms import LoginForm

app_name = 'users'

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),  # users:signup
    path('login/', LoginView.as_view(template_name='users/login.html', form_class=LoginForm, redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),
]