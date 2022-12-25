from django.urls import reverse
from rest_framework import serializers

from app_store.models import (
    Product,
    Colors,
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
