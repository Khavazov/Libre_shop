from django.db import models
from django.conf import settings

from main.models import Product


class Orders(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(max_length=30, default='')
    payment_method = models.CharField(max_length=30, default='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)