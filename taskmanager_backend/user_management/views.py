from rest_framework.generics import GenericAPIView
from . import serializers
from rest_framework import status
from rest_framework.response import Response
from . import models
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login
# Create your views here.



class UserAuth(GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        if "register" in request.path:
            return self.registration(request)
        else:
            return self.login(request)
        

    # registration for staff
    def registration(self, request, *args, **kwargs):

        try:
            serializer = serializers.UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response({"message": "Registered a user"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def login(self, request, *args, **kwargs):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                refresh_token = RefreshToken.for_user(user)
                access_token = refresh_token.access_token
                return Response({
                    "message": "Logged in",
                    "refresh_token": str(refresh_token),
                    "access_token": str(access_token),
                    "username":request.user.username
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Wrong password"}, status=status.HTTP_404_NOT_FOUND)
        except models.userModel.DoesNotExist:
            return Response({"message": "Register as a user to login"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)