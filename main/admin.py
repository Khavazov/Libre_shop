from django.contrib import admin

from account.models import User
from .models import Category, Product, ProductImage, Comment


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', )


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

# class UserAdmin(admin.ModelAdmin):
#     list_display = ()

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
# admin.site.register(User)
admin.site.register(Comment)