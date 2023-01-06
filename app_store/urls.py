from django.urls import path

from app_store import views

app_name = 'store'
urlpatterns = [
    path('', views.ProductSearch.as_view(), name='search'),
    path('category/<slug:slug>/', views.ProductList.as_view(), name='category-list'),
    path('brand/<slug:slug>/', views.ProductList.as_view(), name='brand-list'),
    path('product/<int:product_id>/', views.ProductDetail.as_view(), name='detail'),
    path('comment/<int:product_id>/', views.ProductComment.as_view(), name='comments'),
    path('product/rate/<int:id>/<int:rating>/', views.rate, name='product-rate'),
    path('brand/rate/<slug:id>/<int:rating>/', views.rate, name='brand-rate'),
    path('comment/like/<int:comment_id>/', views.like_comment, name='like-comment'),
    path('product/like/<int:product_id>/', views.like_product, name='like-product'),
    path('subcat/<slug:slug>/', views.get_subcategories, name='sub-categories'),
    path('filters/<slug:cat>/', views.get_category_filters, name='sub-category-filters'),
]
