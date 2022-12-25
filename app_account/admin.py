from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    LikedProduct,
    ProductRating,
    CartItem,
    Address,
    Order, IPAddress,
)


class LikedProductAdmin(admin.StackedInline):
    model = LikedProduct


class RatingAdmin(admin.StackedInline):
    model = ProductRating


class CartAdmin(admin.StackedInline):
    model = CartItem


class AddressAdmin(admin.StackedInline):
    model = Address


UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_superuser',
    'groups',
    'user_permissions'
)

UserAdmin.fieldsets[3][1]['fields'] = (
    'last_login',
    'date_joined',
)

admin.site.register(
    User,
    UserAdmin,
    inlines=[LikedProductAdmin, RatingAdmin, CartAdmin, AddressAdmin]
)

admin.site.register(
    Order,
    inlines=[CartAdmin]
)
admin.site.register(ProductRating)
admin.site.register(IPAddress)
