from django.contrib import admin
from .models import Category, Product, ProductRating
from django.db.models import F

@admin.action(description="make discount True")
def make_discount_true(self, request, queryset):
        queryset.update(discount=True)

@admin.action(description="make discount False")
def make_discount_false(self, request, queryset):
        queryset.update(discount=False)

@admin.action(description="get price less 10 percent")
def minus_price(self, request, queryset):
        queryset.update(price=F('price') * 0.9)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount", "category", "image", 'rating', 'brand')
    actions = ('make_discount_true','make_discount_false', 'minus_price')
    search_fields = ('name', 'brand') 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description","image")
