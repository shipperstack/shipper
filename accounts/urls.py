from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import path
from django.contrib.auth import views as auth_view

from .views import *

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('password_change/',
         PasswordChange.as_view(template_name='registration/pw_change_form.html'),
         name='password_change'
         ),
    path('password_change_done/',
         PasswordChangeDone.as_view(template_name='registration/pw_change_done.html'),
         name='password_change_done'
         ),
    path('password_reset/', PasswordResetView.as_view(template_name='registration/pw_reset_form.html'),
         name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='registration/pw_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',
         PasswordResetConfirm.as_view(template_name='registration/pw_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         PasswordResetCompleteView.as_view(template_name='registration/pw_reset_complete.html'),
         name='password_reset_complete'),
]
