"""
Inventory Module - Week 5 OOP Refactor
========================================

This module handles the INVENTORY (collection of products) using Object-Oriented Programming.
The Inventory class has ONE responsibility: manage a collection of Product objects.

According to the lab brief (Section 2.5), the Inventory class should NOT:
- Load or save files
- Display the main menu
- Ask users for input
- Handle individual product data/state

These responsibilities are handled by other modules instead:
- functions.py handles file I/O operations
- app.py handles the main menu and user interaction
- product.py handles individual product data/state
"""


from product import Product
import functions as fn


class Inventory:
    """
    Represents the inventory system that manages a collection of Product objects.
    
    Uses encapsulation with private attribute (_products) to protect the internal
    collection. External code should only interact through public methods.
    
    Example usage:
        >>> inv = Inventory()
        >>> product = Product({"id": "P001", "name": "Laptop", "price": 999.0, "stock": 5})
        >>> inv.add_product(product)
        >>> inv.search_product("P001")
    """
    
    def __init__(self):
        """
        Initialize the Inventory with an empty collection of Product objects.
        
        Note: This class does NOT load inventory from file in __init__.
        File loading is handled separately by functions.load_inventory().
        The inventory list is passed to this constructor as optional parameter.
        """
        self._products = []  # Private collection of Product objects
    
    def add_product(self, product_dict):
        """
        Add a new product to the inventory.
        
        This method accepts a dictionary (as expected by functions.load_inventory),
        creates a Product object from it, and adds it to the collection.
        Duplicate checking is handled automatically.
        
        Args:
            product_dict (dict): Dictionary with keys: id, name, price, stock
            
        Returns:
            bool: True if product was added successfully, False if duplicate ID
            
        Raises:
            ValueError: If any validation fails (invalid price, negative stock)
        """
        # Create a new Product object from the dictionary
        product = Product(product_dict)
        
        # Check for duplicate product IDs
        for existing_product in self._products:
            if existing_product.get_product_id() == product.get_product_id():
                print(f"Error: Product with ID '{product.get_product_id()}' already exists.")
                return False
        
        # Add to collection
        self._products.append(product)
        print(f"Product '{product.get_name()}' added successfully!")
        
        return True
    
    def search_product(self, product_id):
        """
        Search for a product by its ID.
        
        Args:
            product_id (str): The unique identifier of the product to search
            
        Returns:
            Product | None: The found Product object if exists, None otherwise
        """
        for product in self._products:
            if product.get_product_id() == product_id:
                return product
        
        print(f"Product with ID '{product_id}' not found.")
        return None
    
    def display_all(self):
        """
        Display all products in the inventory.
        
        Uses existing display function from functions module for consistent output.
        """
        if len(self._products) == 0:
            print("Inventory is empty.")
            return
        
        # Use existing display function for consistency
        fn.display_all_products(self._products)


# ---------------------------------------------------------------------------
# Additional management methods (optional extensions)
# ---------------------------------------------------------------------------

    def update_stock_for_product(self, product_id, quantity):
        """
        Update stock quantity for a specific product.
        
        This method is a convenience wrapper that combines search and update.
        Used by the main application when handling menu option 3 (Update Stock).
        
        Args:
            product_id (str): The ID of the product to update
            quantity (int): The amount to add to current stock
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        product = self.search_product(product_id)
        if product is None:
            return False
        
        try:
            old_stock = product.get_stock()
            new_stock = old_stock + int(quantity)
            product.update_stock(new_stock)
            print(f"✓ Stock updated for '{product.get_product_name()}': {old_stock} → {new_stock}")
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False
    
    def get_all_products(self):
        """
        Return a list of all products in the inventory.
        
        Returns:
            list: List of Product objects
        """
        return self._products.copy()  # Return copy to prevent external modification
