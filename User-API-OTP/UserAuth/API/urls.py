from django.urls import path
from .views import create_user, verify_otp, login,list_users

urlpatterns = [
    path('create-user/', create_user, name='create-user'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('login/', login, name='login'),
    path('list/',list_users,name='list_users')
]
