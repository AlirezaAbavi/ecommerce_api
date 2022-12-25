from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import (
    Category,
    Brand,
    Product,
    PostImage,
    Quantity,
    Colors,
    Sizes,
    Detail,
    Comment,
    LikedComment,
    FilterChoice,
    CategoryFilter,
)

# Admin header change
admin.site.site_header = "e-commerce website"


# Register your models here.

def make_on_sell(modeladmin, request, queryset):
    rows_updated = queryset.update(on_sell=True)
    message_bit = "Added to OnSell"
    modeladmin.message_user(request, "{} products {}".format(rows_updated, message_bit))

    make_on_sell.short_description = "Add selected products to OnSell"


def make_off_sell(modeladmin, request, queryset):
    rows_updated = queryset.update(on_sell=False)
    message_bit = "Removed from OnSell"
    modeladmin.message_user(request, "{} products {}".format(rows_updated, message_bit))
    make_off_sell.short_description = "Remove selected products to OnSell"


def publish_comment(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    message_bit = "Published"
    modeladmin.message_user(request, "{} comments {}".format(rows_updated, message_bit))
    make_on_sell.short_description = "Publish selected comments"


def review_comment(modeladmin, request, queryset):
    rows_updated = queryset.update(status='r')
    message_bit = "are ready to review"
    modeladmin.message_user(request, "{} comments {}".format(rows_updated, message_bit))

    make_off_sell.short_description = "Review selected comments"


class DetailAdmin(admin.StackedInline):
    model = Detail


class PostImageAdmin(admin.StackedInline):
    model = PostImage


class QuantityAdmin(admin.StackedInline):
    model = Quantity


class ProductAdmin(admin.ModelAdmin):
    inlines = [DetailAdmin, QuantityAdmin, PostImageAdmin]
    list_display = (
        'thumbnail_tag', 'title', 'product_id', 'brand', 'sell_price', 'product_rate', 'total_quantity', 'on_sell',
        'category_to_str')
    list_filter = ('brand', 'status', 'on_sell')
    search_fields = ('title', 'description')
    ordering = ['-status', '-created_at']
    actions = [make_on_sell, make_off_sell]


admin.site.register(Product, ProductAdmin)


class CategoryFilterAdmin(admin.StackedInline):
    model = CategoryFilter


class FilterChoiceAdmin(admin.StackedInline):
    model = FilterChoice


admin.site.register(
    CategoryFilter,
    inlines=[FilterChoiceAdmin],
)

admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'slug',
        'status',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
    inlines=[CategoryFilterAdmin],
    list_filter=(['status']),
    search_fields=('title', 'slug'),
    prepopulated_fields={'slug': ('title',)},
)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class LikedCommentAdmin(admin.StackedInline):
    model = LikedComment


admin.site.register(Brand, BrandAdmin)
admin.site.register(Colors)
admin.site.register(Sizes)
admin.site.register(
    Comment,
    inlines=[LikedCommentAdmin],
    list_display=('title', 'product', 'user'),
    actions=[publish_comment, review_comment]
)
