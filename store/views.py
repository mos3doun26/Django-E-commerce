from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.contrib import messages
from urllib.parse import unquote
from django.db.models import Q
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories
    }
    return render(request, "store/home.html", context)

def about(request):
    return render(request, "store/about.html")
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    # product = get_object_or_404(Product, id=pk)
    return render(request, "store/product.html", {"product": product})


def category(request, name):
    category_name = name.replace("-", " ")
    try:
        # the url is always is lowercase and my the name of the category has upper case letters
        # and to search about the category without struggle, we use _iexact to skip the case of the letters
        # __iexact: to skip the case of the name, example: 
        category = Category.objects.get(name__iexact=category_name)
        products = Product.objects.filter(category=category)
        return render(request, "store/category.html", {"products": products, "category": category})
    except:
        messages.success(request, message="This category doesn't found...")
        return redirect("home")

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        if searched:
            products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
            return render(request, "store/search.html", context={"products": products, "search_qury": searched})
        else:
            messages.success(request, message="You Entered nothing.")
            return render(request, "store/search.html")
    else:
        return render(request, "store/search.html")