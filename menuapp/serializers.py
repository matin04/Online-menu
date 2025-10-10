from rest_framework import serializers
from .models import User, Category, Dish, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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

