from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .models import Category, Product
from .forms import ProductForm





class cegoryDetailView(DetailView):
    model = Category
    template_name = "store/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.object.products.all()
        return context

class productDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"

class discountedProductsView(ListView):
    model = Product
    template_name = "store/discounted_products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(discount=True)

class productCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_create.html"

    def get_success_url(self):
        return reverse("product_detail", args=[self.object.pk])

class productUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "store/update_product.html"
    context_object_name = "product"

    def get_success_url(self):
        return reverse("product_detail", args=[self.object.pk])

class productDeleteView(DeleteView):
    model = Product
    template_name = "store/delete_product.html"
    context_object_name = "product"
    success_url = reverse_lazy("home")


class home(ListView):
    model = Product
    template_name = "store/home.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if query:
            queryset = queryset.filter(name__icontains=query)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
