from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views
from .views import reset_password_view, send_mail_view,confirm_code_view

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_view,name='logout'),
    
    path("account/", views.account, name="account"),
    # path('insert/',views.insert_email,name='insert'),

    # path('reset_password',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),
    
    
    path("reset_password/<str:token>/", reset_password_view, name="reset_password"),
    path("confirm_code/<uuid:token>/", confirm_code_view, name="confirm_code"),
    path('send_mail/', views.send_mail_view, name='send_mail'),
    path('profile/', views.profile, name='profil'),
]
