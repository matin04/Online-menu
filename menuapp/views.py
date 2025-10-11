from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import  logout
from rest_framework import viewsets, permissions
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    

class EmailConfirmView(APIView):
    def get(self, request, token):
        try:
            confirm = EmailConfirmation.objects.get(token = token)
            user = confirm.user
            user.is_active = True
            user.save()
            confirm.delete()
            return Response({'detail':'Email успешно подтвержден'}, status=status.HTTP_200_OK)
        except EmailConfirmation.DoesNotExist:
            return Response({'detail':'Неверный или устаревший токен'}, status=status.HTTP_400_BAD_REQUEST)



class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user) 
            refresh['email'] = user.email
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully!'}, status=200)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Review.objects.all()
        return Review.objects.filter(user=user)

