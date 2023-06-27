import pyotp as pyotp
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login,logout


from API.models import *

'''
login
This method is going to return a response
Which contains user id and user type

'''
class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return Response({'message': 'Login successful','uid':str(user.user_id),'type':str(user.type)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


'''
logout
'''

class LogoutView(APIView):

    def get(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


'''
Sign in
'''
class SignInView(APIView):
    permission_classes = []
    def post(self,request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            type = request.data.get('type')
            phone_number = request.data.get('phone_number')

            userAccount = UserAccount.objects.create_user(username=username, password=password)

            userAccount.email=email
            userAccount.first_name=first_name
            userAccount.last_name=last_name
            userAccount.type=type
            userAccount.phone_number=phone_number

            userAccount.save()

            return Response({'message': 'User account has been created successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'User account has not been created '}, status=status.HTTP_404_NOT_FOUND)


'''
Change password
'''
class ChangePWDView(APIView):
    def post(self,request):
        password = request.data.get('password')
        user = UserAccount.objects.get(username=request.user.username)
        user.set_password(password)
        user.save()
        return Response({'message': 'Password successfully changed'}, status=status.HTTP_200_OK)

'''
Remove Store By id 
(We are not removing the store from the database we are going to set the flag is_available to false)
'''

class GenerateOTP(APIView):
    def post(self, request):
        user = UserAccount.objects.get(username=request.user.username)
        if user != None:
            otp_base32 = pyotp.random_base32()
            otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=request.user.username.lower(), issuer_name="codepython.com")
            user.otp_auth_url = otp_auth_url
            user.otp_base32 = otp_base32
            user.save()
            return Response({'base32': otp_base32, "otpauth_url": otp_auth_url})
        else:
            return Response({'message': 'User account not found '}, status=status.HTTP_404_NOT_FOUND)


class VerifyOTP(APIView):
    def post(self, request):
        otp_token = request.data.get('token', None)
        user = UserAccount.objects.get(username=request.user.username)
        if user != None:
            totp = pyotp.TOTP(user.otp_base32)
            if not totp.verify(otp_token):
                return Response({'message': 'Token is invalid or user doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)
            user.otp_enabled = True
            user.otp_verified = True
            user.save()
            return Response({'otp_verified': True})

        else:
            return Response({'message': 'User account not found '}, status=status.HTTP_404_NOT_FOUND)


class RemoveStoreView(APIView):
    def post(self,request):
        if(request.user.type=='Trader'):
            store_id=request.data.get('store_id');
            try:
                store=Store.objects.get(store_id=store_id)
                store.is_available=False
                store.save()
                return Response({'message': 'Store successfully removed'}, status=status.HTTP_200_OK)
            except:
                return Response({'message': 'Store not removed '}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'message': 'Store not removed '}, status=status.HTTP_404_NOT_FOUND)
