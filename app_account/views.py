from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from app_account.models import CartItem
from app_account.serializers import CartSerializer, CreateItemSerializer, EditItemSerializer


# Create your views here.
class Cart(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CartItem.objects.filter(user=self.request.user)
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
