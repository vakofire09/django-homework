from .models import Product

def latest_products(request):
    return {
        "latest_products": Product.objects.order_by("-id")[:5]
    }
