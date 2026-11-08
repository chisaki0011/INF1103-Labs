# Inventory Management System

This is a small Python project that grew with the INF1103 labs. It started as
a menu-based inventory program and now uses classes to model products,
suppliers, inventories, and customer orders.

The project covers:

- **Lab 5:** the original functional inventory system and JSON file storage.
- **Lab 6:** `Product` and `Inventory`, with product data kept inside objects.
- **Lab 7:** physical and digital products, an abstract product base class,
  method overriding, and a shipping interface.
- **Lab 8:** supplier associations, inventory aggregation, order composition,
  type hints, and tests for substitutability and polymorphism.

## Run it

The current Docker image uses Python 3.14. Python 3.10 or later is needed to
run the code directly because it uses modern type-hint syntax.

```powershell
python app.py
```

The menu lets you display, add, search, and update products, or save the
inventory. When you add a product, enter its supplier details and then choose
whether it is physical or digital. The app saves the supplier information with
the product, so it is still available after the next load.

Older inventory records do not have supplier information. They still load;
the program displays **Unknown Supplier** for those records. You can replace
that placeholder in `inventory.json` if you know the original supplier.

## Run the tests

```powershell
python -m unittest discover -v
```

The tests cover the original product and inventory behavior as well as the new
Lab 8 relationships:

- A product keeps its supplier reference, and its displayed and saved details
  include that supplier.
- An inventory can remove a product without destroying it; the same object
  can then be added to another inventory.
- An order creates its own order lines. Two orders can refer to the same
  product while keeping separate lines and totals.
- Both physical and digital products work through the shared `Product`
  interface.

Before testing, I expected that deleting a local supplier variable would not
break a product that still refers to that supplier, that removing a product
from an inventory would leave the product usable, and that two orders for the
same product would create two separate order lines. The tests confirm those
expectations. I also expected one loop over the inventory to show the
physical product's shipping message and the digital product's download
message without checking their concrete types; that worked as expected.

## How the classes fit together

- `Product` contains the data shared by every product. `PhysicalProduct` and
  `DigitalProduct` extend it.
- A `Product` refers to a `Supplier`. The supplier is a separate object, not a
  part owned by the product.
- An `Inventory` groups product objects. Removing one only removes the
  inventory's reference; it does not change the product.
- An `Order` creates and manages its `OrderLine` objects. Each line refers to
  a product, but does not own it.

### Why the product subclasses are substitutable

Code that expects a `Product` can use either concrete product without knowing
which one it received. Both keep the same meaning for `update_stock()`, expose
the shared product details, and provide fulfilment information. The physical
product adds weight and shipping; the digital product adds its download size.
Neither subclass removes or weakens the behavior promised by `Product`.

The inventory can therefore display a mixed list with one loop. Each object
responds with its own weight or download size and its own fulfilment message.
That is polymorphism; the shared `Product` behavior is what lets the subclasses
stand in for the base type without surprising the caller.

The [UML diagrams](uml-diagrams.md) show these relationships and the types
used by the main classes. The [Lab 7 reflection](reflection.md) has the
earlier inheritance and abstraction discussion.

## Project files

| File | What it is for |
|---|---|
| `app.py` | Menu and command-line interaction |
| `product.py` | Abstract base class shared by all products |
| `physical_product.py` | Physical products, weight, and shipping |
| `digital_product.py` | Digital products and download size |
| `supplier.py` | Supplier details and display |
| `inventory.py` | Adding, finding, removing, and displaying products |
| `order.py` | Orders and the order lines they own |
| `product_factory.py` | Rebuilding the right product from saved data |
| `functions.py` | Inventory JSON loading, saving, and input helpers |
| `inventory.json` | Saved product data |
| `test_products.py` | Lab 7 product and persistence tests |
| `test_lab8.py` | Lab 8 relationship and substitutability tests |
| `uml-diagrams.md` | Class diagrams and relationship notes |

Earlier files from the functional labs are kept in the repository for
reference.

## Docker

Build the image from the project folder:

```powershell
docker build -t inf1103-labs .
```

Run the app with the project folder mounted so changes to `inventory.json`
persist on your computer:

```powershell
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-labs
```

Run the tests in the same image:

```powershell
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-labs python -m unittest discover -v
```

The Dockerfile copies the Python modules and inventory file into the image.
The host-folder mount makes the inventory file writable while the container
is running.

## Lab submission reminders

The code and tests are here, but screenshots of the Git and Docker workflow
still need to be captured separately if they are required for submission.
