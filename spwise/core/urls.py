from django.contrib import admin
from django.urls import path
from .views import create_user_profile
from .views import login_user
from .views import create_group
from .views import return_groups
urlpatterns = [
    path('create_user',create_user_profile),
    path('login_user',login_user),
    path('create_group',create_group),
    path('return_groups',return_groups)
    # path('create_transaction',create_transaction),
    # path('getall',return_groups);
]
