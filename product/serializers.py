from rest_framework import serializers
from .models import (
                    Banner, Category, Product,
                    Discount, Image, Wishlist,
                    Review, Cart, CartItem,
)


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image']


class CategorySerializer(serializers.ModelSerializer):
    banner = BannerSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'banner']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'banner']


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'title', 'start_date', 'end_date', 'is_active']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    active_discount = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True, source='image_set')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'description', 'price', 'discounted_price',
            'active_discount', 'amount', 'rating', 'is_available', 'category', 'images','created_at'
        ]

    def get_active_discount(self, obj):
        discount = obj.get_active_discount()
        return ProductDiscountSerializer(discount).data if discount else None

    def get_discounted_price(self, obj):
        return obj.get_discounted_price




class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'description',
                  'price', 'amount', 'rating',
                  'is_available', 'category'
                  ]

class DiscountSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Discount
        fields = ['id', 'title', 'product', 'start_date', 'end_date', 'active']

class DiscountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['title', 'product', 'start_date', 'end_date', 'active']

class ImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'product', 'image']



class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['product', 'image']



class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product']


class WishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['user', 'product']


class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'product', 'rating', 'comment']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']


class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def create(self, validated_data):
        cart = self.context['cart']
        product = self.context['product']

        item, created = CartItem.objects.get_or_create(
            cart = cart,
            product = product,
            defaults={'quantity': validated_data['quantity']}
        )

        if not created:
            item.quantity += validated_data['quantity']
            item.save()
        return item








