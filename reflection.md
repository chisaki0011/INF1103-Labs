# Lab 6 Reflection Questions

Answers refer to the implementation in `product.py`, `inventory.py` and `app.py`.

### 1. What is the difference between a class and an object?

A **class** is the blueprint or template that defines what data and behaviour a
thing has. An **object** is a concrete instance created from that blueprint.
`Product` is the class; `Product("P001", "Laptop", 1200.00, 15)` is an object
(one specific product).

### 2. Why is `Product` a suitable class for this system?

A product is a clear noun in the system description. Each product carries the
same set of attributes (ID, name, price, stock) and the same behaviour
(update its stock, display itself). Grouping that data and behaviour into one
class keeps each product self-contained and avoids passing loose dictionaries
around.

### 3. What data belongs inside a `Product` object?

- `__product_id` - unique identifier
- `__name` - product name
- `__price` - price
- `__stock` - current stock quantity

These are the four pieces of information that describe a single product and
nothing else.

### 4. Why should the `Product` class manage its own stock rather than the main program directly changing it?

If any part of the program could write `product.__stock = 50`, the class would
have no control over invalid values. By providing `update_stock(quantity)`, the
class can validate the value (reject negatives) and keep the rule in one place.
Every caller automatically follows the same rule, and the internal storage can
change later without breaking callers.

### 5. What does encapsulation mean in your program?

Encapsulation means bundling data with the methods that operate on it, and
hiding the internal data behind a public interface. In `Product`, the
attributes use the `__` prefix (name mangling), so external code cannot safely
read or write them directly. Access happens through `get_product_id()`,
`get_name()`, `get_price()`, `get_stock()` and changes happen through
`update_stock()`.

### 6. What is the responsibility of the `Product` class?

To represent and manage **one** product: store its attributes, update its own
stock, expose read-only getters, and display its own information. It does not
load/save files, show menus, ask for input, or manage the inventory collection.

### 7. What is the responsibility of the `Inventory` class?

To manage a **collection** of `Product` objects: add products (with duplicate
checking), search for a product by ID, display all products, and update the
stock of a specific product by delegating to that product's `update_stock()`.

### 8. How does separating these responsibilities demonstrate the Single Responsibility Principle?

Each class has exactly one reason to change:

- `Product` changes only if how a single product is represented changes.
- `Inventory` changes only if how the collection is managed changes.
- `functions.py` changes only if persistence or input handling changes.
- `app.py` changes only if the menu or user flow changes.

Because responsibilities are separated, a change in file storage does not
affect the `Product` class, and a change to the menu does not affect
`Inventory`.

### 9. What information does the main program need to know about a `Product`?

Only its public interface: construct it with ID, name, price and stock; ask for
its ID when searching; call `display_information()`; and call
`update_stock()` when the stock changes. It also uses `to_dict()` indirectly
through the save function when persisting.

### 10. What information about the internal implementation of `Product` does the main program not need to know?

The main program does not need to know:

- that the attributes are stored as `__product_id`, `__name`, `__price`,
  `__stock`;
- that Python performs name mangling (`_Product__stock`);
- how validation is implemented inside `update_stock()`;
- how the display line is formatted internally.

It only relies on the public methods, so the internals can be refactored
without changing `app.py`.
