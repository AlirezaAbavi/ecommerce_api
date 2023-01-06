# Generated by Django 4.1.4 on 2023-01-06 22:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('app_account', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrating',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='rate',
                                    to='app_store.product'),
        ),
        migrations.AddField(
            model_name='productrating',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='product_rating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_account.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='likedproduct',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_store.product'),
        ),
        migrations.AddField(
            model_name='likedproduct',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='liked_product', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='order',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='items', to='app_account.order'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_store.product',
                                    to_field='product_id'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='quantity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_store.quantity'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brandrating',
            name='brand',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='rate',
                                    to='app_store.brand'),
        ),
        migrations.AddField(
            model_name='brandrating',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='brand_rating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True,
                                         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                         related_name='user_set', related_query_name='user', to='auth.group',
                                         verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                         related_name='user_set', related_query_name='user', to='auth.permission',
                                         verbose_name='user permissions'),
        ),
    ]