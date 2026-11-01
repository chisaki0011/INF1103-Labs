"""
Functions Module - Lab 7 (Inheritance, Overriding and Abstraction)
===================================================================

This module contains all helper functions for file I/O, input validation,
and display operations. These are extracted from persistent_auditor.py
to follow the Single Responsibility Principle and separation of concerns.

The product classes handle product data/state.
The app.py module handles the main CLI menu and user interaction.
This module handles everything else (file I/O, prompts, displays).
"""

import json
import os

from product_factory import create_product


# ---------------------------------------------------------------------------
# File I/O Functions - Handle reading and saving inventory to JSON
# ---------------------------------------------------------------------------

INVENTORY_FILE = "inventory.json"


def load_inventory(filename=INVENTORY_FILE):
    """Load inventory list from JSON file if it exists, else start empty.
    
    This function handles all error cases: missing file, corrupted JSON,
    invalid data types, etc.

    Each record keeps its 'type' identifier ('physical' or 'digital') and the
    matching extra field ('weight' or 'download_size'), so the factory can
    rebuild the correct subclass later.

    Args:
        filename (str): Path to the JSON file to load.
        
    Returns:
        list: List of product dictionaries. Empty list if file doesn't exist
              or is corrupted.
              
    Example:
        >>> inventory = load_inventory("inventory.json")
        >>> print(len(inventory))
        7
    """
    if os.path.exists(filename):
        print(f"{filename} found.")
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            if not isinstance(data, list):
                print(f"Error: {filename} is corrupted. Starting with empty inventory.")
                return []
            print("Inventory loaded successfully.")
            return data
        except json.JSONDecodeError:
            print(f"Error: {filename} contains invalid JSON.")
            return []
    else:
        # File doesn't exist yet - start fresh
        print(f"{filename} not found. Starting with empty inventory.")
        return []


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Save the inventory to a JSON file.

    Accepts either an Inventory object (the OOP system) or a plain list of
    Product/dictionary objects (the Week 5 functional system). Products are
    converted with Product.to_dict(), which each subclass extends with its
    own 'type' identifier and extra attributes, so nothing is lost on save.

    Args:
        inventory (Inventory | list): Inventory object or list of products.
        filename (str): Path to the JSON file to save to.

    Returns:
        bool: True if saved successfully, False otherwise.

    Example:
        >>> products = [{"id": "P001", "name": "Laptop", "price": 999.0, "stock": 5}]
        >>> save_inventory(products)
        True
    """
    try:
        # An Inventory object exposes get_all_products(); a plain list does not.
        if hasattr(inventory, "get_all_products"):
            products = inventory.get_all_products()
        else:
            products = inventory

        serialisable = []
        for item in products:
            if isinstance(item, dict):
                serialisable.append(item)
            elif hasattr(item, "to_dict"):
                serialisable.append(item.to_dict())
            else:
                raise TypeError(f"Cannot serialise item of type {type(item).__name__}")

        with open(filename, "w") as file:
            json.dump(serialisable, file, indent=2)
        return True
    except (IOError, TypeError) as error:
        print(f"Error: Could not write to file ({error}).")
        return False


# ---------------------------------------------------------------------------
# Display Functions - Show information to the user
# ---------------------------------------------------------------------------

def display_all(inventory):
    """Display all products in the inventory.

    Accepts either an Inventory object, a list of Product objects, or a list
    of product dictionaries (Week 5 compatibility).

    Args:
        inventory (Inventory | list): Inventory object or list of products.

    Returns:
        bool: True if at least one product was displayed, False otherwise.

    Example:
        >>> products = [{"id": "P001", "name": "Laptop", "price": 999.0, "stock": 5}]
        >>> display_all(products)
        Inventory:
        ID: P001 | Name: Laptop | Price: $999.00 | Stock: 5
    """
    if hasattr(inventory, "get_all_products"):
        products = inventory.get_all_products()
    else:
        products = inventory

    print("Inventory:")
    for product in products:
        if hasattr(product, "display_information"):
            product.display_information()
        else:
            # Dictionary (Week 5) format
            display_str = (f"ID: {product['id']} | "
                           f"Name: {product['name']} | "
                           f"Price: ${float(product['price']):.2f} | "
                           f"Stock: {int(product['stock'])}")
            print(display_str)
    return len(products) > 0


# ---------------------------------------------------------------------------
# Search Functions - Find products by various criteria
# ---------------------------------------------------------------------------

def find_product_by_id(inventory, product_id):
    """Find a product by its ID.
    
    Args:
        inventory (list): List of product dictionaries from JSON file.
        product_id (str): The product ID to search for (e.g., "P001").
        
    Returns:
        dict or None: The matching product dictionary, or None if not found.
              
    Example:
        >>> products = [{"id": "P001", "name": "Laptop", ...}]
        >>> find_product_by_id(products, "P001")
        {'id': 'P001', 'name': 'Laptop', ...}
    """
    for product in inventory:
        if product["id"] == product_id:
            return product
    print("Product not found.")
    return None


def search_product(inventory, search_term):
    """Search for products by name (case-insensitive partial match).
    
    Args:
        inventory (list): List of product dictionaries from JSON file.
        search_term (str): The search term to match against product names.
        
    Returns:
        list: List of matching product dictionaries, or empty list if none found.
              
    Example:
        >>> products = [{"id": "P001", "name": "Laptop", ...}, 
                        {"id": "P002", "name": "Mouse", ...}]
        >>> search_product(products, "lap")
        [{'id': 'P001', 'name': 'Laptop', ...}]
    """
    matches = []
    for product in inventory:
        if search_term.lower() in product["name"].lower():
            matches.append(product)
    
    if len(matches) > 0:
        print(f"Found {len(matches)} product(s):")
        for p in matches:
            display_str = (f"ID: {p['id']} | "
                           f"Name: {p['name']} | "
                           f"Price: ${float(p['price']):.2f} | "
                           f"Stock: {int(p['stock'])}")
            print(display_str)
        return matches
    else:
        print("No products found.")
        return []


# ---------------------------------------------------------------------------
# Input Validation Functions - Validate user input before processing
# ---------------------------------------------------------------------------

def get_valid_price():
    """Prompt the user for a valid price (must be >= 0).
    
    Returns:
        float: A valid price value (>= 0).
              
    Example:
        >>> price = get_valid_price()
        >>> print(price)
        99.99
    """
    while True:
        try:
            # Use strip() to remove whitespace from input
            raw_input = input("Enter price (must be >= 0): ").strip()
            if not raw_input:
                print("Error: Price cannot be empty.")
                continue
            
            price = float(raw_input)
            if price < 0:
                print("Error: Price cannot be negative. Please try again.")
                continue
                
            return price
        except ValueError:
            # This catches non-numeric input like "abc" or "$99"
            print("Error: Invalid input. Please enter a numeric value (e.g., 99.99).")


def get_valid_stock():
    """Prompt the user for valid stock quantity (must be >= 0).
    
    Returns:
        int: A valid stock quantity (>= 0).
              
    Example:
        >>> stock = get_valid_stock()
        >>> print(stock)
        50
    """
    while True:
        try:
            raw_input = input("Enter stock quantity (must be >= 0): ").strip()
            if not raw_input:
                print("Error: Stock cannot be empty.")
                continue
            
            stock = int(raw_input)
            if stock < 0:
                print("Error: Stock quantity cannot be negative. Please try again.")
                continue
                
            return stock
        except ValueError:
            # This catches non-numeric input like "abc" or "5.5"
            print("Error: Invalid input. Please enter an integer value (e.g., 50).")


def get_valid_weight():
    """Prompt the user for a valid weight in kilograms (must be >= 0).

    Used when adding a PhysicalProduct.

    Returns:
        float: A valid weight value (>= 0).

    Example:
        >>> weight = get_valid_weight()
        >>> print(weight)
        2.5
    """
    while True:
        try:
            raw_input = input("Enter weight in kg (must be >= 0): ").strip()
            if not raw_input:
                print("Error: Weight cannot be empty.")
                continue

            weight = float(raw_input)
            if weight < 0:
                print("Error: Weight cannot be negative. Please try again.")
                continue

            return weight
        except ValueError:
            print("Error: Invalid input. Please enter a numeric value (e.g., 2.5).")


def get_valid_download_size():
    """Prompt the user for a valid download size in megabytes (must be > 0).

    Used when adding a DigitalProduct.

    Returns:
        float: A valid download size value (> 0).

    Example:
        >>> size = get_valid_download_size()
        >>> print(size)
        1200.0
    """
    while True:
        try:
            raw_input = input("Enter download size in MB (must be > 0): ").strip()
            if not raw_input:
                print("Error: Download size cannot be empty.")
                continue

            download_size = float(raw_input)
            if download_size <= 0:
                print("Error: Download size must be greater than zero.")
                continue

            return download_size
        except ValueError:
            print("Error: Invalid input. Please enter a numeric value (e.g., 1200).")


def get_valid_product_id(inventory):
    """Prompt user for a valid product ID that exists in inventory.
    
    Args:
        inventory (list): List of product dictionaries from JSON file.
        
    Returns:
        str or None: A valid product ID, or None if no valid input entered.
              
    Example:
        >>> products = [{"id": "P001", ...}, {"id": "P002", ...}]
        >>> product_id = get_valid_product_id(products)
        >>> print(product_id)
        P001
    """
    print("Available Product IDs:")
    for product in inventory:
        print(f"  - {product['id']} ({product['name']})")
    
    while True:
        try:
            raw_input = input("\nEnter product ID to update: ").strip()
            if not raw_input:
                print("Error: Product ID cannot be empty.")
                continue
                
            for product in inventory:
                if product["id"] == raw_input:
                    return raw_input
                    
            print(f"Error: '{raw_input}' is not a valid product ID. Please try again.")
        except EOFError:
            # Handle Ctrl+D or pipe input (e.g., from another command)
            print()
            return None


def get_valid_product_name(inventory):
    """Prompt user for a valid product name that exists in inventory.
    
    Args:
        inventory (list): List of product dictionaries from JSON file.
        
    Returns:
        str or None: A valid product name, or None if no valid input entered.
              
    Example:
        >>> products = [{"id": "P001", "name": "Laptop", ...}, 
                        {"id": "P002", "name": "Mouse", ...}]
        >>> product_name = get_valid_product_name(products)
        >>> print(product_name)
        Laptop
    """
    print("Available Products:")
    for product in inventory:
        print(f"  - {product['id']}: {product['name']}")
    
    while True:
        try:
            raw_input = input("\nEnter product name to update: ").strip()
            if not raw_input:
                print("Error: Product name cannot be empty.")
                continue
            
            for product in inventory:
                if product["name"].lower() == raw_input.lower():
                    return product["name"]
                    
            print(f"Error: '{raw_input}' is not a valid product name. Please try again.")
        except EOFError:
            # Handle Ctrl+D or pipe input
            print()
            return None


# ---------------------------------------------------------------------------
# CRUD Operations - Add and Update functions using Product class
# ---------------------------------------------------------------------------

def add_product(inventory):
    """Add a new product to the inventory.
    
    This function prompts the user for all necessary information, validates
    the input, creates a Product object, and adds it to the inventory list.
    
    Args:
        inventory (list): List of product dictionaries from JSON file.
        
    Returns:
        bool: True if product was added successfully, False otherwise.
              
    Example:
        >>> products = [{"id": "P001", ...}, {"id": "P002", ...}]
        >>> add_product(products)
        True
    """
    print("\n=== Add New Product ===")
    
    # Get product ID (must be unique)
    while True:
        product_id = input("Enter product ID (e.g., P003): ").strip()
        if not product_id:
            print("Error: Product ID cannot be empty.")
            continue
        
        # Check if ID already exists
        for product in inventory:
            if product["id"] == product_id:
                print(f"Error: Product ID '{product_id}' already exists!")
                break
        else:
            break
    
    # Get product name
    product_name = input("Enter product name: ").strip()
    
    # Get price (validated by get_valid_price)
    price = get_valid_price()
    
    # Get stock quantity (validated by get_valid_stock)
    stock = get_valid_stock()
    
    # Create a new Product object using the encapsulated class
    new_product_dict = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }
    
    inventory.append(new_product_dict)
    print(f"\nProduct '{product_name}' (ID: {product_id}) added successfully!")
    
    # Save the updated inventory to file
    save_inventory(inventory)
    return True


def update_stock(product_id, inventory):
    """Update stock quantity for an existing product.
    
    This function finds the product by ID, prompts for new stock quantity,
    creates a Product object, calls its update_stock() method, and saves.
    
    Args:
        product_id (str): The product ID to update (e.g., "P001").
        inventory (list): List of product dictionaries from JSON file.
        
    Returns:
        bool: True if stock was updated successfully, False otherwise.
              
    Example:
        >>> products = [{"id": "P001", ...}]
        >>> update_stock("P001", products)
        True
    """
    # Find the product by ID using helper function
    product_data = find_product_by_id(inventory, product_id)
    
    if product_data is None:
        return False
    
    print(f"\nCurrent stock for '{product_data['name']}': {int(product_data['stock'])}")
    
    # Get new stock quantity from user
    new_stock = get_valid_stock()
    
    # Create a Product object to use its encapsulated update_stock method
    product_obj = create_product(product_data)

    old_stock = product_obj.get_stock()
    product_obj.update_stock(new_stock)
    
    print(f"Stock updated from {old_stock} to {product_obj.get_stock()}")
    
    # Update inventory with new stock value
    product_data["stock"] = product_obj.get_stock()
    
    # Save changes to file
    save_inventory(inventory)
    return True
