from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.cart_products
    quantities = cart.get_quantities
    total = cart.total
    return render(request, "cart/cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "total": total})

def cart_add(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # look up product in DB
        product = get_object_or_404(Product, id=product_id)
        # save to a session
        cart.add(product=product, quantity=product_qty)
        qty = cart.__len__()
        # return Response
        response = JsonResponse({"qty": qty})
        messages.success(request, message=f"{product.name} has been add to your cart")
        return response
    return JsonResponse({})


def cart_update(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get('product_qty'))


        cart.update(product=product_id, quantity=product_qty)
        messages.success(request, message=f"item with id: {product_id} had been updated")
        response = JsonResponse({"qty": product_qty})
        return response
    return JsonResponse({})

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))

        cart.delete(product=product_id)
        messages.success(request, message=f"item with id: {product_id} had been deleted")
        response = JsonResponse({"product": product_id})
        return response
    return JsonResponse({})