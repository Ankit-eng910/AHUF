from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * # CategoryViewSet, SubCategoryViewSet, MenuItemViewSet





urlpatterns = [

    path('tables/', TableListCreateAPIView.as_view(), name='table-list-create'),
    path('tables/<int:pk>/status/', TableStatusAPIView.as_view(), name='table-status-update'),
    path('booking/', BookingListCreateAPIView.as_view(),name='booking'),
    path('add-to-cart/', AddToCartAPIView.as_view(),name='add-to-cart'),
    path('cart/update/', UpdateCartItemAPIView.as_view(),name='cart-update'),
    path('cart/delete/', DeleteCartItemAPIView.as_view(),name='cart-delete'),
    path('confirm-booking/', ConfirmBookingAPIView.as_view(),name='confirm-booking'),
    path('menu-item/', getmenudata.as_view(), name='menu-detail'),
    path('cart/<int:booking_id>/', CartDetailAPIView.as_view(),name='cart-id-details'),
    path('pay-and-generate-bill/', PaymentAndGenerateBillAPIView.as_view(), name='pay-generate-bill'),
    path('bill/<int:pk>/', BillDetailAPIView.as_view(), name='bill-detail'),
    path('recent-orders/', RecentUnpaidOrdersAPIView.as_view(), name='recent-orders'),
]