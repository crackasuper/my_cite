from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Restaurant, Category, MenuItem, Order, OrderItem, Delivery
from .serializers import (
    RestaurantSerializer, CategorySerializer, MenuItemSerializer,
    OrderSerializer, OrderItemSerializer, DeliverySerializer
)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def menu(self, request, pk=None):
        restaurant = self.get_object()
        menu_items = MenuItem.objects.filter(category__restaurant=restaurant)
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        order = self.get_object()
        menu_item_id = request.data.get('menu_item_id')
        quantity = request.data.get('quantity', 1)
        notes = request.data.get('notes', '')

        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        
        order_item = OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=quantity,
            price=menu_item.price,
            notes=notes
        )

        # Update order total
        order.total_amount = sum(item.price * item.quantity for item in order.items.all())
        order.save()

        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        # If order is ready for delivery, create delivery record
        if new_status == 'ready':
            Delivery.objects.create(
                order=order,
                estimated_delivery_time=request.data.get('estimated_delivery_time')
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)

class DeliveryViewSet(viewsets.ModelViewSet):
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Delivery.objects.all()
        return Delivery.objects.filter(delivery_person=user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        delivery = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        delivery.status = new_status
        if new_status == 'delivered':
            delivery.actual_delivery_time = request.data.get('actual_delivery_time')
        delivery.save()

        # Update order status
        delivery.order.status = new_status
        delivery.order.save()

        serializer = DeliverySerializer(delivery)
        return Response(serializer.data) 