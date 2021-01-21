from django.contrib.auth.models import User

from rest_framework import serializers
from cart.models import Orders, OrderItems
from main.models import Product


class ProductsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('product', 'quantity')


class OrderItemReprSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()

    class Meta:
        model = OrderItems
        fields = ('product', 'quantity')


class OrdersSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True, write_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Orders
        fields = '__all__'

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Orders.objects.create(**validated_data)
        for item in items:
            product = item['product']
            OrderItems.objects.create(order=order, product=product, quantity=item['quantity'])
        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = OrderItemReprSerializer(instance.items.all(), many=True).data
        return representation


class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'products')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }