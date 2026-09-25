# persistent_auditor.py 
# Starting from scratch. 
# program will read a file of orders, display them, and allow the user to add a new order. 
# The new order will be validated and appended to the file.

ORDERS_FILE = "orders.txt"


def read_orders(filename):
    """Read file into a list. Returns list of non-empty lines."""
    try:
        with open(filename, "r") as file:
            order_lines = file.readlines()
    except FileNotFoundError:
        return []
    return [line.strip() for line in order_lines if line.strip()]


def get_max_id(order_lines):
    """Get max order id from list. Returns 1000 if list is empty."""
    order_ids = []
    for line in order_lines:
        parts = line.split(",")
        if len(parts) != 3:
            continue
        try:
            order_ids.append(int(parts[0].strip()))
        except ValueError:
            continue
    if len(order_ids) == 0:
        return 1000
    return max(order_ids)


def generate_new_id(max_id):
    """Generate next order id."""
    return max_id + 1


def get_valid_item_name(prompt="Enter item name: "):
    """Validate: non-empty, letters/spaces only."""
    while True:
        item_name = input(prompt).strip()
        if not item_name:
            print("Item name cannot be empty.")
            continue
        if not item_name.replace(" ", "").isalpha():
            print("Item name must contain only letters and spaces.")
            continue
        return item_name


def get_valid_quantity(prompt="Enter quantity: "):
    """Validate: positive integer, max 500."""
    while True:
        user_input = input(prompt).strip()
        if not user_input.isdigit():
            print("Quantity must be a positive integer.")
            continue
        quantity = int(user_input)
        if quantity <= 0:
            print("Quantity must be a positive integer.")
            continue
        if quantity > 500:
            print("Quantity exceeds maximum limit of 500.")
            continue
        return quantity


def append_order(filename, new_id, item_name, quantity):
    """Append one order using append mode. Returns the order line."""
    order_line = f"{new_id},{item_name},{quantity}\n"
    with open(filename, "a") as file:
        file.write(order_line)
    return order_line.strip()


def display_orders(order_lines):
    """Loop through list and display each order."""
    if not order_lines:
        print("No orders found.")
        return
    print(f"\nTotal orders: {len(order_lines)}")
    for line in order_lines:
        print(line)


def main():
    # Input: open + read file into list (array)
    order_lines = read_orders(ORDERS_FILE)
    print(f"Loaded {len(order_lines)} order(s) from {ORDERS_FILE}.")
    display_orders(order_lines)

    # Process: get max id -> generate new id
    max_id = get_max_id(order_lines)
    new_id = generate_new_id(max_id)
    print(f"\nMax order id: {max_id}, new order id: {new_id}")

    # Input: get one new order (validated)
    print("\nEnter new order details:")
    item_name = get_valid_item_name()
    quantity = get_valid_quantity()

    # Output: append + write to file
    new_order = append_order(ORDERS_FILE, new_id, item_name, quantity)
    print(f"Appended: {new_order}")

    # Verify: re-read and display
    updated_orders = read_orders(ORDERS_FILE)
    display_orders(updated_orders)


if __name__ == "__main__":
    main()
