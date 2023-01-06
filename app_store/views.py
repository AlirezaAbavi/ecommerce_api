from django.http import Http404, JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as third_filters
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from app_account.models import LikedProduct, ProductRating, BrandRating
from app_store.filters import ProductFilter
from app_store.models import Product, Category, Brand, Comment, LikedComment
from app_store.serializers import ProductListSerializer, ProductSerializer, CommentSerializer


# Create your views here.
class ProductList(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [third_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', '=details__detail']
    ordering_fields = ['sell_price', 'created_at', 'total_rate', 'hits_count']
    ordering = ['hits_count']

    def get_queryset(self):
        req = self.request.get_full_path()
        if '/category/' in req:
            category = get_object_or_404(Category, slug=self.kwargs.get('slug'), status=True)
            queryset = Product.objects.filter(category=category, on_sell=True)
            for cat in category.get_descendants():
                tmp = Product.objects.filter(category=cat, on_sell=True)
                queryset = queryset | tmp
            return queryset
        elif '/brand/' in req:
            brand = get_object_or_404(Brand, slug=self.kwargs.get('slug'), status=True)
            queryset = Product.objects.filter(brand=brand, on_sell=True)
            return queryset
        else:
            raise Http404


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'product_id'

    def get_object(self):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, product_id=product_id, on_sell=True)
        ip_address = self.request.user.ip_address
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)
        product.save()
        return product


class ProductSearch(generics.ListAPIView):
    queryset = Product.objects.filter(status=True)
    serializer_class = ProductListSerializer
    filter_backends = [third_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'brand__title', '=details__detail']
    ordering_fields = ['sell_price', 'created_at', 'rate', 'hits']
    ordering = ['hits_count']


class ProductComment(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset = Comment.objects.filter(status='p', product__product_id=product_id)
        return queryset


@permission_classes([IsAuthenticated])
def rate(request: HttpRequest, id, rating: int):
    path = request.get_full_path()
    if '/product/' in path:
        product = get_object_or_404(Product, product_id=id)
        ProductRating.objects.filter(product=product, user=request.user).delete()
        product.rate.create(user=request.user, rating=rating)
        data = {'rating': product.product_rate()}
        product.save()
        return JsonResponse(data, status=status.HTTP_202_ACCEPTED)
    elif '/brand/' in path:
        brand = get_object_or_404(Brand, slug=id)
        BrandRating.objects.filter(brand=brand, user=request.user).delete()
        brand.rate.create(user=request.user, rating=rating)
        data = {'rating': brand.brand_rate()}
        brand.save()
        return JsonResponse(data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
def like_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    try:
        like = LikedProduct.objects.get(product__product_id=product_id, user=request.user)
        like.delete()
        return JsonResponse({'like': False})
    except:
        LikedProduct.objects.create(user=request.user, product=product)
        return JsonResponse({'like': True})


@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    try:
        like = LikedComment.objects.get(comment=comment, user=request.user)
        like.delete()
        return JsonResponse({'like': False})
    except:
        LikedComment.objects.create(user=request.user, comment=comment)
        return JsonResponse({'like': True})


@api_view(['GET'])
def get_subcategories(request, slug):
    try:
        category = get_object_or_404(Category, slug=slug, status=True)
        data = {}
        i = 1
        for cat in category.get_children():
            if cat.status:
                data.update({i: {
                    'title': cat.title,
                    'slug': cat.slug,
                    'url': request.build_absolute_uri(f'/api/store/category/{cat.slug}'),
                    'image': cat.image.url
                }})
                i += 1
        return JsonResponse(data)
    except:
        return Response(data=None, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_category_filters(request, cat):
    category = get_object_or_404(Category, slug=cat, status=True)
    data = {}
    filter = category.filters.all()
    for anc in category.get_ancestors():
        tmp = anc.filters.all()
        filter = filter | tmp
    for obj in category.filters.all():
        data.update({obj.title: {}})
        i = 1
        for choice in obj.choices.all():
            data[obj.title].update({i: {
                'title': choice.title,
                'kw': choice.kw
            }})
            i += 1
    return JsonResponse(data)
