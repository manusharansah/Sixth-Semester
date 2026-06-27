from cart import Cart

class Billing:

    def generate_bill(self, product, quantity):

        cart = Cart()

        return cart.add_to_cart(product, quantity)