from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('remove_store/',RemoveStoreView.as_view()),
    path('signin/',SignInView.as_view()),
    path('changepwd/',ChangePWDView.as_view()),

    path('otp/generate', GenerateOTP.as_view()),
    path('otp/verify', VerifyOTP.as_view()),
    path('otp/validate', ValidateOTP.as_view()),
    path('otp/disable', DisableOTP.as_view()),




]