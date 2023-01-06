from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('cart/', views.Cart.as_view(), name='cart'),
    path('cart/add', views.AddToCart.as_view(), name='add-cart'),
    path('cart/<int:id>/', views.EditCart.as_view(), name='edit-cart'),
    path('order/', views.OrderList.as_view(), name='order'),
    path('order/submit', views.OrderCreate.as_view(), name='order-create'),
    path('order/<int:order_id>', views.OrderDetail.as_view(), name='order-details'),
    path('address/', views.AddressList.as_view(), name='address-list'),
    path('address/<int:id>/', views.AddressDetail.as_view(), name='address-detail'),
]
