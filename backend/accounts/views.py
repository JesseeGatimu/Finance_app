from rest_framework.response import Response
from .serializers import LoginSerializer,RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

def get_token_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

class RegisterAPI(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            tokens=get_token_for_user(user)
            return Response({
                'message':'Registered Successfully',
                'tokens':tokens
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPI(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                tokens=get_token_for_user(user)
                return Response({
                    'message':'Login successful',
                    'tokens':tokens
                },status=status.HTTP_200_OK)
            return Response({
                'errors':'Invalid credentials'
            },status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)     
    
class LogoutAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            refresh_token=request.data['refresh']
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message':'Logout successful'
            },status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'errors':'Invalid tokens'
            },status=status.HTTP_400_BAD_REQUEST)