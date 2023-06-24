from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login,logout

from API.models import *


class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    def get(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)




class RemoveStoreView(APIView):
    def post(self,request):
        if(request.user.type=='Trader'):
            adress=request.data.get('adress');
            try:
                store=Store.objects.get(adress=adress)
                store.is_available=False
                store.save()
                return Response({'message': 'Store successfuly removed'}, status=status.HTTP_200_OK)
            except:
                return Response({'message': 'Store not removed '}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'message': 'Store not removed '}, status=status.HTTP_404_NOT_FOUND)
