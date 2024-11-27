from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        # store the session of the request
        self.session = request.session
        # get cart session key if it exists
        # save request as a variable
        self.request = request
        cart = self.session.get("session_key")
        # if have not session key, new user then create empty one
        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}

        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        quantity = int(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = quantity

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=carty)

    def add(self, product, quantity):
        product_id = str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = quantity

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=carty)

    def __len__(self):
        return len(self.cart)
    
    def cart_products(self):
        products_ids = self.cart.keys()
        cart_products = Product.objects.filter(id__in = products_ids)
        return cart_products
    
    def get_quantities(self):
        return self.cart
    
    def update(self, product, quantity):
        product_id= str(product)
        our_cart = self.cart
        our_cart[product_id] = quantity

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=carty)

        return self.cart
    
    def delete(self, product):
        product_id = str(product)
        self.cart.pop(product_id)
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=carty)
        return self.cart
    
    def total(self):
        total = 0
        if self.cart:
            for product_id, quantity in self.cart.items():
                product = Product.objects.get(id=product_id)
                product_price = product.sale_price if product.is_on_sale else product.price
                total += (product_price * quantity)

        return total