class Cart:

    def add_to_cart(self, product, quantity):

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        return product.price * quantity