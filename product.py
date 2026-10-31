"""
Product Module - Week 5 OOP Refactor
=====================================

This module handles a single PRODUCT using Object-Oriented Programming.
The Product class has ONE responsibility: manage product data and state.

According to the lab brief (Section 2.5), the Product class should NOT:
- Load or save files
- Display the main menu  
- Ask users for input
- Manage the entire inventory

These responsibilities are handled by other modules instead.
"""


class Product:
    """
    Represents a single product in the inventory system.
    
    Uses encapsulation with private attributes (double underscore prefix)
    to protect the internal data. External code should only interact
    through public methods like update_stock() and display_information().
    
    Example usage:
        >>> my_product = Product({"id": "P001", "name": "Laptop", "price": 999.0, "stock": 5})
        >>> my_product.update_stock(10)
        >>> my_product.display_information()
    """
    
    def __init__(self, product_dict):
        """
        Initialize a Product with data from a dictionary (loaded from JSON).
        
        Args:
            product_dict (dict): Contains product data with keys: 'id', 'name', 
                               'price', and 'stock'.
        
        Example:
            >>> product_data = {"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15}
            >>> product = Product(product_data)
        """
        # Use double underscore prefix to indicate private attributes
        # This follows the encapsulation principle from the lab brief (Section 2.4)
        self.__product_id = product_dict["id"]
        self.__name = product_dict["name"]
        self.__price = float(product_dict["price"])
        self.__stock = int(product_dict["stock"])
    
    def __str__(self):
        """
        Return a string representation of the Product for console display.
        
        Returns:
            str: Formatted product information.
        
        Example:
            >>> product = Product({"id": "P001", "name": "Laptop", "price": 999.0, "stock": 5})
            >>> print(product)
            Product(id=P001, name=Laptop, price=999.0, stock=5)
        """
        return f"Product(id={self.__product_id}, name={self.__name}, price={self.__price}, stock={self.__stock})"
    
    def update_stock(self, quantity):
        """
        Update the product's stock quantity.
        
        This method encapsulates the business logic for updating stock.
        External code calls this instead of directly changing __stock.
        
        Args:
            quantity (int): The amount to ADD to current stock (must be >= 0).
        
        Example:
            >>> product = Product({"id": "P001", "name": "Laptop", "price": 999.0, "stock": 10})
            >>> product.update_stock(5)
            >>> print(product.__stock)
            15
        
        Note:
            This method adds to the current stock (increment), not replaces it.
            For full replacement use: product.update_stock(new_quantity - current_quantity)
        """
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        
        self.__stock += quantity
    
    def display_information(self):
        """
        Display the product's information in a formatted string.
        
        Returns:
            str: Formatted product details (ID, name, price, stock).
        
        Example:
            >>> product = Product({"id": "P001", "name": "Laptop", "price": 999.0, "stock": 15})
            >>> print(product.display_information())
            ID: P001 | Name: Laptop | Price: $999.00 | Stock: 15
        """
        return (f"ID: {self.__product_id} | "
                f"Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | "
                f"Stock: {self.__stock}")
    
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
