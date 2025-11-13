from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify-signup/', views.verify_signup),
    path('login/', views.login_request),
    path('verify-login/', views.verify_login_otp),
    path('logout/', views.logout),
    path('resend-signup-otp/', views.resend_signup_otp),
    path('resend-login-otp/', views.resend_login_otp),
    path('forgot-password/', views.forgot_password_request),
    path('verify-reset-otp/', views.verify_reset_otp),
    path('reset-password/', views.reset_password),
]