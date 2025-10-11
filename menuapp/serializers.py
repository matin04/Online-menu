from rest_framework import serializers
from .models import CustomUser, Category, Dish, Review, CustomUser, EmailConfirmation
from django.core.mail import send_mail
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'is_admin']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    

class DishSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = 'category.name', read_only=True)
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'image', 'video', 'is_active', 'created_at']
    

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    dish_name = serializers.CharField(source='dish.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'dish', 'dish_name', 'text', 'created_at']






class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        confirm = EmailConfirmation.objects.create(user = user)
        self.send_email_confirmation(user.email, confirm.token)
        return user

    def send_email_confirmation(self, email, token):
        confirm_link = f"http://127.0.0.1:8000/confirm-email/{token}"
        send_mail(
            "Confirm your email",
        
            f"Click here to confirm: {confirm_link}",
        
            "fathuddinzodamatin@gmail.com",
        
            [email],
            )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("Email not confirmed")
        
        data['user'] = user
        return data
        

