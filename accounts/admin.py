"""File to manage the admin site for the accounts app"""

from django.contrib import admin
from accounts.models import User

admin.site.register(User)
