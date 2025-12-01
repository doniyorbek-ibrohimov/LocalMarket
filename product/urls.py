from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (BannerViewSet ,CategoryViewSet,
                    ProductViewSet, DiscountViewSet,
                    WishListViewSet, ReviewViewSet,
                    CartAPIView, CartItemAddAPIView,
                    CartItemUpdateAPIView, CartItemDeleteAPIView,
                    )

router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'discounts', DiscountViewSet, basename='discount')
router.register(r'wishlists', WishListViewSet, basename='wishlist')
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = router.urls
urlpatterns += [
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cart/items/add/', CartItemAddAPIView.as_view(), name='cart-item-add'),
    path('cart/items/<int:pk>/update/', CartItemUpdateAPIView.as_view(), name='cart-item-update'),
    path('cart/items/<int:pk>/delete/', CartItemDeleteAPIView.as_view(), name='cart-item-delete'),
]