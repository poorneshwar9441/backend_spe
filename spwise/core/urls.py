from django.contrib import admin
from django.urls import path
from .views import create_user_profile
from .views import login_user
from .views import simplify
from .views import create_group
from .views import create_transaction
from .views import return_groups
urlpatterns = [
    path('create_user',create_user_profile),
    path('login_user',login_user),
    # path('simplify',simplify),
    # path('create_group',create_group),
    # path('create_transaction',create_transaction),
    # path('getall',return_groups);
]
