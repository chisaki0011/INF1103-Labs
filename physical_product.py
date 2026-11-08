"""
PhysicalProduct Module - Lab 7 (Inheritance, Overriding, Interfaces)
====================================================================

A PhysicalProduct "is-a" Product that exists in the real world: it has a
weight, it must be shipped, and shipping costs money.

This class:
- inherits from Product (single class inheritance) and reuses its
  constructor with super();
- adds the weight attribute;
- overrides display_information() and reuses the parent version first;
- implements the abstract get_fulfilment_info() from Product;
- implements the CanBeShipped interface by signing the contract with
  calculate_shipping_cost().
"""

from can_be_shipped import CanBeShipped
from product import Product
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """
    A product that has a physical weight and requires shipping.

    Example:
        >>> guitar = PhysicalProduct("P010", "Guitar", 899.00, 3, 4.5)
        >>> guitar.display_information()
        ID: P010 | Name: Guitar | Price: $899.00 | Stock: 3
          Type: Physical | Weight: 4.50 kg
          Fulfilment: Requires physical shipping and handling.
          Shipping cost: $14.00
    """

    PRODUCT_TYPE: str = "physical"

    # Simple shipping rule: a flat handling fee plus a rate per kilogram.
    BASE_SHIPPING_FEE: float = 5.00
    SHIPPING_RATE_PER_KG: float = 2.00

    def __init__(
        self,
        product_id: str | dict[str, object],
        name: str | None = None,
        price: float | None = None,
        stock: int | None = None,
        weight: float | None = None,
        supplier: Supplier | None = None,
    ) -> None:
        """
        Initialize a PhysicalProduct.

        Args:
            product_id (str | dict): The product ID, or a dictionary containing
                the keys 'id', 'name', 'price', 'stock' and 'weight'.
            name (str): Product name (ignored when a dictionary is supplied).
            price (float): Product price (ignored when a dictionary is supplied).
            stock (int): Current stock quantity (ignored when a dictionary is supplied).
            weight (float): Weight in kilograms (ignored when a dictionary is supplied).
            supplier (Supplier): Supplier associated with this product.

        Raises:
            ValueError: If no weight is supplied or the weight is negative.
        """
        # Pull the extra attribute out before the parent handles the common ones
        if isinstance(product_id, dict):
            weight = product_id.get("weight", weight)

        # Reuse the existing Product constructor (Lab 7, Section 1.2)
        super().__init__(product_id, name, price, stock, supplier)

        if weight is None:
            raise ValueError("PhysicalProduct requires a weight in kilograms.")

        self.__weight: float = float(weight)
        if self.__weight < 0:
            raise ValueError("Weight cannot be negative.")

    def get_weight(self) -> float:
        """
        Get the product's weight (getter for the encapsulated attribute).

        Returns:
            float: Weight in kilograms.
        """
        return self.__weight

    def display_information(self) -> str:
        """
        Display the common product information plus the physical details.

        The parent implementation prints the shared fields, then this
        override adds the weight, the fulfilment method and the shipping
        cost. This is method overriding that reuses parent behaviour.

        Returns:
            str: The full multi-line product information.
        """
        # Reuse the parent behaviour instead of duplicating the common fields
        information = super().display_information()

        detail = f"  Type: Physical | Weight: {self.__weight:.2f} kg"
        print(detail)

        fulfilment = f"  Fulfilment: {self.get_fulfilment_info()}"
        print(fulfilment)

        shipping = f"  Shipping cost: ${self.calculate_shipping_cost():.2f}"
        print(shipping)

        return "\n".join([information, detail, fulfilment, shipping])

    def get_fulfilment_info(self) -> str:
        """
        Implement the abstract method from Product.

        Returns:
            str: Description of how a physical product is delivered.
        """
        return "Requires physical shipping and handling."

    def calculate_shipping_cost(self) -> float:
        """
        Implement the CanBeShipped contract.

        Rule: flat handling fee + a rate per kilogram of weight.

        Returns:
            float: The shipping cost in dollars, rounded to cents.

        Example:
            >>> PhysicalProduct("P010", "Guitar", 899.0, 3, 4.5).calculate_shipping_cost()
            14.0
        """
        cost = self.BASE_SHIPPING_FEE + self.SHIPPING_RATE_PER_KG * self.__weight
        return round(cost, 2)

    def to_dict(self) -> dict[str, object]:
        """
        Extend the parent dictionary with the physical attributes.

        Returns:
            dict: Common product fields plus 'type' and 'weight'.
        """
        data = super().to_dict()
        data["weight"] = self.__weight
        return data
