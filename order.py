"""Order model for customer orders."""

from product import Product
from order_line import OrderLine


class Order:
    """An order that creates and manages its own order lines."""

    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self._order_lines: list[OrderLine] = []

    @property
    def order_lines(self) -> list[OrderLine]:
        """Return a copy of the order lines without exposing the collection."""
        return self._order_lines.copy()

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create an OrderLine and add it to this order."""
        self._order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, index: int) -> None:
        """Remove an order line by its zero-based position."""
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError("Order line index must be an integer.")
        if index < 0 or index >= len(self._order_lines):
            raise IndexError("Order line index is out of range.")
        del self._order_lines[index]

    def calculate_total(self) -> float:
        """Return the sum of all order-line subtotals."""
        return sum(
            (line.calculate_subtotal() for line in self._order_lines), 0.0
        )

    def display_information(self) -> str:
        """Print and return the order lines and order total."""
        lines = [f"Order {self.order_id}"]
        print(lines[0])
        for order_line in self._order_lines:
            lines.append(order_line.display_information())
        lines.append(f"Total: ${self.calculate_total():.2f}")

        information = "\n".join(lines)
        print(lines[-1])
        return information
