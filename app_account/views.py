import datetime

from django.conf import settings
from django.http import HttpResponseForbidden
from pytz import utc
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from app_account.models import CartItem, Order, Address
from app_account.serializers import CartSerializer, CreateItemSerializer, EditItemSerializer, OrderListSerializer, \
    OrderCreateSerializer, OrderDetailSerializer, AddressSerializer


# Create your views here.
class Cart(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CartItem.objects.filter(user=self.request.user).order_by('created_at')
        return queryset


class AddToCart(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CreateItemSerializer
    permission_classes = [IsAuthenticated]


class EditCart(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EditItemSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = CartItem.objects.filter(user=self.request.user)
        return queryset


class OrderList(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        for order in orders:
            if order.status == 0:
                diff = now - order.created_at
                if diff.seconds >= settings.ORDER_EXPIRY_TIME:
                    order.delete()
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class OrderCreate(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if CartItem.objects.filter(user=self.request.user).count() > 0:
            queryset = Order.objects.filter(user=self.request.user)
            return queryset
        else:
            raise HttpResponseForbidden


class AddressList(generics.ListCreateAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        queryset = Address.objects.filter(user=self.request.user)
        return queryset


class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    lookup_field = 'id'


class OrderDetail(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_id'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset
