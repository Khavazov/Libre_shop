from rest_framework import serializers

from .models import Product, Category, Comment, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'product')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user
        comment = Comment.objects.create(**validated_data)
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['author'] = UserSerializer(instance.author_id).data
        return representation


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'product.image', 'categories')

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class ProductDetailsSerializer(serializers.ModelSerializer):
    # some_field = serializers.CharField(write_only=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'categories')

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = self._get_image_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        representation['comment'] = CommentSerializer(instance.comment.all(), many=True).data
        return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', )


class CreateProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'categories', 'images')

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        print(images_data)
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'categories')
