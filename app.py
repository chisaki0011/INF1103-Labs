"""
Inventory Management System - Main Application (Week 5 OOP Refactor)
======================================================================

This is the main application entry point that ties everything together.

Architecture:
- product.py       : Handles individual product data/state (encapsulation)
- inventory.py     : Handles collection of products (inventory management)
- functions.py     : File I/O, input validation, display operations
- app.py           : Main CLI menu and user interaction flow

According to Single Responsibility Principle and Separation of Concerns:
- Product class ONLY manages its own data/state
- Inventory class manages the collection of Product objects
- Helper functions handle file I/O, prompts, and displays
- This app.py module handles the main menu and orchestrates everything
"""

from product import Product
from inventory import Inventory
import functions as fn


def main():
    """Main entry point for the application."""
    
    # Instantiate Inventory object (manages collection of Product objects)
    inventory = Inventory()
    
    # Load existing inventory from file if exists
    loaded_products = fn.load_inventory()
    
    if loaded_products:
        for product_dict in loaded_products:
            # Add each product to Inventory - duplicate checking is handled by Inventory.add_product()
            inventory.add_product(product_dict)  # add_product checks for duplicates
    
    print("Welcome to the Inventory Management System!")
    print("=" * 50)
    
    while True:
        display_menu()
        
        choice = input("Enter your choice (1-6 or 'q' to quit): ").strip()
        
        if choice.lower() == 'q':
            # Save inventory before exiting
            success = fn.save_inventory(inventory)
            if success:
                print("\nInventory saved successfully!")
            else:
                print("\nWarning: Could not save inventory. Data may be lost!")
            
            print("\nThank you for using Inventory Management System.")
            print("=" * 50 + "\n")
            break
        
        # Handle menu options by calling Inventory object methods
        if choice == '1':
            option_1_display_all(inventory)
            
        elif choice == '2':
            option_2_add_product(inventory)
            
        elif choice == '3':
            option_3_update_stock(inventory)
            
        elif choice == '4':
            option_4_search(inventory)
            
        elif choice == '5':
            option_5_save_inventory(inventory)
            
        else:
            print("\nInvalid choice! Please enter a number between 1-6.\n")


def option_1_display_all(inventory):
    """Handle menu option 1: Display All Products."""
    inventory.display_all()
    input("\nPress Enter to continue...")


def option_2_add_product(inventory):
    """Handle menu option 2: Add New Product."""
    print("\n--- Add New Product ---\n")
    
    product_id = input("Enter Product ID: ").strip()
    name = input("Enter Product Name: ").strip()
    try:
        price_str = input("Enter Price (e.g., 99.99): ").strip()
        price = float(price_str)
    except ValueError:
        print("\nError: Invalid price format.")
        input("Press Enter to continue...")
        return
    
    try:
        stock_str = input("Enter Stock Quantity: ").strip()
        stock = int(stock_str)
    except ValueError:
        print("\nError: Invalid stock quantity.")
        input("Press Enter to continue...")
        return
    
    # Create dictionary for Product initialization
    product_dict = {
        'id': product_id,
        'name': name,
        'price': price,
        'stock': stock
    }
    
    # Add product through Inventory object (which validates and checks duplicates)
    success = inventory.add_product(product_dict)
    
    if success:
        input("\nPress Enter to continue...")


def option_3_update_stock(inventory):
    """Handle menu option 3: Update Stock for Product."""
    print("\n--- Update Stock ---\n")
    
    product_id = input("Enter Product ID: ").strip()
    
    if inventory.search_product(product_id) is None:
        input("Press Enter to continue...")
        return
    
    try:
        quantity_str = input("Enter quantity to add: ").strip()
        quantity = int(quantity_str)
    except ValueError:
        print("\nError: Invalid quantity.")
        input("Press Enter to continue...")
        return
    
    success = inventory.update_stock_for_product(product_id, quantity)
    
    if not success:
        input("Press Enter to continue...")


def option_4_search(inventory):
    """Handle menu option 4: Search for Product."""
    print("\n--- Search Product ---\n")
    
    product_id = input("Enter Product ID to search: ").strip()
    
    product = inventory.search_product(product_id)
    
    if product:
        product.display_information()
    
    input("\nPress Enter to continue...")


def option_5_save_inventory(inventory):
    """Handle menu option 5: Save Inventory to File."""
    print("\n--- Save Inventory ---\n")
    
    # Save inventory using helper function
    success = fn.save_inventory(inventory)
    
    if success:
        print("✓ Inventory saved successfully!")
    else:
        print("✗ Failed to save inventory.")
    
    input("\nPress Enter to continue...")


def display_menu():
    """Print the menu options.
    
    This function is called every time the user returns to the menu
    after performing an operation. It follows the Single Responsibility
    Principle by only displaying the menu, not processing any options.
    """
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit (auto-save)")
    print("q - Quit without saving")
    print("=" * 31)


if __name__ == "__main__":
    main()
