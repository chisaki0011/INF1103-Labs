# Week 5: OOP Inventory System Refactor

## Overview

This is a refactored inventory management system using **Object-Oriented Programming (OOP)** principles and proper separation of concerns.

### Key Principles Applied

- **Encapsulation**: Product class uses private attributes (`__product_id`, `__name`, `__price`, `__stock`)
- **Single Responsibility Principle (SRP)**: Each module has one clear purpose
- **Separation of Concerns**: Data/state, logic, and UI are separated into different modules

---

## File Architecture

```
INF1103-Labs/
├── app.py              # Main CLI entry point - handles menu flow
├── product.py          # Product class - manages data/state only
├── functions.py        # Helper functions - file I/O, validation, display
├── inventory.json      # Data file (auto-created on first run)
├── README.md           # This file
└── .gitignore         # Ignores deprecated files (*.pyc, __pycache__, *.bak)
```

---

## Module Responsibilities

### 1. `product.py` - Product Class (Encapsulation)

**Responsibility**: Manage individual product data and state ONLY.

**Key Features**:
- Private attributes using `__prefix` convention
- Getter methods for each attribute (`get_product_id()`, `get_name()`, etc.)
- `update_stock()` method to modify stock quantity
- `display_information()` to show formatted product details
- **Accepts dict parameter in `__init__`** for data initialization

```python
class Product:
    def __init__(self, data: dict):
        """Initialize with dict containing id, name, price, stock."""
        self.__product_id = data["id"]
        self.__name = data["name"]
        self.__price = data["price"]
        self.__stock = data["stock"]
    
    def get_product_id(self):  return self.__product_id
    # ... other getters ...
    
    def update_stock(self, quantity):  # Adds to current stock
        self.__stock += quantity
    
    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} ...")
```

**IMPORTANT**: Product class does NOT handle input prompts or file I/O.

---

### 2. `functions.py` - Helper Functions (File I/O & Validation)

**Responsibility**: Handle all file operations, input validation, and display functions.

**Key Functions**:

| Function | Purpose |
|----------|---------|
| `load_inventory(filename)` | Load inventory from JSON file |
| `save_inventory(inventory, filename)` | Save inventory to JSON file |
| `display_all(inventory)` | Display all products |
| `find_product_by_id(inventory, product_id)` | Find product by ID |
| `search_product(inventory, search_term)` | Search products by name |
| `get_valid_price()` | Prompt for valid price (>= 0) |
| `get_valid_stock()` | Prompt for valid stock quantity (>= 0) |
| `get_valid_product_id(inventory)` | Get validated product ID from user |
| `add_product(inventory)` | Add new product to inventory |
| `update_stock(product_id, inventory)` | Update stock via Product class |

---

### 3. `app.py` - Main Application (CLI Menu)

**Responsibility**: Handle main CLI menu flow and orchestrate operations.

**Key Features**:
- Loads inventory using `fn.load_inventory()`
- Displays menu repeatedly until exit
- Processes user input for each option
- Uses Product class via `from product import Product`
- Imports ALL helper functions from `functions.py` as alias `fn`

---

## Setup Instructions

### Prerequisites

- Python 3.6 or higher (no external packages required)

### Running the Application

1. **Start the system**:
   ```bash
   python app.py
   ```

2. **Menu options**:
   ```
   ----------- MENU -----------
   1. Display All Products
   2. Add Product
   3. Update Stock
   4. Search Product
   5. Save Inventory
   6. Exit
   ----------------------------
   ```

### Example Usage

#### Adding a New Product
```bash
$ python app.py
=============================================
INVENTORY MANAGEMENT SYSTEM
=============================================
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Save Inventory
6. Exit
----------------------------
Enter option: 2
Add new product? (y/n): y
Enter product ID (e.g., P003): P003
Enter product name: Wireless Mouse
Enter price (must be >= 0): 29.99
Enter stock quantity (must be >= 0): 100

Product 'Wireless Mouse' (ID: P003) added successfully!
Inventory saved successfully.
```

#### Updating Stock
```bash
$ python app.py
----------- MENU -----------
...
Enter option: 3

--- UPDATE STOCK ---
Available Product IDs:
  - P001 (Laptop)
  - P002 (Mouse)
  - P003 (Wireless Mouse)

Enter product ID to update: P003
Current stock for 'Wireless Mouse': 100
Enter stock quantity (must be >= 0): 50
Stock updated from 100 to 150
```

---

## Data Format

### `inventory.json` Structure

```json
[
  {
    "id": "P001",
    "name": "Laptop",
    "price": 999.99,
    "stock": 10
  },
  {
    "id": "P002",
    "name": "Mouse",
    "price": 25.50,
    "stock": 50
  }
]
```

**Notes**:
- Created automatically on first run if not exists
- Empty list `[]` if file doesn't exist yet
- All prices stored as floats (JSON converts)
- Stock quantities stored as integers

---

## Class Diagrams

### Product Class Architecture

```
┌─────────────────────────────────┐
│       Product Class             │
├─────────────────────────────────┤
│  __private_attr (encapsulated)  │
│  - __product_id                 │
│  - __name                       │
│  - __price                      │
│  - __stock                      │
├─────────────────────────────────┤
│  + get_product_id() -> str      │
│  + get_name() -> str            │
│  + get_price() -> float         │
│  + get_stock() -> int           │
│                                 │
│  - update_stock(quantity)       │
│  - display_information()        │
└─────────────────────────────────┘

Note: Accepts dict parameter in __init__:
      { "id": "...", "name": "...", 
         "price": ..., "stock": ... }
```

### System Architecture

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│    User     │      │  app.py      │      │ functions.py  │
└──────┬──────┘      └──────┬───────┘      └──────┬────────┘
       │                    │                     │
       │ Menu Display      │ Load/Save           │ File I/O
       │ User Input        │ Display All         │ Validation
       └──────────────────>│                   │
                           │ Product Ops        │ Search
                           └──────────────────> │ CRUD
                                               │
┌─────────────┐                    ┌────────────────────────┐
│ product.py  │◄─── Encapsulation │     inventory.json      │
├─────────────┤                    │                         │
│ - __product_id              └────────────────────────┘
│ - __name                     (Data file)
│ - __price
│ - __stock

Single Responsibility Principle Applied:
- Product: ONLY manages its own data/state
- Functions: Handles all I/O, prompts, validation
- App: Handles main menu flow
```

---

## Deprecated Files

The following files have been refactored and should be ignored:

| File | Status | Reason |
|------|--------|--------|
| `inventory_manager.py` | Deprecated | Refactored into `app.py` |
| `modular_auditor.py` | Deprecated | Functions extracted to `functions.py` |
| `old_persistent_audior.py` | Deprecated | Old implementation, replaced |
| `auditor.py` | Deprecated | Functions moved to `functions.py` |

---

## Testing the Refactor

Run these commands to verify the system works:

```bash
# Test with empty inventory (starts fresh)
python app.py

# Add a test product
echo "6" | python app.py  # Exit after menu display

# Or use a simple test script
python -c "
from product import Product
p = Product({'id': 'P001', 'name': 'Test', 'price': 9.99, 'stock': 5})
print(f'Product: {p.display_information()}')
"
```

---

## Git Workflow

### Adding New Files

```bash
# Add all new files to git
git add app.py product.py functions.py README.md .gitignore

# Commit the refactoring
git commit -m "Week 5: Refactor to OOP with separation of concerns

- Created Product class with encapsulated attributes
- Moved helper functions to separate functions.py module
- Refactored inventory_manager.py into app.py (CLI entry point)
- Added .gitignore for deprecated files (.pyc, __pycache__, *.bak)
- Updated README.md with architecture documentation"

# Push to remote repository
git push origin main
```

---

## Best Practices Followed

1. **Encapsulation**: All attributes prefixed with `__` in Product class
2. **Single Responsibility Principle**: Each module has one clear purpose
3. **Separation of Concerns**: Data, logic, and UI separated
4. **Beginner-friendly comments**: Added throughout code
5. **Type hints**: Used where appropriate for clarity

---

## Next Steps

- Test the system with various inputs
- Add unit tests for Product class methods
- Consider adding input validation at app level
- Document all edge cases in README.md
