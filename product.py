"""
Product Module - Lab 7 (Inheritance, Overriding and Abstraction)
================================================================

This module defines the ABSTRACT base class for every product in the
inventory system.

A product "is-a" item that is either physical or digital, so a generic
Product on its own is not something the system should allow. Product is
therefore an abstract class (it inherits from ABC and declares the
abstract method get_fulfilment_info()), which means it can never be
instantiated directly.

Product still owns everything that is common to every product type:
- the encapsulated attributes (id, name, price, stock, supplier reference)
- update_stock(), display_information() and the getters
- to_dict() for JSON persistence

The specialised classes (PhysicalProduct / DigitalProduct) inherit from
Product and add their own attributes and behaviour. This keeps Product
closed for modification but open for extension (Open/Closed Principle).

The Supplier object is created independently and associated with a Product.
Older saved records without supplier data use the explicit unknown supplier.

Responsibilities kept OUT of this module (SRP):
- functions.py  : file I/O, prompts and display helpers
- app.py        : main menu and user interaction
- inventory.py  : the collection of products
"""

from abc import ABC, abstractmethod

from supplier import DEFAULT_SUPPLIER, Supplier


class Product(ABC):
    """
    Abstract base class for a single product in the inventory system.

    Uses encapsulation with private attributes (double underscore prefix)
    to protect the internal data. External code should only interact
    through public methods like update_stock() and display_information().

    Concrete subclasses reuse the constructor with super() and accept
    either the lab-style positional arguments::

        PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.2, supplier)

    or a dictionary loaded from inventory.json::

        PhysicalProduct({"type": "physical", "id": "P001", "name": "Laptop",
                         "price": 1200.00, "stock": 15, "weight": 2.2,
                         "supplier": supplier_data})
    """

    #: Type identifier written to inventory.json so that the correct
    #: subclass can be rebuilt when the data is loaded. Every concrete
    #: subclass must override this.
    PRODUCT_TYPE: str | None = None

    def __init__(
        self,
        product_id: str | dict[str, object],
        name: str | None = None,
        price: float | None = None,
        stock: int | None = None,
        supplier: Supplier | None = None,
    ) -> None:
        """
        Initialize the common part of a product.

        This constructor is called by the subclasses through super().

        Args:
            product_id (str | dict): The product ID, or a dictionary containing
                the keys 'id', 'name', 'price' and 'stock'.
            name (str): Product name (ignored when a dictionary is supplied).
            price (float): Product price (ignored when a dictionary is supplied).
            stock (int): Current stock quantity (ignored when a dictionary is supplied).
            supplier (Supplier | None): The independently created supplier.
                Older records without one use the unknown-supplier placeholder.

        Example:
            >>> PhysicalProduct("P001", "Laptop", 1200.0, 15, 2.2)
            >>> PhysicalProduct({"id": "P001", "name": "Laptop",
            ...                  "price": 1200.0, "stock": 15, "weight": 2.2})
        """
        # Support dictionary input so inventory.json can be loaded directly
        if isinstance(product_id, dict):
            data = product_id
            product_id = data["id"]
            name = data["name"]
            price = data["price"]
            stock = data["stock"]
            supplier_data = data.get("supplier")
            if supplier is None:
                if isinstance(supplier_data, Supplier):
                    supplier = supplier_data
                elif isinstance(supplier_data, dict):
                    supplier = Supplier.from_dict(supplier_data)

        if name is None or price is None or stock is None:
            raise ValueError(
                "Product requires an id, name, price and stock "
                "(or a single dictionary containing those keys)."
            )
        if supplier is None:
            supplier = DEFAULT_SUPPLIER
        if not isinstance(supplier, Supplier):
            raise TypeError("Product supplier must be a Supplier object.")

        # Use double underscore prefix to indicate private attributes
        # This follows the encapsulation principle from Lab 6
        self.__product_id: str = str(product_id)
        self.__name: str = str(name)
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.__supplier: Supplier = supplier

    def __str__(self) -> str:
        """
        Return a string representation of the Product for console display.

        Returns:
            str: Formatted product information.

        Example:
            >>> product = PhysicalProduct("P001", "Laptop", 999.0, 5, 2.2)
            >>> print(product)
            PhysicalProduct(id=P001, name=Laptop, price=999.0, stock=5)
        """
        return (
            f"{type(self).__name__}(id={self.__product_id}, name={self.__name}, "
            f"price={self.__price}, stock={self.__stock})"
        )

    def update_stock(self, quantity: int) -> None:
        """
        Set the product's stock to a new quantity.

        This method encapsulates the business logic for updating stock.
        External code calls this instead of directly changing __stock.

        Args:
            quantity (int): The new stock quantity (must be >= 0).

        Raises:
            ValueError: If quantity is negative.

        Example:
            >>> product = PhysicalProduct("P001", "Laptop", 999.0, 10, 2.2)
            >>> product.update_stock(50)
            >>> product.get_stock()
            50
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self.__stock = quantity

    def display_information(self) -> str:
        """
        Display the product's common information in a formatted line.

        Subclasses override this method, call super().display_information()
        to reuse the common part, and then print their own extra details.

        Returns:
            str: The formatted product details (also printed to the console).

        Example:
            >>> product = PhysicalProduct("P001", "Laptop", 999.0, 15, 2.2)
            >>> product.display_information()
            ID: P001 | Name: Laptop | Price: $999.00 | Stock: 15
        """
        information = (
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )
        print(information)
        supplier_information = self.__supplier.display_information()
        return f"{information}\n{supplier_information}"

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """
        Describe how this product type is delivered to the customer.

        Every concrete product type must implement this method, because the
        system has decided that every product is either physical or digital
        and each of them is fulfilled in a different way.

        Returns:
            str: A human-readable description of the fulfilment method.
        """
        raise NotImplementedError

    def get_product_type(self) -> str:
        """
        Get the type identifier used for JSON persistence.

        Returns:
            str: 'physical', 'digital', or whatever a new subclass declares.

        Raises:
            NotImplementedError: If a subclass forgot to set PRODUCT_TYPE.
        """
        if self.PRODUCT_TYPE is None:
            raise NotImplementedError(
                f"{type(self).__name__} must define a PRODUCT_TYPE identifier."
            )
        return self.PRODUCT_TYPE

    def get_product_id(self) -> str:
        """
        Get the product ID (getter method for encapsulated attribute).

        Returns:
            str: The product's ID.
        """
        return self.__product_id

    def get_name(self) -> str:
        """
        Get the product name (getter method for encapsulated attribute).

        Returns:
            str: The product's name.
        """
        return self.__name

    def get_price(self) -> float:
        """
        Get the product price (getter method for encapsulated attribute).

        Returns:
            float: The product's price.
        """
        return self.__price

    def get_stock(self) -> int:
        """
        Get the current stock quantity (getter method for encapsulated attribute).

        Returns:
            int: The product's current stock level.
        """
        return self.__stock

    def get_supplier(self) -> Supplier:
        """Return the Supplier associated with this product."""
        return self.__supplier

    def to_dict(self) -> dict[str, object]:
        """
        Convert the common product data into a JSON-serialisable dictionary.

        Subclasses override this method, call super().to_dict() to reuse the
        common fields, and then add their own extra attributes.

        Returns:
            dict: Dictionary with product details, its supplier, and the
            product type's extra attributes.
        """
        return {
            "type": self.get_product_type(),
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }
