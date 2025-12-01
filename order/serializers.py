from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        read_only_fields = ['total_price']

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        total_price = product.discounted_price * quantity
        return OrderItem.objects.create(total_price=total_price, **validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']
        read_only_fields = ['total_price']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address', 'items', 'status']
        read_only_fields = ['status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            total_price = product.discounted_price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, total_price=total_price)
        return order


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    overall_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'first_name', 'last_name', 'phone', 'address',
            'status', 'created_at', 'overall_price', 'items'
        ]

    def get_overall_price(self, obj):
        return round(obj.overall_price, 2)
