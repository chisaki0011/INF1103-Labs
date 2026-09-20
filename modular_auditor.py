def get_valid_input(prompt):
    """Handles the prompt, handles input validation, and returns a valid integer or a 'quit' signal.
    Args:
        prompt (str): The message shown to the user.
    Returns:
        Union[int, str]: The number as an integer, or 'quit' as a string.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'quit':
            return 'quit'
        if user_input.isdigit():
            return int(user_input)
        print("Invalid input. Please enter a valid number or 'quit'.")

def process_delivery(current_total, new_value):
    """Calculates the new total and returns it.
    Args:
        current_total (int): The current total inventory.
        new_value (int): The delivery amount.
    Returns:
        int: The updated total inventory.
    """
    return current_total + new_value

def calculate_tax(amount):
    """Calculates the tax for a delivery (10% of the delivery value).
    Args:
        amount (int): The delivery amount.
    Returns:
        float: The tax amount.
    """
    return amount * 0.1

def generate_report(total_units, failed_attempts):
    """Prints the final summary of deliveries processed and failed/rejected entries.
    Args:
        total_units (int): Total deliveries processed.
        failed_attempts (int): Number of failed/rejected entries.
    """
    print(f"\nTotal Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

def add_item(inventory_total, deliveries_processed, failed_attempts):
    """Modularizes the 'Add Item' menu option.
    Args:
        inventory_total (int): Current total inventory.
        deliveries_processed (int): Number of successful deliveries so far.
        failed_attempts (int): Number of rejected entries so far.
    Returns:
        tuple: (inventory_total, deliveries_processed, failed_attempts, should_exit)
    """
    item_name = input("Enter the name of the item to add: ").strip()
    stock_quantity = get_valid_input("Enter the quantity of the item: ")

    if stock_quantity == 'quit':
        return inventory_total, deliveries_processed, failed_attempts, True
    if not item_name.isalpha():
        print("Item name must contain only alphabetic characters.")
        failed_attempts += 1
    elif stock_quantity <= 0:
        print("Quantity must be a positive integer.")
        failed_attempts += 1
    elif stock_quantity > 500:
        print("Quantity exceeds the maximum limit of 500.")
        failed_attempts += 1
    else:
        inventory_total = process_delivery(inventory_total, stock_quantity)
        tax = calculate_tax(stock_quantity)
        deliveries_processed += 1
        print(f"Added {stock_quantity} of {item_name} to inventory. Tax: {tax:.2f}. Inventory Total: {inventory_total}")

    return inventory_total, deliveries_processed, failed_attempts, False

def view_inventory(inventory_total):
    """Prints the current inventory.
    Args:
        inventory_total (int): Current total inventory.
    """
    if inventory_total > 0:
        print(f"Current Inventory: {inventory_total} units")
    else:
        print("No items in inventory.")

# Initialize the inventory to zero
inventory_total = 0
deliveries_processed = 0
failed_attempts = 0

print("Welcome to Smart Invertory Management System")

while True:
    print("Please select an option:")
    print("1. Add Item")
    print("2. Remove Item - not working at the moment")
    print("3. View Inventory")
    print("4. Exit")

    user_choice = get_valid_input("Enter your choice (1-4 or 'quit'): ")

    if user_choice == 'quit':
        generate_report(deliveries_processed, failed_attempts)
        print("Exiting the system. Goodbye!")
        break
    elif user_choice == 1:
        inventory_total, deliveries_processed, failed_attempts, should_exit = add_item(inventory_total, deliveries_processed, failed_attempts)
        if should_exit:
            generate_report(deliveries_processed, failed_attempts)
            print("Exiting the system. Goodbye!")
            break
    elif user_choice == 2:
        print("Remove Item - not working at the moment")
    elif user_choice == 3:
        view_inventory(inventory_total)
    elif user_choice == 4:
        generate_report(deliveries_processed, failed_attempts)
        print("Exiting the system. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option (1-4 or 'quit').")