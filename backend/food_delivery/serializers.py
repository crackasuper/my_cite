from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant, Category, MenuItem, Order, OrderItem, Delivery

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    restaurant_name = serializers.CharField(source='category.restaurant.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        write_only=True,
        source='restaurant'
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'status', 'total_amount')

class DeliverySerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    delivery_person = UserSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ('order', 'delivery_person', 'actual_delivery_time') 