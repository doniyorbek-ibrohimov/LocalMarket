from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Banner, Category, Product, Image,
    Discount, Wishlist, Review, Cart, CartItem
)
from django.urls import reverse
from unfold.admin import ModelAdmin as UnfoldAdmin

class UnfoldTranslationAdmin(UnfoldAdmin):
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


# ---------------------
# Inline for product images
# ---------------------
class ProductImageInline(admin.StackedInline):
    model = Image
    extra = 1
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview')
    verbose_name = "Product image"
    verbose_name_plural = "Product images"

    def image_preview(self, obj):
        if obj and getattr(obj, "image", None):
            return format_html('<img src="{}" style="max-height:100px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


# ---------------------
# Banner admin
# ---------------------
@admin.register(Banner)
class BannerAdmin(UnfoldAdmin):
    list_display = ("id", "title", "created_at", "image_preview")
    search_fields = ("title",)
    readonly_fields = ("created_at", "image_preview")

    def image_preview(self, obj):
        if obj and getattr(obj, "image", None):
            return format_html('<img src="{}" style="max-height:80px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


# ---------------------
# Category admin
# ---------------------
@admin.register(Category)
class CategoryAdmin(UnfoldAdmin):
    list_display = ("id", "name", "banner_link", "created_at")
    search_fields = ("name",)
    list_filter = ("banner",)
    readonly_fields = ("created_at",)

    def banner_link(self, obj):
        if obj.banner:
            url = reverse('admin:product_banner_change', args=[obj.banner.pk])
            return format_html('<a href="{}">{}</a>', url, obj.banner.title)
        return "-"
    banner_link.short_description = "Banner"


# ---------------------
# Product admin
# ---------------------
@admin.register(Product)
class ProductAdmin(UnfoldAdmin):
    list_display = ("id", "name", "brand", "category", "price", "amount", "rating", "is_available", "created_at")
    list_filter = ("category", "brand", "is_available")
    search_fields = ("name", "brand", "description")
    inlines = [ProductImageInline]
    readonly_fields = ("created_at",)
    list_editable = ("is_available",)
    save_on_top = True
    fieldsets = (
        (None, {
            "fields": ("name", "brand", "description", "category", "is_available")
        }),
        ("Pricing & Stock", {
            "fields": ("price", "amount", "rating")
        }),
        ("Timestamps", {"fields": ("created_at",)}),
    )


# ---------------------
# Discount admin
# ---------------------
@admin.register(Discount)
class DiscountAdmin(UnfoldAdmin):
    list_display = ("id", "title", "product", "percentage", "active", "start_date", "end_date", "created_at")
    list_filter = ("active", "product")
    search_fields = ("title", "product__name")
    readonly_fields = ("created_at",)
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f"{updated} discounts activated.")
    make_active.short_description = "Mark selected discounts active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f"{updated} discounts deactivated.")
    make_inactive.short_description = "Mark selected discounts inactive"


# ---------------------
# Wishlist admin
# ---------------------
@admin.register(Wishlist)
class WishlistAdmin(UnfoldAdmin):
    list_display = ("id", "user", "product", "created_at")
    search_fields = ("user__username", "product__name")


# ---------------------
# Review admin
# ---------------------
@admin.register(Review)
class ReviewAdmin(UnfoldAdmin):
    list_display = ("id", "product", "user", "rating", "short_comment", "created_at")
    search_fields = ("product__name", "user__username", "comment")
    list_filter = ("rating",)

    def short_comment(self, obj):
        if obj.comment:
            return obj.comment[:60]
        return "-"
    short_comment.short_description = "Comment"


# ---------------------
# Cart & CartItem admin (inline)
# ---------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("total_price",)
    fields = ("product", "quantity", "total_price")


@admin.register(Cart)
class CartAdmin(UnfoldAdmin):
    list_display = ("id", "user", "created_at", "total_items", "total_value")
    search_fields = ("user__username",)
    inlines = [CartItemInline]
    readonly_fields = ("created_at",)

    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = "Items"

    def total_value(self, obj):
        return sum(i.total_price for i in obj.items.all())
    total_value.short_description = "Total value"



