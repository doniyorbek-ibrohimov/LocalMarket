from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldAdmin
from .models import *

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

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("total_price",)
    fields = ("product", "quantity", "total_price")

@admin.register(Order)
class OrderAdmin(UnfoldAdmin):
    list_display = ("id", "user", "status", "created_at", "overall_price_display")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "first_name", "last_name", "phone", "address")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at",)

    def overall_price_display(self, obj):
        return obj.overall_price
    overall_price_display.short_description = "Total"

