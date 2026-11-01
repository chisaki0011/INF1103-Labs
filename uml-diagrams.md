# UML Class Diagrams - Week 8 OOP Inventory System (Lab 6)

## Overview

This document contains the UML class diagrams for the Inventory Management
System after the Week 8 OOP refactor. The system uses two classes:

- `Product` - represents and manages **one** product.
- `Inventory` - manages a **collection** of `Product` objects.

File handling and the menu live outside both classes, following the Single
Responsibility Principle (Lab 6, Sections 2.5 and 2.8).

---

## Class 1: `Product`

### Summary

Represents a single product in the inventory system with encapsulated
attributes and state-management methods.

### UML Diagram

```
┌──────────────────────────────────┐
│             Product              │
├──────────────────────────────────┤
│ - __product_id : str             │
│ - __name : str                   │
│ - __price : float                │
│ - __stock : int                  │
├──────────────────────────────────┤
│ + __init__(product_id, name,     │
│            price, stock)          │
│ + update_stock(quantity: int)     │
│ + display_information()           │
│ + get_product_id() : str          │
│ + get_name() : str                │
│ + get_price() : float             │
│ + get_stock() : int               │
│ + to_dict() : dict                │
│ + __str__() : str                 │
└──────────────────────────────────┘
```

### Attributes (private - encapsulation)

| Attribute | Type | Description |
|-----------|------|-------------|
| `__product_id` | `str` | Unique product identifier |
| `__name` | `str` | Product name |
| `__price` | `float` | Product price |
| `__stock` | `int` | Current stock quantity |

### Public methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `__init__(product_id, name, price, stock)` | Lab-style constructor. Also accepts a single dictionary (used for JSON loading). | `product_id` (str \| dict), `name` (str), `price` (float), `stock` (int) | None |
| `update_stock(quantity)` | Sets the stock to `quantity`; rejects negative values. | `quantity` (int) | None |
| `display_information()` | Prints a formatted product line. | - | `str` |
| `get_product_id()` | Returns the ID. | - | `str` |
| `get_name()` | Returns the name. | - | `str` |
| `get_price()` | Returns the price. | - | `float` |
| `get_stock()` | Returns the current stock. | - | `int` |
| `to_dict()` | Returns a JSON-serialisable dictionary. | - | `dict` |
| `__str__()` | Returns a readable representation. | - | `str` |

### Encapsulation

External code never touches the private attributes. For example:

```python
product.update_stock(50)      # correct - controlled by the class
product.__stock = 50          # wrong - silently creates a new attribute
product._Product__stock = 50  # name-mangled escape hatch - do not use
```

---

## Class 2: `Inventory`

### Summary

Manages a collection of `Product` objects. Delegates file I/O to
`functions.py` and user interaction to `app.py`.

### UML Diagram

```
┌──────────────────────────────────┐
│            Inventory             │
├──────────────────────────────────┤
│ - _products : list[Product]      │
├──────────────────────────────────┤
│ + __init__()                     │
│ + add_product(product) : bool    │
│ + search_product(product_id)     │
│ + display_all()                  │
│ + update_stock_for_product(      │
│       product_id, new_stock)     │
│ + get_all_products() : list      │
│ + to_dict_list() : list[dict]    │
└──────────────────────────────────┘
```

### Public methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `__init__()` | Creates an empty inventory. | - | None |
| `add_product(product)` | Adds a `Product` (or dict) after a duplicate-ID check. | `product` (Product \| dict) | `bool` |
| `search_product(product_id)` | Finds a product by ID. | `product_id` (str) | `Product \| None` |
| `display_all()` | Displays every product. | - | None |
| `update_stock_for_product(product_id, new_stock)` | Finds a product and sets its stock. | `product_id` (str), `new_stock` (int) | `bool` |
| `get_all_products()` | Returns a copy of the product list. | - | `list[Product]` |
| `to_dict_list()` | Returns the collection as JSON-ready dicts. | - | `list[dict]` |

---

## Module Structure

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  product.py  │◄────►│ inventory.py │◄────►│ functions.py │
│  Product     │      │  Inventory   │      │  File I/O    │
└──────────────┘      └──────────────┘      └──────────────┘
                             ▲
                             │ uses
                             ▼
                      ┌──────────────┐
                      │    app.py    │
                      │ Menu / CLI   │
                      └──────────────┘
                             │
                             ▼
                      inventory.json
```

| Module | Responsibility |
|--------|----------------|
| `product.py` | Stores product information and manages its own state |
| `inventory.py` | Stores, adds, searches and displays products |
| `functions.py` | Loads and saves `inventory.json`; input helpers |
| `app.py` | Displays the menu, gets user input, calls Inventory methods |

---

## Relationships

### Composition (strong)

- An `Inventory` **contains** multiple `Product` objects.
- Products are created in `app.py` or by `Inventory.add_product()` when loading
  from JSON, then stored in `Inventory._products`.
- A product only exists as part of the inventory collection.

### Dependency

- `Inventory` depends on `Product`.
- `functions.save_inventory()` depends on `Product.to_dict()` (via duck typing).
- `app.py` depends on `Inventory`, `Product` and `functions`.

---

## Usage Flow Example (matches Lab 6, Sections 2.6 and 2.7)

```python
from product import Product
from inventory import Inventory

# 1. Create the inventory object
inventory = Inventory()

# 2. Create Product objects - lab-style constructor
product1 = Product("P001", "Laptop", 1200.00, 15)
product2 = Product("P002", "Mouse", 25.50, 40)

# 3. Pass the objects to the Inventory
inventory.add_product(product1)
inventory.add_product(product2)

# 4. Display, search, update
inventory.display_all()
product = inventory.search_product("P001")
if product:
    product.display_information()

inventory.update_stock_for_product("P001", 20)

# 5. Save through the file-handling module
import functions as fn
fn.save_inventory(inventory)
```

---

## Design Principles Applied

### Single Responsibility Principle (SRP)

- **Product** - only represents/manages one product.
- **Inventory** - only manages the collection of products.
- **functions** - only handles file I/O and input/display helpers.
- **app.py** - only handles the menu and user flow.

### Encapsulation

- `Product` uses private attributes (`__product_id`, `__name`, `__price`, `__stock`).
- `Inventory` uses a private collection (`_products`).
- Access is only through public methods/getters; `to_dict()` is the only
  controlled way to serialise a product.

### Separation of Concerns

- Data layer: `Product`
- Collection layer: `Inventory`
- Persistence layer: `functions`
- Presentation/orchestration layer: `app.py`

---

## Lab 6 Requirement Checklist

| Requirement | Location |
|-------------|----------|
| Product class with four private attributes | `product.py` |
| `__init__` constructor | `product.py` |
| `update_stock(quantity)` | `product.py` |
| `display_information()` | `product.py` |
| Encapsulation via `__` attributes and getters | `product.py` |
| Product has no file I/O, menu or input code | `product.py` |
| Inventory class holding Product objects | `inventory.py` |
| `add_product()`, `search_product()`, `display_all()` | `inventory.py` |
| Program refactored from dicts to objects | `app.py` |
| All six menu options | `app.py` |
