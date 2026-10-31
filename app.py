"""
Inventory Management System - Main Application (Week 5 OOP Refactor)
======================================================================

This is the main application entry point that ties everything together.

Architecture:
- product.py       : Handles individual product data/state (encapsulation)
- functions.py     : File I/O, input validation, display operations
- app.py           : Main CLI menu and user interaction flow

According to Single Responsibility Principle and Separation of Concerns:
- Product class ONLY manages its own data/state
- Helper functions handle file I/O, prompts, and displays
- This app.py module handles the main menu and orchestrates everything
"""

from product import Product
import functions as fn


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
    print("6. Exit")
    print("----------------------------")


def main():
    """Main function that runs the inventory management system.
    
    This is the entry point for the application. It:
    1. Loads existing inventory from file (or starts empty)
    2. Displays the main menu repeatedly until user exits
    3. Processes user input and calls appropriate functions
    
    Following Single Responsibility Principle:
    - This module handles the CLI/menu flow
    - It imports from product.py for Product class operations
    - It imports from functions.py for all other operations
    """
    print("=" * 42)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 42)

    # Load inventory using helper function from functions module
    # This follows the separation of concerns principle
    inventory = fn.load_inventory(fn.INVENTORY_FILE)

    while True:
        display_menu()
        try:
            option = input("Enter option: ").strip()
        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+C gracefully - user pressed interrupt key
            print()  # Print newline for clean output
            print("Saving inventory before exit...")
            # Try to save before exiting
            if fn.save_inventory(inventory, fn.INVENTORY_FILE):
                print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            return

        # Process each menu option
        if option == "1":
            # Display All Products
            print("\n--- DISPLAY ALL PRODUCTS ---")
            fn.display_all(inventory)
            
        elif option == "2":
            # Add Product
            add_new_product = input("Add new product? (y/n): ").strip().lower()
            if add_new_product == "y" or add_new_product == "yes":
                # Use helper function from functions module to add product
                # This prompts for all details and saves automatically
                fn.add_product(inventory)
            else:
                print("Skipping product addition.")
                
        elif option == "3":
            # Update Stock
            print("\n--- UPDATE STOCK ---")
            
            # Get valid product ID from user using validated input function
            product_id = fn.get_valid_product_id(inventory)
            
            if product_id:
                # Use helper function to update stock (encapsulated via Product class)
                fn.update_stock(product_id, inventory)
            else:
                print("No product found for stock update.")
                
        elif option == "4":
            # Search Product
            search_term = input("\nEnter search term (e.g., 'lap' for 'Laptop'): ").strip()
            if search_term:
                # Use helper function to search by name
                fn.search_product(inventory, search_term)
            else:
                print("No search term provided.")
                
        elif option == "5":
            # Save Inventory (manual save)
            save_inventory = input("\nSave inventory now? (y/n): ").strip().lower()
            if save_inventory == "y" or save_inventory == "yes":
                if fn.save_inventory(inventory, fn.INVENTORY_FILE):
                    print("Inventory saved successfully.")
                else:
                    print("Failed to save inventory. Please check disk space and permissions.")
            else:
                print("Skipping manual save.")
                
        elif option in ["6", "q", "quit"]:
            # Exit or quit shortcut
            print("\nQuitting...")
            if fn.save_inventory(inventory, fn.INVENTORY_FILE):
                print("Inventory saved successfully.")
            break
            
        else:
            # Invalid option
            print("\nInvalid option. Please choose 1-6 or 'q' to quit.")

    # Handle EOF (e.g., from pipe input like "echo q | python app.py")
    return


if __name__ == "__main__":
    main()
