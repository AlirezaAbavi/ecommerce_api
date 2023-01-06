from django.urls import reverse
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

from app_account.models import ProductRating, LikedProduct
from app_store.models import (
    Product,
    Colors, Quantity, Detail, PostImage, LikedComment, Comment, Brand,
)


class ProductListSerializer(serializers.ModelSerializer):
    def get_colors(self, obj):
        colors = Colors.objects.filter(color__product=obj).values('title', 'code')
        new_colors = {}
        if colors:
            tmp = colors[0].get('code')
            i = 1
            for item in colors:
                if item.get('code') == tmp:
                    new_colors.update({i: {
                        'title': item.get('title'),
                        'code': tmp
                    }})
                    item.popitem()
                else:
                    tmp = item.get('code')
                    i += 1
                    new_colors.update({i: {
                        'title': item.get('title'),
                        'code': tmp
                    }})
                    item.popitem()
        return new_colors

    def get_product_rating(self, obj):
        return Product.product_rate(obj.id)

    def get_abs_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('store:detail', kwargs={'product_id': obj.product_id}))

    def get_brand(self, obj):
        request = self.context['request']
        return {
            'title': obj.brand.title,
            'url': request.build_absolute_uri(reverse('store:brand-list', kwargs={'slug': obj.brand.slug})),
        }

    brand = serializers.SerializerMethodField('get_brand')

    url = serializers.SerializerMethodField('get_abs_url')

    colors = serializers.SerializerMethodField('get_colors')

    rating = serializers.SerializerMethodField('get_product_rating')

    class Meta:
        model = Product
        fields = [
            'title',
            'url',
            'price',
            'sell_price',
            'rating',
            'status',
            'brand',
            'thumbnail',
            'colors'
        ]


class ProductSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    def get_product_rating(self, obj):
        return Product.product_rate(obj.id)

    def get_user_rating(self, obj):
        user = self.context['request'].user
        # if user.is_authenticated and ProductRating.objects.filter(user=user):
        try:
            user_rating = ProductRating.objects.get(user=user, product=obj).rating
            return user_rating
        except:
            return None

    def get_brand(self, obj):
        request = self.context['request']
        return {
            'title': obj.brand.title,
            'url': request.build_absolute_uri(reverse('store:brand-list', kwargs={'slug': obj.brand.slug})),
        }

    def get_categories(self, obj):
        request = self.context['request']
        data = {}
        i = 1
        for cat in obj.category.get_ancestors():
            data.update({i: {
                'title': cat.title,
                'url': request.build_absolute_uri(reverse('store:category-list', kwargs={'slug': cat.slug})),
            }})
            i += 1
        data.update({i: {
            'title': obj.category.title,
            'url': request.build_absolute_uri(reverse('store:category-list', kwargs={'slug': obj.category.slug})),
        }})
        return data

    def get_quantities(self, obj):
        quantities = Quantity.objects.filter(product=obj).values('color_id', 'color__title',
                                                                 'color__code', 'size__code',
                                                                 'quantity', 'status', 'id')
        if quantities:
            tmp = quantities[0].get('color_id')
            i = 1
            for item in quantities:
                if item.get('color_id') == tmp:
                    item["quantity_id"] = i
                    item.pop('color_id')
                else:
                    tmp = item.get('color_id')
                    i += 1
                    item["quantity_id"] = i
                    item.pop('color_id')
        return quantities

    def get_details(self, obj):
        details = Detail.objects.filter(product=obj).values('detail_title', 'detail',
                                                            'put_in_header')
        return details

    def get_images(self, obj):
        images = PostImage.objects.filter(product=obj).values('images')
        return images

    def is_product_liked(self, obj):
        user = self.context['request'].user
        try:
            like = LikedProduct.objects.get(product=obj, user=user)
            return True
        except:
            return False

    # def get_abs_url(self, obj):
    #     request = self.context['request']
    #     return request.build_absolute_uri(f'/brand/{obj.product_id}')

    quantities = serializers.SerializerMethodField('get_quantities')
    details = serializers.SerializerMethodField('get_details')
    images = serializers.SerializerMethodField('get_images')
    brand = serializers.SerializerMethodField('get_brand')
    user_rating = serializers.SerializerMethodField('get_user_rating')
    rating = serializers.SerializerMethodField('get_product_rating')
    categories = serializers.SerializerMethodField('get_categories')
    is_liked = serializers.SerializerMethodField('is_product_liked')

    class Meta:
        model = Product
        fields = [
            'product_id',
            'title',
            'is_liked',
            'price',
            'sell_price',
            'user_rating',
            'rating',
            'description',
            'status',
            'brand',
            'categories',
            'quantities',
            'details',
            'images',
            'hits_count',
        ]


class CommentSerializer(serializers.ModelSerializer):
    def get_likes(self, obj):
        return LikedComment.objects.filter(comment=obj).count()

    def is_comment_liked(self, obj):
        user = self.context['request'].user
        try:
            like = LikedComment.objects.get(comment=obj, user=user)
            return True
        except:
            return False

    def get_product(self, obj):
        return obj.product.product_id

    likes = serializers.SerializerMethodField('get_likes')
    is_liked = serializers.SerializerMethodField('is_comment_liked')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.SerializerMethodField('get_product')

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'product',
            'is_liked',
            'title',
            'body',
            'likes',
            'created_at',
        ]


class PopularBrandsSerializer(serializers.ModelSerializer):
    def get_abs_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('store:brand-list', kwargs={'slug': obj.slug}))

    url = serializers.SerializerMethodField('get_abs_url')

    class Meta:
        model = Brand
        fields = [
            'title'
            'image',
            'url',
        ]
