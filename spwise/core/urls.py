from django.contrib import admin
from django.urls import path
from .views import create_user_profile
from .views import login_user
from .views import create_group
from .views import return_groups
from .views import update_group
from .views import create_expense
from .views import return_expenses
from .views import get_participant
from .views import simplify

urlpatterns = [
    path('create_user',create_user_profile),
    path('login_user',login_user),
    path('create_group',create_group),
    path('return_groups',return_groups),
    path('update_group',update_group),
    path('create_expense',create_expense),
    path('return_expenses',return_expenses),
    path('simplify',simplify),
    path('get_participants',get_participant)

]
