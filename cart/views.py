from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from cart.models import Orders
from main.models import Product
from cart.serializers import ProductsSerializer, OrdersSerializer
from cart.serializers import UserSerializer
from cart.permissions import IsOwnerOrReadOnly
from cart.permissions import IsStaffOrTargetUser

User = get_user_model()


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-title')
    serializer_class = ProductsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all().order_by('-id')
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return (permissions.AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()),

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_update(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)