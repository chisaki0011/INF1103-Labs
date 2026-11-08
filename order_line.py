"""OrderLine model for customer orders."""

from product import Product


class OrderLine:
    """One product and quantity within an order."""

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("OrderLine requires a Product object.")
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("OrderLine quantity must be an integer.")
        if quantity <= 0:
            raise ValueError("OrderLine quantity must be greater than zero.")

        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        """Return the product price multiplied by the ordered quantity."""
        return self.product.get_price() * self.quantity

    def display_information(self) -> str:
        """Print and return this line's product, quantity, and subtotal."""
        information = (
            f"{self.product.get_name()} x {self.quantity} "
            f"@ ${self.product.get_price():.2f} = "
            f"${self.calculate_subtotal():.2f}"
        )
        print(information)
        return information
