"""
Inventory Management System - Main Application (Lab 8)
======================================================

This is the main application entry point that ties everything together.

Architecture:
- product.py           : abstract Product base class (common data/state)
- physical_product.py  : PhysicalProduct - adds weight, can be shipped
- digital_product.py   : DigitalProduct - adds download size
- can_be_shipped.py    : CanBeShipped interface (shipping contract)
- supplier.py          : Supplier details associated with products
- order.py             : Orders and the order lines they own
- product_factory.py   : rebuilds the right subclass when loading JSON
- inventory.py         : handles the collection of products
- functions.py         : file I/O, input validation, display operations
- app.py               : main CLI menu and user interaction flow

According to the Single Responsibility Principle and Separation of Concerns:
- Product classes ONLY manage their own data/state
- Inventory manages the collection of Product objects
- Helper functions handle file I/O, prompts, and displays
- This app.py module handles the main menu and orchestrates everything
"""

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from supplier import Supplier
import functions as fn


def main():
    """Main entry point for the application."""

    # Instantiate Inventory object (manages collection of Product objects)
    inventory = Inventory()

    # Load existing inventory from file if it exists
    loaded_products = fn.load_inventory()

    if loaded_products:
        for product_dict in loaded_products:
            # add_product() rebuilds the right subclass from the 'type' field
            # and checks for duplicate IDs. A corrupt record is skipped so one
            # bad entry cannot stop the whole system from starting.
            try:
                inventory.add_product(product_dict)
            except (TypeError, ValueError, KeyError) as error:
                print(f"Warning: skipping invalid product record ({error}).")

    print("Welcome to the Inventory Management System!")
    print("=" * 50)

    while True:
        display_menu()

        choice = input("Enter your choice (1-6 or 'q' to quit): ").strip()

        if choice.lower() == 'q':
            # Quit without saving (menu option 'q')
            print("\nQuitting without saving.")
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

        elif choice == '6':
            # Exit and auto-save
            print("\nSaving inventory before exit...")
            if fn.save_inventory(inventory):
                print("Inventory saved successfully.")
            else:
                print("Warning: Could not save inventory. Data may be lost!")

            print("\nThank you for using Inventory Management System.")
            print("=" * 50 + "\n")
            break

        else:
            print("\nInvalid choice! Please enter a number between 1-6 or 'q'.")


def option_1_display_all(inventory):
    """Handle menu option 1: Display All Products."""
    print()
    inventory.display_all()
    input("\nPress Enter to continue...")


def option_2_add_product(inventory):
    """Handle menu option 2: Add New Product.

    The user chooses between a physical and a digital product, then enters
    the extra information that product type requires. The correct subclass
    is created here, so Inventory never needs to know the difference.
    """
    print("\n--- Add New Product ---\n")

    product_id = input("Enter Product ID: ").strip()
    if not product_id:
        print("\nError: Product ID cannot be empty.")
        input("Press Enter to continue...")
        return

    name = input("Enter Product Name: ").strip()
    if not name:
        print("\nError: Product name cannot be empty.")
        input("Press Enter to continue...")
        return

    # Shared attributes - validated helpers from functions.py
    price = fn.get_valid_price()
    stock = fn.get_valid_stock()

    supplier_id = input("Enter Supplier ID: ").strip()
    supplier_name = input("Enter Supplier Name: ").strip()
    supplier_email = input("Enter Supplier Contact Email: ").strip()
    if not supplier_id or not supplier_name or not supplier_email:
        print("\nError: Supplier ID, name, and email cannot be empty.")
        input("Press Enter to continue...")
        return
    supplier = Supplier(supplier_id, supplier_name, supplier_email)

    print("\nProduct type:")
    print("  1. Physical product (has a weight and can be shipped)")
    print("  2. Digital product (has a download size)")
    type_choice = input("Choose type (1 or 2): ").strip()

    if type_choice == "1":
        weight = fn.get_valid_weight()
        product = PhysicalProduct(
            product_id, name, price, stock, weight, supplier=supplier
        )

    elif type_choice == "2":
        download_size = fn.get_valid_download_size()
        product = DigitalProduct(
            product_id, name, price, stock, download_size, supplier=supplier
        )

    else:
        print("\nError: Invalid product type. Please choose 1 or 2.")
        input("Press Enter to continue...")
        return

    inventory.add_product(product)

    input("\nPress Enter to continue...")


def option_3_update_stock(inventory):
    """Handle menu option 3: Update Stock for Product."""
    print("\n--- Update Stock ---\n")

    product_id = input("Enter Product ID: ").strip()

    if inventory.search_product(product_id) is None:
        input("Press Enter to continue...")
        return

    try:
        stock_str = input("Enter new stock quantity: ").strip()
        new_stock = int(stock_str)
        if new_stock < 0:
            raise ValueError
    except ValueError:
        print("\nError: Invalid stock quantity.")
        input("Press Enter to continue...")
        return

    inventory.update_stock_for_product(product_id, new_stock)
    input("\nPress Enter to continue...")


def option_4_search(inventory):
    """Handle menu option 4: Search for Product."""
    print("\n--- Search Product ---\n")

    product_id = input("Enter Product ID to search: ").strip()

    product = inventory.search_product(product_id)

    if product:
        print("\nProduct Found")
        product.display_information()

    input("\nPress Enter to continue...")


def option_5_save_inventory(inventory):
    """Handle menu option 5: Save Inventory to File."""
    print("\n--- Save Inventory ---\n")

    success = fn.save_inventory(inventory)

    if success:
        print("Inventory saved successfully to inventory.json.")
    else:
        print("Failed to save inventory.")

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
