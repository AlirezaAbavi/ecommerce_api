from django.urls import reverse
from rest_framework import serializers

from app_store.models import Product, Quantity
from .models import CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'sell_price',
            'thumbnail',
            'brand',
        ]


#
#
class CartSerializer(serializers.ModelSerializer):
    def get_quantity(self, obj):
        q = Quantity.objects.get(id=obj.quantity.id)
        return {
            'color_title': q.color.title,
            'color_code': q.color.code,
            'size_code': q.size.code
        }

    def get_brand(self, obj):
        return obj.product.brand.title

    def get_abs_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('store:detail', kwargs={'product_id': obj.product.product_id}))

    product = ProductSerializer()

    quantity = serializers.SerializerMethodField('get_quantity')

    brand = serializers.SerializerMethodField('get_brand')

    url = serializers.SerializerMethodField('get_abs_url')

    class Meta:
        model = CartItem
        fields = [
            'product',
            'quantity',
            'number',
            'brand',
            'url',
        ]


class CreateItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartItem
        fields = [
            'user',
            'product',
            'quantity',
        ]

    def create(self, validated_data):
        try:
            item = CartItem.objects.get(**validated_data)
            item.number += 1
            item.save()
            return item
        except CartItem.DoesNotExist:
            return CartItem.objects.create(**validated_data)


class EditItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['number']
