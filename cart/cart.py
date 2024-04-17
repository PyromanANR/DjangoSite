from main.models import Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site
        self.cart = cart

    def __len__(self):
        return len(self.cart)

    def add_product(self, product, quantity=1):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'id': product_id}

        self.cart[product_id]['quantity'] += quantity
        self.save()
        current_user = Profile.objects.filter(user__id=self.request.user.id)
        # Convert {'3':1, '2':4} to {"3":1, "2":4}
        carty = str(self.cart)
        carty = carty.replace("\'", "\"")
        # Save carty to the Profile Model
        current_user.update(cart=str(carty))

    def save(self):
        self.session.modified = True

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Get the current user profile
        current_user = Profile.objects.filter(user__id=self.request.user.id)
        # Convert {'3':1, '2':4} to {"3":1, "2":4}
        carty = str(self.cart)
        carty = carty.replace("\'", "\"")
        # Save carty to the Profile Model
        current_user.update(cart=str(carty))


    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # Get cart
        ourcart = self.cart
        # Update Dictionary/cart
        cart = ourcart[product_id]
        cart['quantity'] = product_qty
        self.session.modified = True
        # Get the current user profile
        current_user = Profile.objects.filter(user__id=self.request.user.id)
        # Convert {'3':1, '2':4} to {"3":1, "2":4}
        carty = str(self.cart)
        carty = carty.replace("\'", "\"")
        # Save carty to the Profile Model
        current_user.update(cart=str(carty))
