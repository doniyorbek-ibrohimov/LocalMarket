from rest_framework import viewsets, generics, permissions, filters
from .filters import ProductFilter
from users.mixins import ReadOnlyOrIsAdminMixin
from users.permissions import IsAdmin


from .serializers import (
            BannerSerializer, CartSerializer,
            CategorySerializer, CategoryCreateSerializer,
            ProductSerializer, ProductCreateSerializer,
            DiscountSerializer, DiscountCreateSerializer,
            WishlistSerializer, WishlistCreateSerializer,
            ReviewSerializer, ReviewCreateSerializer,
            CartItemSerializer, CartItemCreateUpdateSerializer
)
from .models import (
            Banner, Category,Product, Discount,
            Wishlist, Review, Cart, CartItem,
)

class BannerViewSet(ReadOnlyOrIsAdminMixin, viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer




class CategoryViewSet(ReadOnlyOrIsAdminMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CategorySerializer
        return CategoryCreateSerializer



class ProductViewSet(ReadOnlyOrIsAdminMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand', 'category__name']
    ordering_fields = ['price', '-price', 'rating','-rating', 'created_at', '-created_at']
    filterset_class = ProductFilter
    ordering = ['-rating']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductSerializer
        return ProductCreateSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DiscountSerializer
        return DiscountCreateSerializer
    
class WishListViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return WishlistSerializer
        return WishlistCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReviewSerializer
        return ReviewCreateSerializer

class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartItemAddAPIView(generics.CreateAPIView):
    serializer_class = CartItemCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if getattr(self, 'swagger_fake_view', False):
            return context

        if not self.request.user.is_authenticated:
            return context

        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        return context

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        return CartItem.objects.filter(cart__user=self.request.user)


class CartItemUpdateAPIView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        return CartItem.objects.filter(cart__user=self.request.user)


class CartItemDeleteAPIView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        return CartItem.objects.filter(cart__user=self.request.user)



