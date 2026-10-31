from persistent_auditor import *

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
