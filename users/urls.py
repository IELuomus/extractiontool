
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from users.views import (
    signup,
    normal_signup,
    editor_signup,
    data_admin_signup
)


urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('signup/', signup, name='signup'),
    # path('signup/normal/', normal_signup, name='normal_signup'),
    # path('signup/editor/', editor_signup, name='editor_signup'),
    # path('signup/data-admin/',
    #      data_admin_signup, name='data_admin_signup'),
    # path('password-reset/', auth_views.PasswordResetView.as_view(
    #     template_name='users/password_reset.html'), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='users/password_reset_done.html'), name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
