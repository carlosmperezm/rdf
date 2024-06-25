"""Urls for the accounts app"""

from django.urls import path, URLPattern
from accounts.views import SignUpView

urlpatterns: list[URLPattern] = [
    path("signup/", SignUpView.as_view(), name="sign_up"),
]
