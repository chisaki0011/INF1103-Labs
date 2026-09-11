print("Welcome to Smart Invertory Management System")
print("Please select an option:")
print("1. Add Item")
print("2. Remove Item - not working at the moment")
print("3. View Inventory")
print("4. Exit")

item_name = ""
quantity = 0

while True:
    user_choice = input("Enter your choice (1-4): ")
    if user_choice == '1':
        item_name = input("Enter the name of the item to add: ")
        quantity = int(input("Enter the quantity of the item: "))
        if quantity <= 0:
            print("Quantity must be a positive integer.")
        elif quantity > 500:
            print("Quantity exceeds the maximum limit of 500.")
        elif not item_name.isalpha():
            print("Item name must contain only alphabetic characters.")
        else:
            print(f"Added {quantity} of {item_name} to inventory.")

    elif user_choice == '3':    
        # Code to view the inventory
        print("Viewing inventory...")
        print(f"{item_name}: {quantity} units")

    elif user_choice == '4':
        print("Exiting the system. Goodbye!")
        break

    else:
        print("Invalid choice. Please select a valid option (1-4).")
