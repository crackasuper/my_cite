from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'menu-items', views.MenuItemViewSet)
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'deliveries', views.DeliveryViewSet, basename='delivery')

urlpatterns = [
    path('', include(router.urls)),
] 