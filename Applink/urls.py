from django.contrib import admin
from django.urls import path , re_path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    path('register',registerUser, name='register'),
    path('fillGoogle',register_user_google, name='fillup'),
    path('subscribtion', subscribtion, name='subscribe' ),
    path('auth', obtain_auth_token ),
    path('login', loginUser , name='login'),
    path('sample', sample_api ),
    path("logout", logout, name='logout'),
    path("update", update, name='up'),
    path("delete", delete, name='delete'),
    path("change_your_password", change_password, name='change'),
    path('is_connected', is_connected, name='verify_connection'),
    path('user_forgot_password', forgot_password, name='api_forgot'),
    path('user_refresh_password', forgot_password_change, name='api_refresh'),
    path('all_tables_users', get_all_user),
    path('delete_users_admin', delete_on_user, name='delete_user'),
    path('contact_enter', contact_register, name='contact_enter'),
    path('translate', translate, name='translate'),
    path('phone_verification',phone_verification, name='phone_verification')

]