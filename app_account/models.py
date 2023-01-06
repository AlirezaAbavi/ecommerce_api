from random import randint

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()
    created = models.DateTimeField(default=timezone.now, editable=False)


class LikedProduct(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='liked_product')
    product = models.ForeignKey('app_store.Product', default=None, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now=True, editable=False)


class ProductRating(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='product_rating')
    product = models.ForeignKey('app_store.Product', default=None, on_delete=models.CASCADE, related_name='rate')
    rating = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)],
                                      help_text='A number between 0 - 5')


class BrandRating(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='brand_rating')
    brand = models.ForeignKey('app_store.Brand', default=None, on_delete=models.CASCADE, related_name='rate')
    rating = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(5), MinValueValidator(0)], help_text='A number between 0 - 5'
    )

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=500)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    order_id = models.IntegerField(unique=True, blank=True, null=True)
    number_of_products = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1, blank=False)
    total_price = models.FloatField(null=True, validators=[MinValueValidator(0.0)])
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    STATUS_CHOICES = (
        (0, 'Waiting for payment'),
        (1, "Processing"),
        (3, "Shipped"),
        (4, "Received by costumer"),
    )
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)

    def save(self, **kwargs):
        if not self.total_price:
            self.total_price = CartItem.objects.filter(order=self).aggregate(price=Sum("product__sell_price"))[
                                   "price"] or 0

        if not self.number_of_products:
            self.number_of_products = CartItem.objects.filter(order=self).aggregate(
                number=Sum("number"))["number"] or 0

        if not self.order_id:
            while True:
                id = randint(10000, 99999)
                p = Order.objects.filter(order_id=id)
                if not p:
                    self.order_id = id
                    return super(Order, self).save(**kwargs)
                else:
                    continue
        else:
            return super(Order, self).save(**kwargs)


class CartItem(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True, related_name='items')
    order = models.ForeignKey(Order, default=None, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='items')
    product = models.ForeignKey('app_store.Product', to_field='product_id', on_delete=models.CASCADE, default=None)
    quantity = models.ForeignKey('app_store.Quantity', on_delete=models.SET_NULL, null=True)
    number = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def cart_price(self) -> float:
        return CartItem.objects.filter(user=self.user).aggregate(price=Sum("product__sell_price"))["price"] or 0
