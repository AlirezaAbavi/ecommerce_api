from django.urls import path

from app_store import views

app_name = 'store'
urlpatterns = [
    path('category/<slug:slug>/', views.ProductList.as_view(), name='category-list'),
    path('brand/<slug:slug>/', views.ProductList.as_view(), name='brand-list'),
    path('product/<int:product_id>/', views.ProductDetail.as_view(), name='detail'),

]
