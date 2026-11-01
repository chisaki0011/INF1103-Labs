# INF1103 Inventory Management System

This repository contains the Week 5 (functional) inventory system, its Week 8
(object-oriented) refactor, and the Lab 7 extension with inheritance,
method overriding and abstraction.

- **Week 5 / Lab 5** - dictionaries, functions and JSON persistence.
- **Week 8 / Lab 6** - the same system refactored into `Product` and
  `Inventory` classes using encapsulation and the Single Responsibility
  Principle.
- **Lab 7** - `Product` becomes an abstract class with the subclasses
  `PhysicalProduct` and `DigitalProduct`, a `CanBeShipped` interface, and
  type-aware JSON persistence.

---

## Project Structure

```
INF1103-Labs/
├── app.py                 # Entry point - menu and user flow
├── product.py             # Product - abstract base class (common data/state)
├── physical_product.py    # PhysicalProduct - weight + shipping
├── digital_product.py     # DigitalProduct - download size
├── can_be_shipped.py      # CanBeShipped - interface-style ABC
├── product_factory.py     # Rebuilds the right subclass when loading JSON
├── inventory.py           # Inventory class - collection of Product objects
├── functions.py           # File I/O (load/save) and input/display helpers
├── inventory.json         # Persistent inventory data (7 products)
├── test_products.py       # unittest suite for the Lab 7 behaviour
├── inventory_manager.py   # Week 5 functional entry point (legacy)
├── persistent_auditor.py  # Week 5 functions (load/save/CRUD) (legacy)
├── Dockerfile             # Container image definition
├── uml-diagrams.md        # UML class diagrams for every class
├── reflection.md          # Lab 6 and Lab 7 reflection answers
├── log.txt                # Git history for submission
└── README.md              # This file
```

> `auditor.py`, `modular_auditor.py`, `old_persistent_auditor.py` and
> `hello.py` are earlier-week files kept for history but ignored by git
> (see `.gitignore`).

---

## Running the System

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

### Adding a product

Option **2** now asks for the product type first:

```
Product type:
  1. Physical product (has a weight and can be shipped)
  2. Digital product (has a download size)
Choose type (1 or 2):
```

- **1** also asks for the weight in kilograms.
- **2** also asks for the download size in megabytes.

### Example session

```
inventory.json found.
Inventory loaded successfully.
Product 'Laptop' added successfully!
...
Welcome to the Inventory Management System!
...
Enter your choice (1-6 or 'q' to quit): 1

Current Inventory
------------------------------------------------------------
ID: P001 | Name: Laptop | Price: $1200.00 | Stock: 15
  Type: Physical | Weight: 2.20 kg
  Fulfilment: Requires physical shipping and handling.
  Shipping cost: $9.40
ID: P006 | Name: Antivirus 2026 | Price: $49.90 | Stock: 999
  Type: Digital | Download size: 350.00 MB
  Fulfilment: Delivered digitally via download link.
------------------------------------------------------------
```

---

## Running the Tests

```bash
python -m unittest test_products -v
```

The 23 tests cover:

- `Product` cannot be instantiated (abstract class);
- physical products store/display weight and calculate shipping;
- digital products store/display download size and do **not** implement
  `CanBeShipped`;
- both subclasses implement `get_fulfilment_info()`;
- the factory rebuilds the correct subclass from JSON;
- inventory operations and save/load round-trips preserve types.

---

## Running the Week 5 Functional System (Legacy)

```bash
python inventory_manager.py
```

This uses `persistent_auditor.py` and the Week 5 dictionary/list design.

---

## Class Design

### `Product` (`product.py`) - abstract

Responsible for the data and behaviour shared by **every** product.

```python
class Product(ABC):
    PRODUCT_TYPE = None

    def __init__(self, product_id, name=None, price=None, stock=None):
        # Accepts Product("P001", "Laptop", 1200.0, 15)
        # or a dictionary loaded from JSON (used by the subclasses)
        ...

    def update_stock(self, quantity): ...
    def display_information(self): ...
    @abstractmethod
    def get_fulfilment_info(self): ...
    def get_product_type(self): ...
    def get_product_id(self): ...
    def get_name(self): ...
    def get_price(self): ...
    def get_stock(self): ...
    def to_dict(self): ...
```

Private attributes (`__product_id`, `__name`, `__price`, `__stock`) are only
changed through `update_stock()`. The class contains **no** file I/O, menu or
`input()` code. Because `get_fulfilment_info()` is abstract, `Product` itself
cannot be instantiated.

### `PhysicalProduct` (`physical_product.py`)

```python
class PhysicalProduct(Product, CanBeShipped):
    PRODUCT_TYPE = "physical"

    def __init__(self, product_id, name=None, price=None, stock=None, weight=None):
        super().__init__(product_id, name, price, stock)
        ...

    def display_information(self):   # super() first, then weight/fulfilment/shipping
    def get_fulfilment_info(self):   # "Requires physical shipping and handling."
    def get_weight(self): ...
    def calculate_shipping_cost(self):  # 5.00 + 2.00 * weight
    def to_dict(self):               # super() + weight
```

### `DigitalProduct` (`digital_product.py`)

```python
class DigitalProduct(Product):
    PRODUCT_TYPE = "digital"

    def __init__(self, product_id, name=None, price=None, stock=None,
                 download_size=None):
        super().__init__(product_id, name, price, stock)
        ...

    def display_information(self):   # super() first, then download size/fulfilment
    def get_fulfilment_info(self):   # "Delivered digitally via download link."
    def get_download_size(self): ...
    def to_dict(self):               # super() + download_size
```

`DigitalProduct` deliberately does **not** implement `CanBeShipped`.

### `CanBeShipped` (`can_be_shipped.py`)

An interface-style abstract base class with a single abstract method,
`calculate_shipping_cost()`. It holds no attributes and no implementation.
Only `PhysicalProduct` signs the contract.

### `Inventory` (`inventory.py`)

Responsible for a **collection** of `Product` objects. It works with the
abstract `Product` type, so it never checks whether a product is physical or
digital.

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

### `product_factory.py`

```python
PRODUCT_CLASSES = {"physical": PhysicalProduct, "digital": DigitalProduct}

def create_product(data): ...
```

Reads the `type` field saved in `inventory.json` and returns the matching
subclass. A missing `type` (older Lab 6 data) is treated as `physical` with a
weight of `0.0` so old files still load. Adding a new product type means one
new entry in `PRODUCT_CLASSES`.

### `functions.py`

Handles persistence and input helpers:

| Function | Purpose |
|----------|---------|
| `load_inventory(filename)` | Load JSON and return a list of dictionaries |
| `save_inventory(inventory, filename)` | Save an `Inventory` object or list of products |
| `display_all(inventory)` | Display products (objects or dictionaries) |
| `get_valid_price()` / `get_valid_stock()` | Validated prompts |
| `get_valid_weight()` / `get_valid_download_size()` | Validated prompts for the extra attributes |

### `app.py`

Displays the menu, reads user input, creates the chosen subclass and calls
`Inventory` methods. It never touches a product's private attributes.

See `uml-diagrams.md` for the full UML diagrams.

---

## Data Format

`inventory.json` is a list of product dictionaries. Every record carries a
`type` identifier plus the attributes for that type:

```json
[
  { "type": "physical", "id": "P001", "name": "Laptop",
    "price": 1200.0, "stock": 15, "weight": 2.2 },

  { "type": "digital", "id": "P006", "name": "Antivirus 2026",
    "price": 49.9, "stock": 999, "download_size": 350.0 }
]
```

The file currently holds five physical and two digital products. If the file is
missing or invalid, the program starts with an empty inventory.

---

## Docker

Build the image (only needed when the `Dockerfile` or dependencies change):

```bash
docker build -t inf1103-labs-smart-auditor .
```

Run the system with a volume mount so `inventory.json` persists on the host:

```bash
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-labs-smart-auditor
```

Run the test suite in the container:

```bash
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-labs-smart-auditor python -m unittest test_products -v
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
| 1 - Display All Products | Shows common data, plus weight/shipping or download size |
| 2 - Add Product | Lets the user choose physical or digital, validates the extra field, rejects duplicate IDs |
| 3 - Update Stock | Sets the new stock through `Product.update_stock()` |
| 4 - Search Product | Finds by ID and prints the type-specific details |
| 5 - Save Inventory | Writes `inventory.json` including `type` and the extra attribute |
| 6 - Exit | Saves and exits cleanly |
| q - Quit | Exits without saving |

Lab 7 behaviour verified by `test_products.py`:

| Requirement | Verified |
|-------------|----------|
| `Product` cannot be instantiated | yes |
| Physical products store and display weight | yes |
| Digital products store and display download size | yes |
| Both subclasses implement `get_fulfilment_info()` | yes |
| Physical products can calculate shipping costs | yes |
| Digital products are not required to implement shipping | yes |
| Inventory operations continue to work | yes |
| JSON save/load preserve the correct product types | yes |

---

## Submission Checklist

### Week 5 / Lab 5

- [x] `inventory_manager.py` - functional entry point
- [x] `inventory.json` - updated data file
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

### Lab 7

- [x] `product.py` - abstract `Product` with `get_fulfilment_info()`
- [x] `physical_product.py` - weight, overridden display, shipping cost
- [x] `digital_product.py` - download size, overridden display
- [x] `can_be_shipped.py` - interface-style ABC
- [x] `product_factory.py` - type-aware loading
- [x] `app.py` - type selection when adding a product
- [x] `inventory.json` - records include `type` and the extra attribute
- [x] `test_products.py` - 23 passing tests
- [x] `uml-diagrams.md` - updated UML (inheritance, realisation, abstract)
- [x] `reflection.md` - Lab 7 reflection (including the optional task)
- [x] `.gitignore` - cache, virtualenv, `.env` and IDE exclusions
- [ ] Screenshot of `git status` / `git log` and the Docker workflow *(student to capture)*

Package the files into one folder, zip it, and upload to xSite.

---

## Git Workflow

```bash
git status
git add .
git commit -m "Lab 7: inheritance, overriding, abstraction and shipping interface"
git push origin main
git log > log.txt
```
