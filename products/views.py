from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product

# Create your views here.


def all_products(request):
    """A view to show all products, including sorting and search queries"""

    # Get all products
    products = Product.objects.all()

    query = None  # Sets query to empty value to prevent errors
    categories = None  # Sets category to empty value to prevent errors
    sort = None  # Sets sort to empty value to prevent errors
    direction = None  # Sets direction to empty value to prevent errors

    # Search queries
    if request.GET:
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("name"))
            if sortkey == "category":
                sortkey = "category__name"

            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == "desc":  # If direction is descending
                    sortkey = f"-{sortkey}"  # display descending
            products = products.order_by(sortkey)  # Sort products

        if "category" in request.GET:  # If there is a category
            categories = request.GET["category"].split(",")  # Split the categories
            products = products.filter(
                category__name__in=categories
            )  # Filter the products by the categories
            categories = Category.objects.filter(
                name__in=categories
            )  # Filter the categories by the categories
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

    current_sorting = f"{sort}_{direction}"  # Set current sorting

    context = {  # Pass the context to the template
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_sorting": current_sorting,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to show individual product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/products_detail.html", context)
