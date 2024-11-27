from django.shortcuts import render, redirect
from cart.cart import Cart
from store.models import Product
from .models import Order
from .forms import ShippingAddressForm, PaymentForm
from .models import ShippingAddress, OrderItem
from django.contrib import messages

def process_order(request):
    if request.POST:
        # cart and its info
        cart = Cart(request)
        cart_products = cart.cart_products
        quantities = cart.get_quantities
        total = cart.total()
        # get the billing info from last page
        payment_info =  PaymentForm(request.POST or None)

        # get the shipping info
        shipping_info = request.session["my_shipping"]
        # creating order 
        shipping_address = f"{shipping_info["shipping_address_1"]}\n{shipping_info["shipping_address_2"]}\n{shipping_info["shipping_country"]}\n{shipping_info["shipping_state"]}\n{shipping_info["shipping_city"]}\n{shipping_info["shipping_zip_code"]}"
        # check user is logged in 
        if request.user.is_authenticated:
            create_order = Order(user=request.user or None, full_name=shipping_info["shipping_full_name"], email=shipping_info["shipping_email"], shipping_address=shipping_address, amount_paid=total)
            create_order.save()
        else:
            create_order = Order(full_name=shipping_info["shipping_full_name"], email=shipping_info["shipping_email"], shipping_address=shipping_address, amount_paid=total)
            create_order.save()
        # create order items
        # get order id
        order_id = create_order.id
        # loop on cart_products to get every product info
        for product in cart_products():
            # product id
            product_id = product.id
            # get the price of the product
            price = product.sale_price if product.is_on_sale else product.price
            # imortant to get the correct quantity of the product we loop with
            for key, value in quantities().items():
                if int(key) == product.id:
                    # create the order item
                    if request.user.is_authenticated:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=request.user, quantity=value, price=price)
                        create_order_item.save()
                    else:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()
        # Removing products from cart after ordering
        # Our cart is a session_key then we will delete the session_key from rquest session
        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]
            
        messages.success(request, message="Order Placed!")
        return redirect("home")
    else:
        messages.success(request, message="Access denied")
        return redirect("home")


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.cart_products
        quantities = cart.get_quantities
        total = cart.total
        # create session with shipping info 
        my_shipping = request.POST
        request.session["my_shipping"] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm(request.POST)
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "total": total, "shipping_info": request.POST, "billing_form": billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "total": total, "shipping_info": request.POST, "billing_form": billing_form})
    else:
        messages.success(request, message="Access denied")
        return redirect("home")

def checkout(request):
    cart = Cart(request)
    cart_products = cart.cart_products
    quantities = cart.get_quantities
    total = cart.total
    if request.user.is_authenticated:
        shipping_address = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_address)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "total": total, "shipping_form": shipping_form})
    else:
        shipping_form = ShippingAddressForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "total": total, "shipping_form": shipping_form})
