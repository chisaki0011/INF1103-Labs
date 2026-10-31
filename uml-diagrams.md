# UML Class Diagrams - Week 5 OOP Refactor

## Overview
This document contains UML class diagrams for the Inventory Management System after Week 5 refactoring. The system now uses Object-Oriented Programming with Product and Inventory classes following the Single Responsibility Principle.

---

## Class 1: `Product`

### Summary
Represents a single product in the inventory system with encapsulated attributes and state management methods.

### UML Diagram

```
┌─────────────────────────────┐
│      Product                │
│  ┌─────────────────────────┐│
│  │ - __product_id: str     ││  Private attributes (encapsulation)
│  │ - __name: str           ││
│  │ - __price: float        ││
│  │ - __stock: int          ││
│  └─────────────────────────┘│
├─────────────────────────────┤
│  + get_product_id() → str   │  Public getter methods
│  + get_product_name() → str │
│  + get_product_price() → float│
│  + get_stock() → int        │
├─────────────────────────────┤
│  + update_stock(newStock)   │  State management methods
│  + display_information()     │
├─────────────────────────────┤
│  + __init__(product_dict)   │  Constructor accepting dict parameter
└─────────────────────────────┘
```

### Attributes (Private - Encapsulation)
- `__product_id` : str - Unique product identifier
- `__name` : str - Product name/description
- `__price` : float - Product price in currency
- `__stock` : int - Current stock quantity

### Public Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `__init__(product_dict)` | Constructor that accepts dictionary with keys: id, name, price, stock | product_dict (dict) | None |
| `get_product_id()` | Get product ID (no direct access to private attribute) | - | str |
| `get_product_name()` | Get product name | - | str |
| `get_product_price()` | Get product price | - | float |
| `get_stock()` | Get current stock quantity | - | int |
| `update_stock(newStock)` | Update stock to new value (sets private attribute) | newStock (int) | None |
| `display_information()` | Display all product information in formatted output | - | None |

---

## Class 2: `Inventory`

### Summary
Manages a collection of Product objects with methods for adding, searching, and displaying products. Handles inventory operations but delegates file I/O to functions module.

### UML Diagram

```
┌─────────────────────────────────┐
│       Inventory                 │
│  ┌─────────────────────────────┐│
│  │ - _products: list[Product]  ││  Private collection of Product objects
│  └─────────────────────────────┘│
├─────────────────────────────────┤
│  + add_product(product_dict)    │  Add new product to inventory
│  + search_product(product_id)   │  Search for product by ID
│  + display_all()                │  Display all products in collection
├─────────────────────────────────┤
│  + update_stock_for_product()   │  Update stock for specific product
│  + get_all_products()           │  Return copy of products list
└─────────────────────────────────┘
```

### Attributes (Private)
- `_products` : `list[Product]` - Collection of Product objects

### Public Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `__init__()` | Initialize empty inventory collection | - | None |
| `add_product(product_dict)` | Add new product after validation and duplicate check | product_dict (dict) | bool |
| `search_product(product_id)` | Search for product by ID | product_id (str) | Product \| None |
| `display_all()` | Display all products in collection | - | None |
| `update_stock_for_product(id, qty)` | Update stock for specific product | id (str), qty (int) | bool |
| `get_all_products()` | Return copy of products list | - | list[Product] |

---

## Module Structure

```
┌──────────────┐      ┌─────────────┐      ┌──────────┐
│ product.py   │◄────►│  Inventory  │◄────►│ functions │
│ Product Class│      │             │       │            │
└──────────────┘      │ Collection  │◄────►│ Helper     │
                      │ Management  │      │ Functions  │
                      └─────────────┘      └────────────┘
                               ▲
                               │ Uses
                               ▼
┌──────────────────────────────────────┐
│              app.py                  │
│    Main CLI / Menu Orchestrator      │
└──────────────────────────────────────┘

Data File: inventory.json
Format: List of dictionaries, one per product:
  [{"id": "...", "name": "...", "price": ..., "stock": ...}, ...]
```

---

## Relationships

### Composition (Strong)
- **Inventory** contains multiple **Product** objects
- Product objects are created by Inventory when added via `add_product()`
- Lifecycle: Products exist only as long as they're in the inventory collection

### Dependency
- **Inventory** depends on **functions** module for validation utilities
- **Product** uses data from dictionaries provided by **functions** module
- **app.py** orchestrates and calls methods on both classes

---

## Usage Flow Example

```python
# 1. Create Inventory instance
inventory = Inventory()

# 2. Load existing inventory (handled in main())
loaded_products = fn.load_inventory()
for product_dict in loaded_products:
    inventory.add_product(product_dict)

# 3. Display all products
inventory.display_all()

# 4. Add new product
new_product = {
    'id': 'P001',
    'name': 'Laptop',
    'price': 999.99,
    'stock': 5
}
inventory.add_product(new_product)

# 5. Search for product
product = inventory.search_product('P001')
if product:
    product.display_information()

# 6. Update stock
inventory.update_stock_for_product('P001', 10)

# 7. Save inventory
fn.save_inventory(inventory)
```

---

## Design Principles Applied

### Single Responsibility Principle (SRP)
- **Product**: ONLY manages its own data/state
- **Inventory**: ONLY manages collection of Product objects
- **functions**: ONLY handles file I/O, validation, displays
- **app.py**: ONLY handles menu display and user interaction flow

### Encapsulation
- Product uses private attributes (`__product_id`, `__name`, etc.)
- Inventory uses private attribute (`_products`)
- Access only through public getter/setter methods
- No direct access to private members from outside class

### Separation of Concerns
- Data layer: Product class
- Collection layer: Inventory class  
- I/O layer: functions module
- Presentation/Orchestration layer: app.py

---

## Files Created/Modified in Week 5 Refactor

| File | Purpose | Notes |
|------|---------|-------|
| `product.py` | Product class implementation | Encapsulated attributes, getter methods |
| `inventory.py` | Inventory class implementation | Collection management methods |
| `functions.py` | Helper functions | Moved from persistent_auditor.py |
| `app.py` | Main application entry point | Uses all three modules |

---

## Next Steps for Completion

1. Commit inventory.py with descriptive message
2. Commit updated app.py with descriptive message
3. Test all 6 menu options work correctly
4. Create UML diagrams (this document)
5. Update README.md with new architecture
6. Push changes to GitHub
7. Generate git log > log.txt for submission
