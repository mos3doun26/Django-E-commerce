from .cart import Cart


# here we create content processors to make out cart avialable on all pages.
def cart(request):
    # return the defualt date from our cart
    return {"cart": Cart(request)}