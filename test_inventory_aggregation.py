"""Tests for Lab 8 Inventory aggregation."""

import unittest

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("SUP-001", "Acme Supplies", "contact@acme.example")


class InventoryAggregationTests(unittest.TestCase):
    def test_product_can_move_between_inventories(self) -> None:
        product = PhysicalProduct(
            "P201", "Shelf", 40.0, 2, 4.0, supplier=make_supplier()
        )
        first = Inventory()
        second = Inventory()

        self.assertTrue(first.add_product(product))
        self.assertIs(first.find_product("P201"), product)
        self.assertTrue(first.remove_product("P201"))
        self.assertIsNone(first.find_product("P201"))
        self.assertEqual(product.get_name(), "Shelf")
        self.assertTrue(second.add_product(product))
        self.assertIs(second.find_product("P201"), product)

    def test_products_property_does_not_expose_inventory_collection(self) -> None:
        product = DigitalProduct(
            "P202", "Font", 12.0, 5, 50.0, supplier=make_supplier()
        )
        inventory = Inventory()
        inventory.add_product(product)

        exposed_copy = inventory.products
        exposed_copy.clear()

        self.assertIs(inventory.find_product("P202"), product)

    def test_remove_returns_false_when_product_is_absent(self) -> None:
        self.assertFalse(Inventory().remove_product("missing"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
