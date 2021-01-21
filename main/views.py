from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .models import Product, Comment, ProductImage
from .permisssions import ProductPermission, IsCommentAuthor
from .serializers import ProductSerializer, ProductDetailsSerializer, CreateProductSerializer, UpdateProductSerializer, \
    CommentSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = ProductFilter
    search_fields = ["title", ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [ProductPermission, ]
        return [permission() for permission in permissions]


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ProductPermission, ]
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [IsCommentAuthor, ]
        return [permission() for permission in permissions]

