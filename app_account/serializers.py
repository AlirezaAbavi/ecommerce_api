from django.urls import reverse
from rest_framework import serializers

from app_store.models import Product, Quantity
from .models import CartItem, Order, Address


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


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = [
            'user',
            'full_name',
            'country',
            'city',
            'address',
            'zip_code',
        ]


class OrderListSerializer(serializers.ModelSerializer):
    def get_thumbnails(self, obj):
        return CartItem.objects.filter(order=obj).values('product__thumbnail')

    def get_abs_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('user:order-details', kwargs={'order_id': obj.order_id}))

    order_id = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    number_of_products = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    url = serializers.SerializerMethodField('get_abs_url')
    thumbnails = serializers.SerializerMethodField('get_thumbnails')

    class Meta:
        model = Order
        fields = [
            'order_id',
            'number_of_products',
            'total_price',
            'created_at',
            'status',
            'url',
            'thumbnails',
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'user',
            'address',
        ]

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        items = CartItem.objects.filter(user=order.user)
        for item in items:
            item.user = None
            item.order = order
            item.save()
        order.save()
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    def get_items(self, obj):
        items = CartItem.objects.filter(order=obj)
        request = self.context['request']
        data = {}
        i = 1
        for item in items:
            data.update({i: {
                'title': item.product.title,
                'total_price': item.price,
                'number': item.number,
                'brand': item.product.brand.title,
                'url': request.build_absolute_uri(
                    reverse('store:detail', kwargs={'product_id': obj.product.product_id})),
                'quantity': {
                    'color_title': item.quantity.color.title,
                    'color_code': item.quantity.color.code,
                    'size': item.quantity.size.title
                }
            }})
            i += 1
        return data

    order_id = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    number_of_products = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    address = AddressSerializer()
    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Order

        fields = [
            'order_id',
            'number_of_products',
            'total_price',
            'created_at',
            'status',
            'address',
            'items',
        ]
