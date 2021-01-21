from django.db import models

from account.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, primary_key=True)
    parent = models.ForeignKey('self',
                               related_name='children',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', null=True, blank=True)


class Cart(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    text = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # return self.author
        return f"{self.author}: {self.text}"
