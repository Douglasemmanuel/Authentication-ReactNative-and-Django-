#from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from account.renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.

#Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)

    return{
        'refresh':str(refresh),
        'access':str(access),
        # 'access': str(refresh.access_token),
    }


#we create a user registration view for the jwt registration view
class UserRegistrationView(APIView):
    renderer_classes =  [UserRenderer]
    def post(self,request,format=None):
            serializer = UserRegistrationSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
            serializer.is_valid(raise_exception=True)
            user = serializer.save() 
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Sucess'},
            status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        # return Response(serializer.errors,
        # status=status.HTTP_400_BAD_REQUEST)


#we create a user login view for the jwt registration view
class UserLoginView(APIView):
    renderer_classes =  [UserRenderer]
    def post (self,request,format=None):
            serializer = UserLoginSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
            serializer.is_valid(raise_exception=True)
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email , password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Sucess'},
                status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}},
                status=status.HTTP_404_NOT_FOUND)
        # return Response(serializer.errors , 
        # status=status.HTTP_400_BAD_REQUEST)


#we create a user profile view for the user to view their profile
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data , status=status.HTTP_200_OK)


#we create a user changepassword view for the user to change their password
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data,
        context={'user':request.user})
        # if  serializer.is_valid(raise_exception=True):
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Sucesfully'},
        status=status.HTTP_200_OK)
        # return Response(serializer.errors , 
        # status=status.HTTP_400_BAD_REQUEST)


#we create a user sendpasswordResetEmail view for the user to get their resetpasswordverification through their email
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None): 
        serializer = SendPasswordResetEmailSerializer(data=request.data)    
        # if  serializer.is_valid(raise_exception=True):
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Link Sent. Please check your Email'},
        status=status.HTTP_200_OK)
        # return Response(serializer.errors , 
        # status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format=None): 
        serializer = UserPasswordResetSerializer(data=request.data,
        context={'uid':uid,'token':token})
        # if  serializer.is_valid(raise_exception=True):
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Sucessfully'},
        status=status.HTTP_200_OK)
        # return Response(serializer.errors , 
        # status=status.HTTP_400_BAD_REQUEST)    

