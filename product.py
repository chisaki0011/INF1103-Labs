"""
Product Module - Week 8 OOP Refactor (Lab 6)
============================================

This module handles a single PRODUCT using Object-Oriented Programming.
The Product class has ONE responsibility: manage product data and state.

According to the lab brief (Section 2.5), the Product class should NOT:
- Load or save files
- Display the main menu
- Ask users for input
- Manage the entire inventory

These responsibilities are handled by other modules instead:
- functions.py handles file I/O operations
- app.py handles the main menu and user interaction
- inventory.py handles the collection of products
"""


class Product:
    """
    Represents a single product in the inventory system.

    Uses encapsulation with private attributes (double underscore prefix)
    to protect the internal data. External code should only interact
    through public methods like update_stock() and display_information().

    The constructor accepts either the lab-style positional arguments::

        Product("P001", "Laptop", 1200.00, 15)

    or a dictionary loaded from inventory.json::

        Product({"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15})
    """

    def __init__(self, product_id, name=None, price=None, stock=None):
        """
        Initialize a Product.

        Args:
            product_id (str | dict): The product ID, or a dictionary containing
                the keys 'id', 'name', 'price' and 'stock'.
            name (str): Product name (ignored when a dictionary is supplied).
            price (float): Product price (ignored when a dictionary is supplied).
            stock (int): Current stock quantity (ignored when a dictionary is supplied).

        Example:
            >>> Product("P001", "Laptop", 1200.0, 15)
            >>> Product({"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15})
        """
        # Support dictionary input so inventory.json can be loaded directly
        if isinstance(product_id, dict):
            data = product_id
            product_id = data["id"]
            name = data["name"]
            price = data["price"]
            stock = data["stock"]

        if name is None or price is None or stock is None:
            raise ValueError(
                "Product requires an id, name, price and stock "
                "(or a single dictionary containing those keys)."
            )

        # Use double underscore prefix to indicate private attributes
        # This follows the encapsulation principle from the lab brief (Section 2.4)
        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__price = float(price)
        self.__stock = int(stock)

    def __str__(self):
        """
        Return a string representation of the Product for console display.

        Returns:
            str: Formatted product information.

        Example:
            >>> product = Product("P001", "Laptop", 999.0, 5)
            >>> print(product)
            Product(id=P001, name=Laptop, price=999.0, stock=5)
        """
        return (
            f"Product(id={self.__product_id}, name={self.__name}, "
            f"price={self.__price}, stock={self.__stock})"
        )

    def update_stock(self, quantity):
        """
        Set the product's stock to a new quantity.

        This method encapsulates the business logic for updating stock.
        External code calls this instead of directly changing __stock.

        Args:
            quantity (int): The new stock quantity (must be >= 0).

        Raises:
            ValueError: If quantity is negative.

        Example:
            >>> product = Product("P001", "Laptop", 999.0, 10)
            >>> product.update_stock(50)
            >>> product.get_stock()
            50
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self.__stock = quantity

    def display_information(self):
        """
        Display the product's information in a formatted line.

        Returns:
            str: The formatted product details (also printed to the console).

        Example:
            >>> product = Product("P001", "Laptop", 999.0, 15)
            >>> product.display_information()
            ID: P001 | Name: Laptop | Price: $999.00 | Stock: 15
        """
        information = (
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )
        print(information)
        return information

    def get_product_id(self):
        """
        Get the product ID (getter method for encapsulated attribute).

        Returns:
            str: The product's ID.
        """
        return self.__product_id

    def get_name(self):
        """
        Get the product name (getter method for encapsulated attribute).

        Returns:
            str: The product's name.
        """
        return self.__name

    def get_price(self):
        """
        Get the product price (getter method for encapsulated attribute).

        Returns:
            float: The product's price.
        """
        return self.__price

    def get_stock(self):
        """
        Get the current stock quantity (getter method for encapsulated attribute).

        Returns:
            int: The product's current stock level.
        """
        return self.__stock

    def to_dict(self):
        """
        Convert the Product back into a JSON-serialisable dictionary.

        Used by the file-handling functions when saving inventory.json.

        Returns:
            dict: Dictionary with keys 'id', 'name', 'price' and 'stock'.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
