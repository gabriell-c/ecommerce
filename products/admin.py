from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product, ProductImage, Rating


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductReviewInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "price", "stock", "active", "created_at")
    list_filter = ("active", "category")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductReviewInline]


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ProductImage)
admin.site.register(Rating)
