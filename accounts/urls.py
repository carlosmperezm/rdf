"""Urls for the accounts app"""

from django.urls import path, URLPattern
from accounts.views import SignUpView, LoginView, UserInfoView

urlpatterns: list[URLPattern] = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("userinfo/", UserInfoView.as_view(), name="userinfo"),
]
