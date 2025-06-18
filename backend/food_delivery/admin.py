from django.contrib import admin
from .models import Restaurant, Category, MenuItem, Order, OrderItem, Delivery

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    list_filter = ('restaurant',)
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at', 'restaurant')
    search_fields = ('user__username', 'restaurant__name')
    inlines = [OrderItemInline]

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_person', 'status', 'estimated_delivery_time', 'actual_delivery_time')
    list_filter = ('status', 'estimated_delivery_time')
    search_fields = ('order__user__username', 'delivery_person__username') 