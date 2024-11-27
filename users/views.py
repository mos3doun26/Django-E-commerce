from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserUpdateForm, UpdatePasswordForm, UpdateInfoForm
from store.models import Profile
import json
from cart.cart import Cart
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username = username, password = password)
            messages.success(request, message=f"Your account has been created, {username}")
            login(request, user=user)
            return redirect("home")
        else:
            try:
                form.clean_email()
            except:
                 messages.success(request, message="You can't use this email, Already registered.")
                 return redirect("register")

            messages.success(request, message="There is an error, Please Try register again.")
            return redirect("register")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})

def custom_logout(request):
    logout(request)
    messages.success(request, message="You are logged out, Thank for your shopping.")
    return redirect("home")

def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if not user == None:
            login(request, user)
            messages.success(request, message=f"You are logged in, {username}")
            # get the current user profile
            current_user = Profile.objects.get(user__id = request.user.id)
            # get the str of old cart saved in database
            saved_cart = current_user.old_cart
            # convert this str of old cart to python dictionary
            saved_cart = json.loads(saved_cart)
            # if there is an old cart 
            if saved_cart:
                # get the products and their quantity and add them to cart instance
                for product, quantity in saved_cart.items():
                    # current cart
                    cart = Cart(request)
                    cart.db_add(product=product, quantity=quantity)
                    
            return redirect("home")
        else:
            messages.success(request, message="There is an error, please try again.")
            return redirect("login")
    else:
        return render(request, "users/login.html")
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UserUpdateForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, message="Your profile has been updated")
            return redirect("home")
        return render(request, "users/update_user.html", {"user_form": user_form})
    else:
        messages.success(request, message="Login first to access this page...")
        return redirect("login")


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        password_form = UpdatePasswordForm(current_user)
        if request.method == "POST":
            password_form = UpdatePasswordForm(current_user, request.POST)
            if password_form.is_valid():
                password_form.save()
                login(request, current_user)
                messages.success(request, message="Your password has been updated.")
                return redirect("update_password")
            else:
                for error in list(password_form.errors.values()):
                    messages.error(request, error)
                return redirect("update_password")
        else:
            return render(request, "users/update_password.html", {"form": password_form})
    else:
        messages.success(request, message="You can't access this page login in first.")
        return redirect("login")


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_address = ShippingAddress.objects.get(user__id=request.user.id)
        form = UpdateInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_address)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, message="Your profile info has been updated")
            return redirect("home")
        return render(request, "users/update_info.html", {"form": form, "shipping_form": shipping_form})
    else:
        messages.success(request, message="Login first to access this page...")
        return redirect("login")