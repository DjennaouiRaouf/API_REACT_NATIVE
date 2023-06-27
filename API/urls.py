from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('remove_store/',RemoveStoreView.as_view()),
    path('signin/',SignInView.as_view()),
    path('changepwd/',ChangePWDView.as_view()),

    path('generateotp/', GenerateOTP.as_view()),
    path('verifyotp/', VerifyOTP.as_view()),





]