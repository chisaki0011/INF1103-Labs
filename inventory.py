"""
Inventory Module - Lab 8 (Aggregation and Polymorphism)
=======================================================

This module handles the INVENTORY (collection of products) using Object-Oriented
Programming. The Inventory class has ONE responsibility: manage a collection of
Product objects.

The Inventory aggregates Product objects. Products can exist before they are
added and remain usable after removal. It works with the abstract Product type,
so it does not know or care whether a product is physical or digital. It only
calls the public methods that every product promises to provide.

According to the lab brief, the Inventory class should NOT:
- Load or save files
- Display the main menu
- Ask users for input
- Handle individual product data/state (including weight or download size)

These responsibilities are handled by other modules instead:
- functions.py handles file I/O operations
- app.py handles the main menu and user interaction
- product.py / physical_product.py / digital_product.py handle product data
- product_factory.py rebuilds the right subclass when loading JSON
"""


from product import Product
from product_factory import create_product


class Inventory:
    """
    Represents the inventory system that manages a collection of Product objects.

    Uses encapsulation with private attribute (_products) to protect the internal
    collection. External code should only interact through public methods.

    Example usage:
        >>> inv = Inventory()
        >>> product = PhysicalProduct("P001", "Laptop", 999.0, 5, 2.2)
        >>> inv.add_product(product)
        >>> inv.search_product("P001")
    """

    def __init__(self) -> None:
        """Initialize the Inventory with an empty collection of Product objects."""
        self._products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        """Return a copy of the products currently in this inventory."""
        return self._products.copy()

    def add_product(self, product: Product | dict[str, object]) -> bool:
        """
        Add a new Product to the inventory.

        Accepts a Product object or a dictionary (used when loading
        inventory.json). Duplicate product IDs are rejected.

        Args:
            product (Product | dict): The product to add.

        Returns:
            bool: True if the product was added, False if the ID already exists.

        Raises:
            TypeError: If the argument is neither a Product nor a dictionary.
            ValueError: If the dictionary has an unknown product type or is
                missing the attributes required by that type.
        """
        # Accept a dictionary for convenience when loading from JSON.
        # The factory picks PhysicalProduct or DigitalProduct from the 'type'.
        if isinstance(product, dict):
            product = create_product(product)

        if not isinstance(product, Product):
            raise TypeError(
                "Inventory.add_product() expects a Product object or a dictionary."
            )

        # Check for duplicate product IDs
        for existing_product in self._products:
            if existing_product.get_product_id() == product.get_product_id():
                print(
                    f"Error: Product with ID '{product.get_product_id()}' "
                    f"already exists."
                )
                return False

        # Add to collection
        self._products.append(product)
        print(f"Product '{product.get_name()}' added successfully!")

        return True

    def search_product(self, product_id):
        """
        Search for a product by its ID.

        Args:
            product_id (str): The unique identifier of the product to search.

        Returns:
            Product | None: The found Product object if it exists, None otherwise.
        """
        for product in self._products:
            if product.get_product_id() == product_id:
                return product

        print(f"Product with ID '{product_id}' not found.")
        return None

    def display_all(self):
        """
        Display all products in the inventory.

        Each product displays itself through its own overridden
        display_information(), so physical and digital products print their
        own details without the Inventory knowing the difference.
        """
        if len(self._products) == 0:
            print("Inventory is empty.")
            return

        print("Current Inventory")
        print("-" * 60)
        for product in self._products:
            product.display_information()
        print("-" * 60)

    def update_stock_for_product(self, product_id, new_stock):
        """
        Set the stock quantity for a specific product.

        This method is a convenience wrapper that combines search and update.
        Used by the main application when handling menu option 3 (Update Stock).

        Args:
            product_id (str): The ID of the product to update.
            new_stock (int): The new stock quantity.

        Returns:
            bool: True if updated successfully, False otherwise.
        """
        product = self.search_product(product_id)
        if product is None:
            return False

        try:
            old_stock = product.get_stock()
            product.update_stock(new_stock)
            print(
                f"Stock updated for '{product.get_name()}': "
                f"{old_stock} -> {product.get_stock()}"
            )
            return True
        except ValueError as error:
            print(f"Error: {error}")
            return False

    def get_all_products(self):
        """
        Return a list of all products in the inventory.

        Returns:
            list: List of Product objects (a copy, so callers cannot replace
            the internal collection).
        """
        return self._products.copy()

    def to_dict_list(self):
        """
        Return the inventory as a list of JSON-serialisable dictionaries.

        Used by the file-handling functions when saving inventory.json.

        Returns:
            list[dict]: One dictionary per product.
        """
        return [product.to_dict() for product in self._products]
