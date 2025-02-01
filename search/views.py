from django.shortcuts import render
from products.models import Category, Product

def search(request):
    # Get the search query from the GET request
    search_query = request.GET.get('category_name')

    # Fetch all categories for dropdown or display purposes
    categories = Category.objects.all()

    # Filter products based on the search query
    product = Product.objects.filter(
        category__category_name__icontains=search_query
    ) if search_query else Product.objects.none()

    # Prepare context for the template
    context = {
        "product": product,
        "search": search_query,
        "categories": categories,  # Include all categories in the context
    }
    return render(request, 'products/category.html', context)
