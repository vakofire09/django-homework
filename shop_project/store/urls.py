from django.urls import path
from .views import (
    home, cegoryDetailView, productDetailView,
    discountedProductsView, productCreateView,
    productUpdateView, productDeleteView, ProductRateView, 
    AddToCartView, CartDetailView
)

urlpatterns = [
    path("", home.as_view(), name="home"),
    path("category/<int:pk>/", cegoryDetailView.as_view(), name="category_detail"),
    path("discounts/", discountedProductsView.as_view(), name="discounted_products"),
    path("product/<int:pk>/", productDetailView.as_view(), name="product_detail"),
    path("product/<int:pk>/update/", productUpdateView.as_view(), name="update_product"),
    path("product/<int:pk>/delete/", productDeleteView.as_view(), name="delete_product"),
    path("product/add/", productCreateView.as_view(), name="product_create"),
    path('product/<int:product_id>/rate/', ProductRateView.as_view(), name='rate_product'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
]
