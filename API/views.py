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
        token = request.data.get('token')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.otp_enabled == False :
                login(request,user)
            if user.otp_enabled == True :
                totp = pyotp.TOTP(user.otp_base32)
                if totp.verify(token):
                    login(request,user)
                else:
                    return Response({'message': 'Token is invalid or user doesn\'t exist'},
                                    status=status.HTTP_400_BAD_REQUEST)


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
            enable2FA=request.data.get('enable2FA')
            UserAccount.objects.create_user(username=username, password=password,
                                                          email=email,type=type,
                                                          phone_number=phone_number,
                                            first_name=first_name,last_name=last_name)
            if enable2FA == "True":
                userAccount = UserAccount.objects.get(username=username)
                otp_base32 = pyotp.random_base32()
                otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
                    name=username, issuer_name="codepython.com")
                userAccount.otp_auth_url = otp_auth_url
                userAccount.otp_base32 = otp_base32
                userAccount.otp_enabled = True
                userAccount.save()

            return Response({'message': 'User account has been created successfully','base32': otp_base32, 'otpauth_url': otp_auth_url}, status=status.HTTP_200_OK)
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
