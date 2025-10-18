from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from .models import Product, ProductRating
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import ProductRatingForm
from .models import Product, CartItem
from django.views import View


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
    
class ProductRateView(LoginRequiredMixin, FormView):
    template_name = 'store/rate_product.html'
    form_class = ProductRatingForm

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, id=kwargs['product_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            kwargs.update({'data': self.request.POST})
        user_rating = ProductRating.objects.filter(user=self.request.user, product=self.product).first()
        if user_rating:
            kwargs.update({'instance': user_rating})  
        return kwargs

    def form_valid(self, form):
        if ProductRating.objects.filter(user=self.request.user, product=self.product).exists():
            messages.warning(self.request, "You can only rate once.")
            return redirect('product_detail', pk=self.product.id)
        else:
            rating = form.save(commit=False)
            rating.user = self.request.user
            rating.product = self.product
            rating.save()
            messages.success(self.request, "Thank you for your rating!")
            return redirect('product_detail', pk=self.product.id)
        
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f"Added {product.name} to your cart!")
        return redirect('cart_detail')


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "store/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = CartItem.objects.filter(user=self.request.user)
        total = sum(item.get_total_price() for item in items)
        context['items'] = items
        context['total'] = total
        return context