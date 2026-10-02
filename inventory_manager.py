"""inventory_audior.py
Week 5 Lab - Inventory Management System (Data Manipulation).

Reuses design patterns from:
  - auditor.py          (menu loop, basic validation: isalpha, quantity limits)
  - modular_auditor.py  (functional design, docstrings, input helpers, report style)
  - persistent_auditor.py (file persistence: read/append, validation helpers,
                           display from list, verify by re-reading)

Requirements covered:
  1. Data Representation: inventory items as dicts in a list (>= 3 products).
  2. Data Manipulation:  add_product(), update_stock(), search_product(),
                         display_all().
  3. Data Persistence:   load_inventory(), save_inventory() with inventory.json.
  4. Menu System:        Display, Add, Update, Search, Save, Exit.
"""

import json
import os

INVENTORY_FILE = "inventory.json"


# ---------------------------------------------------------------------------
# Persistence (reused pattern from persistent_auditor.read_orders / append_order)
# ---------------------------------------------------------------------------
def load_inventory(filename=INVENTORY_FILE):
    """Load inventory list from JSON file if it exists, else start empty.

    Args:
        filename (str): JSON file to load from.

    Returns:
        list: List of product dictionaries.
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
            print(f"Error: {filename} contains invalid JSON. Starting with empty inventory.")
            return []
        except OSError as e:
            print(f"Error loading inventory: {e}")
            return []
    else:
        print(f"{filename} not found.")
        print("Starting with empty inventory.")
        return []


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Save inventory list to JSON file.

    Args:
        inventory (list): List of product dictionaries.
        filename (str): JSON file to save to.

    Returns:
        bool: True if save succeeded, False otherwise.
    """
    try:
        with open(filename, "w") as file:
            json.dump(inventory, file, indent=2)
        return True
    except OSError as e:
        print(f"Error saving inventory: {e}")
        return False
    except TypeError as e:
        print(f"Error saving inventory: invalid data - {e}")
        return False


# ---------------------------------------------------------------------------
# Helpers (reused patterns from modular_auditor.get_valid_input and
# persistent_auditor.get_valid_item_name / get_valid_quantity)
# ---------------------------------------------------------------------------
def find_product(inventory, product_id):
    """Return product dict matching product_id, or None if not found."""
    for product in inventory:
        if str(product.get("id", "")).lower() == product_id.lower():
            return product
    return None


def get_valid_price(prompt="Price: "):
    """Prompt until a valid price (> 0) is entered. Returns float."""
    while True:
        user_input = input(prompt).strip()
        try:
            price = float(user_input)
        except ValueError:
            print("Invalid price. Please enter a valid number.")
            continue
        if price <= 0:
            print("Price must be greater than 0.")
            continue
        return price


def get_valid_stock(prompt="Stock Quantity: "):
    """Prompt until a valid stock (positive int, max 500) is entered.

    Reuses quantity rules from auditor.py / persistent_auditor.py.
    Returns int.
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input.isdigit():
            print("Invalid stock quantity. Please enter a valid integer.")
            continue
        quantity = int(user_input)
        if quantity <= 0:
            print("Stock quantity must be a positive integer.")
            continue
        if quantity > 500:
            print("Stock quantity exceeds maximum limit of 500.")
            continue
        return quantity


# ---------------------------------------------------------------------------
# Data Manipulation (required functions)
# ---------------------------------------------------------------------------
def display_all(inventory):
    """Display all products in the inventory list."""
    print("Current Inventory")
    print("------------------------------------------------")
    if not inventory:
        print("No products in inventory.")
    else:
        for product in inventory:
            try:
                pid = product["id"]
                name = product["name"]
                price = float(product["price"])
                stock = int(product["stock"])
                print(f"ID: {pid} | Name: {name} | Price: ${price:.2f} | Stock: {stock}")
            except (KeyError, ValueError, TypeError):
                print(f"Error: Skipping corrupted product entry: {product}")
    print("------------------------------------------------")


def add_product(inventory):
    """Add a new product to the inventory list (with validation)."""
    print("Add New Product")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Error: Product ID cannot be empty.")
        return
    if find_product(inventory, product_id) is not None:
        print("Error: Product ID already exists.")
        return

    product_name = input("Product Name: ").strip()
    if not product_name:
        print("Error: Product name cannot be empty.")
        return
    if not product_name.replace(" ", "").isalpha():
        print("Error: Product name must contain only letters and spaces.")
        return

    try:
        price_input = input("Price: ").strip()
        price = float(price_input)
    except ValueError:
        print("Error: Invalid price. Please enter a valid number.")
        return
    if price <= 0:
        print("Error: Price must be greater than 0.")
        return

    stock_input = input("Stock Quantity: ").strip()
    if not stock_input.isdigit():
        print("Error: Invalid stock quantity. Please enter a valid integer.")
        return
    stock = int(stock_input)
    if stock <= 0:
        print("Error: Stock quantity must be a positive integer.")
        return
    if stock > 500:
        print("Error: Stock quantity exceeds maximum limit of 500.")
        return

    inventory.append({
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    })
    print("Product added successfully!")


def update_stock(inventory):
    """Update stock quantity for an existing product."""
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product['name']}")
    try:
        print(f"Current Stock: {int(product['stock'])}")
    except (ValueError, TypeError, KeyError):
        print("Error: Current stock value is corrupted.")
        return

    stock_input = input("New Stock Quantity: ").strip()
    if not stock_input.isdigit():
        print("Error: Invalid stock quantity. Please enter a valid integer.")
        return
    new_stock = int(stock_input)
    if new_stock <= 0:
        print("Error: Stock quantity must be a positive integer.")
        return
    if new_stock > 500:
        print("Error: Stock quantity exceeds maximum limit of 500.")
        return

    product["stock"] = new_stock
    print("Stock updated successfully!")


def search_product(inventory):
    """Search for a product by ID and display its details."""
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("------------------------------------------------")
    try:
        price = float(product["price"])
        stock = int(product["stock"])
        print(f"ID: {product['id']}")
        print(f"Name: {product['name']}")
        print(f"Price: ${price:.2f}")
        print(f"Stock: {stock}")
    except (KeyError, ValueError, TypeError):
        print(f"Error: Product entry is corrupted: {product}")
    print("------------------------------------------------")


def display_menu():
    """Print the menu options."""
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        try:
            option = input("Enter option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print("Saving inventory before exit...")
            if save_inventory(inventory, INVENTORY_FILE):
                print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("Saving inventory...")
            if save_inventory(inventory, INVENTORY_FILE):
                print(f"Inventory saved successfully to {INVENTORY_FILE}.")
            else:
                print("Failed to save inventory.")
        elif option == "6":
            print("Saving inventory before exit...")
            if save_inventory(inventory, INVENTORY_FILE):
                print("Inventory saved successfully.")
            else:
                print("Failed to save inventory.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
