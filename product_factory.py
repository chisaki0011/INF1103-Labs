"""
Product Factory Module - Lab 7 (Section 5, JSON persistence)
============================================================

Rebuilds the correct Product subclass from data loaded out of
inventory.json. The 'type' identifier saved by each product decides which
class is created.

Keeping this mapping in one place means the rest of the system never needs
to know the concrete class names. Adding a new product type is a one-line
change to PRODUCT_CLASSES plus the new class itself, which is the
Open/Closed Principle in practice.
"""

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product


#: Maps the "type" value stored in inventory.json to its class.
PRODUCT_CLASSES: dict[str, type[Product]] = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}

#: Older Lab 6 records have no "type" field. Treat them as physical products
#: (the original Product was a generic stocked item) so old data still loads.
DEFAULT_PRODUCT_TYPE: str = "physical"


def create_product(data: Product | dict[str, object]) -> Product:
    """
    Create the appropriate Product subclass from a dictionary.

    Args:
        data (Product | dict): A product object (returned unchanged) or a
            dictionary with at least 'id', 'name', 'price' and 'stock', plus
            'type' and the type-specific fields ('weight' or 'download_size').
            New records may also contain a nested 'supplier' dictionary.

    Returns:
        Product: An instance of PhysicalProduct or DigitalProduct.

    Raises:
        TypeError: If data is neither a Product nor a dictionary.
        ValueError: If the type identifier is unknown or the record is
            missing required fields.

    Example:
        >>> create_product({"type": "digital", "id": "P011", "name": "Editor",
        ...                 "price": 49.9, "stock": 10, "download_size": 1200})
        DigitalProduct(id=P011, name=Editor, price=49.9, stock=10)
    """
    if isinstance(data, Product):
        return data

    if not isinstance(data, dict):
        raise TypeError(
            "create_product() expects a Product object or a dictionary."
        )

    type_id = str(data.get("type", DEFAULT_PRODUCT_TYPE)).strip().lower()
    product_class = PRODUCT_CLASSES.get(type_id)

    if product_class is None:
        known_types = ", ".join(sorted(PRODUCT_CLASSES))
        raise ValueError(
            f"Unknown product type '{type_id}'. Expected one of: {known_types}."
        )

    # Legacy Lab 6 records have no weight; keep them loadable.
    if type_id == "physical" and data.get("weight") is None:
        data = dict(data)
        data["weight"] = 0.0

    return product_class(data)
