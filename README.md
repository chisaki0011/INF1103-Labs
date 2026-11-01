# INF1103 Inventory Management System

This repository contains the Week 5 (functional) inventory system and its
Week 8 (object-oriented) refactor.

- **Week 5 / Lab 5** - dictionaries, functions and JSON persistence.
- **Week 8 / Lab 6** - the same system refactored into `Product` and
  `Inventory` classes using encapsulation and the Single Responsibility
  Principle.

---

## Project Structure

```
INF1103-Labs/
├── app.py                 # Week 8 OOP entry point - menu and user flow
├── product.py             # Product class - one product's data/state
├── inventory.py           # Inventory class - collection of Product objects
├── functions.py           # File I/O (load/save) and input/display helpers
├── inventory.json         # Persistent inventory data (4 products)
├── inventory_manager.py   # Week 5 functional entry point (legacy)
├── persistent_auditor.py  # Week 5 functions (load/save/CRUD) (legacy)
├── Dockerfile             # Container image definition
├── uml-diagrams.md        # UML class diagrams for Product and Inventory
├── reflection.md          # Answers to the Lab 6 reflection questions
├── log.txt                # Git history for submission
└── README.md              # This file
```

> `auditor.py`, `modular_auditor.py`, `old_persistent_auditor.py` and
> `hello.py` are earlier-week files kept for history but ignored by git
> (see `.gitignore`).

---

## Running the Week 8 OOP System

No third-party packages are required (Python 3.6+).

```bash
python app.py
```

Menu:

```
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Save Inventory
6. Exit (auto-save)
q - Quit without saving
===========================
```

- Options **1-5** perform the operation and return to the menu.
- Option **6** saves `inventory.json` and exits.
- `q` exits **without** saving.

### Example session

```
inventory.json found.
Inventory loaded successfully.
Welcome to the Inventory Management System!
...
Enter your choice (1-6 or 'q' to quit): 1

Current Inventory
------------------------------------------------
ID: P001 | Name: Laptop | Price: $1200.00 | Stock: 15
ID: P002 | Name: Mouse | Price: $25.50 | Stock: 40
ID: P003 | Name: Keyboard | Price: $45.00 | Stock: 25
ID: P004 | Name: Earpiece | Price: $29.90 | Stock: 100
------------------------------------------------
```

---

## Running the Week 5 Functional System (Legacy)

```bash
python inventory_manager.py
```

This uses `persistent_auditor.py` and the Week 5 dictionary/list design.

---

## Class Design (Week 8)

### `Product` (`product.py`)

Responsible for **one** product only.

```python
class Product:
    def __init__(self, product_id, name=None, price=None, stock=None):
        # Accepts Product("P001", "Laptop", 1200.0, 15)
        # or Product({"id": "P001", "name": "Laptop", ...}) when loading JSON
        ...

    def update_stock(self, quantity): ...
    def display_information(self): ...
    def get_product_id(self): ...
    def get_name(self): ...
    def get_price(self): ...
    def get_stock(self): ...
    def to_dict(self): ...
```

Private attributes (`__product_id`, `__name`, `__price`, `__stock`) are only
changed through `update_stock()`. The class contains **no** file I/O, menu or
`input()` code.

### `Inventory` (`inventory.py`)

Responsible for a **collection** of `Product` objects.

```python
class Inventory:
    def __init__(self): ...
    def add_product(self, product): ...          # accepts Product or dict
    def search_product(self, product_id): ...
    def display_all(self): ...
    def update_stock_for_product(self, product_id, new_stock): ...
    def get_all_products(self): ...
    def to_dict_list(self): ...
```

### `functions.py`

Handles persistence and input helpers:

| Function | Purpose |
|----------|---------|
| `load_inventory(filename)` | Load JSON and return a list of dictionaries |
| `save_inventory(inventory, filename)` | Save an `Inventory` object or list of products |
| `display_all(inventory)` | Display products (objects or dictionaries) |
| `get_valid_price()` / `get_valid_stock()` | Validated prompts |

### `app.py`

Displays the menu, reads user input and calls `Inventory` methods. It never
touches a product's private attributes.

See `uml-diagrams.md` for the full UML diagrams.

---

## Data Format

`inventory.json` is a list of product dictionaries:

```json
[
  { "id": "P001", "name": "Laptop",   "price": 1200.0, "stock": 15 },
  { "id": "P002", "name": "Mouse",    "price": 25.5,   "stock": 40 },
  { "id": "P003", "name": "Keyboard", "price": 45.0,   "stock": 25 },
  { "id": "P004", "name": "Earpiece", "price": 29.9,   "stock": 100 }
]
```

If the file is missing or invalid, the program starts with an empty inventory.

---

## Docker

Build the image (only needed when the `Dockerfile` or dependencies change):

```bash
docker build -t inf1103-labs-smart-auditor .
```

Run the Week 8 OOP system with a volume mount so `inventory.json` persists on
the host:

```bash
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-labs-smart-auditor
```

Run the Week 5 functional system instead:

```bash
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-labs-smart-auditor python inventory_manager.py
```

The volume mount means you can edit the Python files locally and re-run the
container without rebuilding the image.

---

## Testing Checklist

| Menu option | Verified behaviour |
|-------------|--------------------|
| 1 - Display All Products | Loads `inventory.json` and prints every product |
| 2 - Add Product | Creates a `Product` object; duplicate IDs are rejected |
| 3 - Update Stock | Sets the new stock through `Product.update_stock()` |
| 4 - Search Product | Finds by ID and prints the product details |
| 5 - Save Inventory | Writes `inventory.json` via `functions.save_inventory()` |
| 6 - Exit | Saves and exits cleanly |
| q - Quit | Exits without saving |

Quick smoke test (no interactive input):

```bash
python -c "
from product import Product
from inventory import Inventory
inv = Inventory()
inv.add_product(Product('P001', 'Laptop', 1200.00, 15))
inv.add_product(Product('P002', 'Mouse', 25.50, 40))
inv.display_all()
inv.update_stock_for_product('P001', 20)
print(inv.search_product('P099'))
import functions as fn
fn.save_inventory(inv)
"
```

---

## Submission Checklist

### Week 5 / Lab 5

- [x] `inventory_manager.py` - functional entry point
- [x] `inventory.json` - updated data file (4 products)
- [x] `log.txt` - git history (`git log > log.txt`)
- [x] `Dockerfile` - image definition
- [ ] Screenshot of `docker build` output *(student to capture)*
- [ ] Screenshot of the program running in Docker with input/output *(student to capture)*

### Week 8 / Lab 6

- [x] `product.py` - Product class with encapsulated attributes
- [x] `inventory.py` - Inventory class managing Product objects
- [x] `app.py` - refactored menu using objects
- [x] `functions.py` - file load/save
- [x] `inventory.json` - updated data file
- [x] `uml-diagrams.md` - UML for all classes
- [x] `reflection.md` - reflection question answers
- [x] `log.txt` - git history
- [ ] Screenshot of the Docker container running *(student to capture)*
- [ ] Screenshot of the program accepting input and producing output *(student to capture)*

Package the files into one folder, zip it, and upload to xSite.

---

## Git Workflow

```bash
git add .
git commit -m "Week 8: OOP refactor with Product and Inventory classes"
git push origin main
git log > log.txt
```
