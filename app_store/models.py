from random import randint

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, Avg
from django.utils.html import format_html
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from app_account.models import User, BrandRating, IPAddress, ProductRating


# Create your models here.
class Category(MPTTModel):
    title = models.CharField(max_length=100, blank=False, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=100, editable=True, blank=False, unique=True, default=None)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/categories', null=True, blank=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Brand(models.Model):
    title = models.CharField(max_length=100, blank=False, null=True)
    slug = models.SlugField(max_length=100, editable=True, blank=False, unique=True, default='')
    total_rate = models.FloatField(default=0.0)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/brands', null=True, blank=True)

    def brand_rate(self) -> float:
        return BrandRating.objects.filter(brand=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def save(self, **kwargs):
        self.total_rate = self.brand_rate()
        return super(Brand, self).save(**kwargs)

    def __str__(self):
        return self.title


class Colors(models.Model):
    title = models.CharField(max_length=20, blank=False, null=True)
    code = models.CharField(max_length=7, blank=False, null=False)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.title


class Sizes(models.Model):
    title = models.CharField(max_length=20, blank=False, null=True)
    category = models.ManyToManyField(Category, related_name='Sizes')
    code = models.CharField(max_length=7, blank=False, null=False)

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, blank=False)
    product_id = models.IntegerField(null=True, blank=True, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=False, related_name='products')
    price = models.FloatField(default=0.00, validators=[MinValueValidator(0.0)])
    sell_price = models.FloatField(default=0.00, validators=[MinValueValidator(0.0)])
    total_rate = models.FloatField(default=0.00)
    hits = models.ManyToManyField(IPAddress, through='ProductHit', related_name='hits')
    hits_count = models.PositiveIntegerField(default=0, blank=True)
    total_quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=1, blank=False)
    on_sell = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='images/products', blank=False, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    STATUS_CHOICES = (
        (1, 'In Stock'),  # In Stock
        (2, "Coming Soon"),  # Coming Soon
        (3, "Out of Stock"),  # Out of Stock
    )
    status = models.IntegerField(null=True, blank=True, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['-status']

    def product_rate(self) -> float:
        return ProductRating.objects.filter(product=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def save(self, **kwargs):
        self.total_rate = self.product_rate()
        try:
            self.hits_count = self.hits.count()
        except:
            self.hits_count = 0
        self.total_quantity = Quantity.objects.filter(product=self).aggregate(Sum('quantity'))['quantity__sum'] or 0
        if not self.status == 2:
            if self.total_quantity == 0:
                self.status = 3
            else:
                self.status = 1
        if not self.product_id:
            while True:
                p_id = randint(10000, 99999)
                p = Product.objects.filter(product_id=p_id)
                if not p:
                    self.product_id = p_id
                    return super(Product, self).save(**kwargs)
                else:
                    continue
        else:
            return super(Product, self).save(**kwargs)

    def category_to_str(self):
        return ", ".join([category.title for category in self.category.get_family()])

    category_to_str.short_description = "Category"

    def thumbnail_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.thumbnail.url))

    thumbnail_tag.short_description = "thumbnail"

    def __str__(self):
        return self.title


class PostImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='images')
    images = models.FileField(upload_to='images/products')


class Quantity(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='quantities')
    color = models.ForeignKey(Colors, default=None, null=True, on_delete=models.SET_NULL, related_name="color")
    size = models.ForeignKey(Sizes, null=True, on_delete=models.SET_NULL, related_name='size')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=1, blank=False)
    STATUS_CHOICES = (
        (1, 'In Stock'),  # In Stock
        (2, "Coming Soon"),  # Coming Soon
        (3, "Out of Stock"),  # Out of Stock
    )
    status = models.IntegerField(null=True, blank=True, choices=STATUS_CHOICES)

    def save(self, **kwargs):
        if not self.status == 2:
            if self.quantity == 0:
                self.status = 3
            else:
                self.status = 1
        return super(Quantity, self).save(**kwargs)

    class Meta:
        verbose_name = 'Quantity'
        verbose_name_plural = 'Quantities'


class Detail(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='details')
    detail_title = models.CharField(max_length=100)
    detail = models.CharField(max_length=250)
    put_in_header = models.BooleanField(default=False)


class Comment(models.Model):
    STATUS_CHOICES = (
        ('p', "Publish"),  # publish
        ('r', "Reviewing"),  # in review
        ('b', "Denied(Delete comment)"),  # back
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=1000, null=False, blank=False)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='r')

    class Meta:
        ordering = ['-product']

    def __str__(self):
        return self.body[:50]


class LikedComment(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='liked_comment')
    comment = models.ForeignKey(Comment, default=None, on_delete=models.CASCADE, related_name='likes')
    added_at = models.DateTimeField(auto_now=True, editable=False)


class CategoryFilter(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='filters')
    title = models.CharField(max_length=100)


class FilterChoice(models.Model):
    filter = models.ForeignKey(CategoryFilter, on_delete=models.CASCADE, related_name='choices')
    title = models.CharField(max_length=100)
    kw = models.CharField(max_length=200)


class ProductHit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
