from django.contrib import admin
from .models import Category, Product

@admin.action(description="Apply 10% discount on selected products")
def apply_discount(modeladmin, request, queryset):
    for product in queryset:
        product.price = product.price * 0.9
        product.save()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount", "category")
    actions = [apply_discount]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
