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

    def save(self):
        self.session.modified = True
