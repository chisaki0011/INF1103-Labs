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

---

# Lab 7 Reflection

Answers refer to `product.py`, `physical_product.py`, `digital_product.py`,
`can_be_shipped.py`, `product_factory.py` and `inventory.py`.

### 1. Why do `PhysicalProduct` and `DigitalProduct` inherit from `Product`?

The "is-a" test works in both directions:

- "A guitar **is-a** physical product" and "a physical product **is-a**
  product".
- "An operating system **is-a** digital product" and "a digital product
  **is-a** product".

Everything that is true of any product (ID, name, price, stock, updating
stock, displaying the common fields, JSON serialisation) is therefore written
once in `Product`. The subclasses only add what makes them different: a
weight and shipping for physical products, a download size for digital ones.

If the subclasses did not inherit, the common fields, the validation and the
display formatting would be copy-pasted into each class, and a bug fix in one
copy would have to be repeated everywhere.

### 2. What is method overriding and where does `super()` help?

Overriding means a subclass supplies its own version of a method that it
inherited. `PhysicalProduct.display_information()` and
`DigitalProduct.display_information()` both replace
`Product.display_information()`, so the child version is the one that runs.

Rather than re-printing the common fields, each override calls
`super().display_information()` first and then prints only its own extra
lines. The parent keeps ownership of the common format, the child adds its
own detail, and there is no duplicated formatting code.

The same pattern is used for `to_dict()`: the child calls
`super().to_dict()` to get the common fields (including `type`) and then adds
`weight` or `download_size`. That is how the JSON keeps the type information
without every class rebuilding the whole dictionary.

### 3. Why make `Product` abstract, and what happens if you instantiate it?

The system has decided that every product is either physical or digital, so a
"generic product" is not a valid thing to create. Making `Product` inherit
from `ABC` and marking `get_fulfilment_info()` with `@abstractmethod` turns
that design rule into something Python enforces:

```
>>> Product("P001", "Generic", 10.0, 1)
TypeError: Can't instantiate abstract class Product without an implementation
for abstract method 'get_fulfilment_info'
```

It also forces every future product type to answer the important question
"how is this delivered?". A subclass that forgets the method cannot be
instantiated either, so the mistake is caught immediately instead of
producing a product whose fulfilment behaviour is silently missing.

The abstract class still contains concrete methods (`update_stock()`,
`display_information()`, the getters), so it is not "empty" - it defines both
the shared implementation and the contract.

### 4. Why is `CanBeShipped` an interface rather than a superclass?

`CanBeShipped` describes a capability ("must be able to be shipped"), not a
kind of thing. "A guitar is-a shipped" is false, so putting shipping in the
product inheritance tree would be wrong. The capability is also not tied to
products: in principle a crate or a document could implement it too.

In Python there is no `interface` keyword, so `CanBeShipped` is an abstract
base class containing only the `calculate_shipping_cost()` contract - no
attributes and no implementation. `PhysicalProduct` signs that contract by
inheriting it and providing the method; `DigitalProduct` does not, because a
download is not shipped.

This keeps `PhysicalProduct` at **single class inheritance** (`Product`) plus
one interface. The inheritance tree stays a clean "is-a" hierarchy while
capabilities are mixed in separately.

### 5. How does this design follow the Open/Closed Principle?

`Product`, `Inventory`, `functions.py` and `app.py` are closed for
modification: they work with the abstract `Product` type and only call methods
that every product provides. New product types are added by extension - a new
subclass plus one entry in `PRODUCT_CLASSES` in `product_factory.py` - and the
collection code does not change at all.

`Inventory.display_all()` is the clearest example: it simply calls
`product.display_information()` on each object. It does not check the type and
does not know about weights or download sizes, yet it correctly prints both
kinds of product (polymorphism).

### 6. Optional task - adding `SubscriptionProduct`

**How well does the current design support it?** Mostly well. A
`SubscriptionProduct(Product)` class needs a `billing_period` (for example
"monthly") and a `get_fulfilment_info()` implementation; `to_dict()` extends
the parent dictionary with `billing_period`. That part is pure extension.

**What still has to change?** Three things outside the new class:

1. `PRODUCT_CLASSES` in `product_factory.py` needs a `"subscription"` entry,
   otherwise the loader cannot rebuild the type from JSON.
2. `app.py` needs a third menu choice and a prompt for `billing_period`,
   because the user interface has to collect the new attribute.
3. `inventory.json` data gains the new field (handled automatically on save).

`Product`, `Inventory`, `functions.py`, `PhysicalProduct`, `DigitalProduct`
and `CanBeShipped` do not need to change. That is a good result for a
single new type.

**How could the changes be reduced or removed?** The two remaining changes are
both about *data entry*, not about the model:

- Replace the `if/elif` type prompt in `app.py` with a small per-type
  descriptor (name, extra-field label, field name, validation) held in a
  registry. The menu would then be generated from the registry, so a new type
  only adds one registry entry.
- Go further and use composition instead of inheritance: give a product a
  `FulfilmentStrategy` object (`PhysicalFulfilment`, `DigitalFulfilment`,
  `SubscriptionFulfilment`) and inject it. Adding a delivery method then means
  adding one strategy class and one registry entry, with no new subclass and
  no new prompt logic.

That is why the hint says the next improvement is not an inheritance solution:
inheritance makes the *model* easy to extend, but the user interface and the
persistence mapping still need one small, predictable change per type. A
registry (and, eventually, composition/strategy) is what removes that last
coupling.

