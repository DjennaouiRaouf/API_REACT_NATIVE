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


class SignInView(APIView):
    permission_classes = []
    def post(self,request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            userAccount = UserAccount.objects.create_user(username=username, password=password)
            userAccount.email="abc@gmail.com"
            userAccount.type="Trader"
            userAccount.save()

            return Response({'message': 'User account has been created successfuly'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'User account has not been created '}, status=status.HTTP_404_NOT_FOUND)



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
                return Response({'message': 'Store successfuly removed'}, status=status.HTTP_200_OK)
            except:
                return Response({'message': 'Store not removed '}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'message': 'Store not removed '}, status=status.HTTP_404_NOT_FOUND)
