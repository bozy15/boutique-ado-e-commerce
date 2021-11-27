from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product

# Create your views here.


def all_products(request):
    """A view to show all products, including sorting and search queries"""

    # Get all products
    products = Product.objects.all()
    # Sets query to empty value to prevent errors
    query = None

    # Search queries
    if request.GET:
        # Get the query from the URL
        # if theres no query, display error message
        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("products"))

            # Search by name and description
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # Filter the products by the search query
            products = products.filter(queries)
    context = {
        "products": products,
        "search_term": query,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to show individual product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/products_detail.html", context)
