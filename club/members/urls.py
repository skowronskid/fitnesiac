from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login_user', views.login_user,name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user/', views.register_user, name='register_user'),
    path('activate/(<uidb64>/<token>/', views.activate, name='activate'), 

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='pass_reset/password_reset.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='pass_reset/password_reset_sent.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pass_reset/password_reset_form.html'), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='pass_reset/password_reset_done.html'),name="password_reset_complete"),

    path('<str:username>/profile/', views.view_profile, name='profile'),
    path('profile/settings/', views.change_user_settings, name='settings'),
    path('follow/<str:username>', views.follow_user, name="follow"),
    path('unfollow/<str:username>', views.unfollow_user, name="unfollow"),
    
]
