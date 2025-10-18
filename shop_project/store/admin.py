from django.contrib import admin
from .models import Category, Product
from django.db import models


@admin.action(description='Apply 10 percent discount to selected products')
def apply_discount(modeladmin, request, queryset):
    for product in queryset:
        product.price = product.price * 0.9
        product.discount = True
        product.save()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount", "category", "image", 'rating')
    actions = [apply_discount]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
