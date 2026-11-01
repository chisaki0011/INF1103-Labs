"""
Tests for the Lab 7 product hierarchy and inventory integration.

Run with:
    python -m unittest test_products -v
"""

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

import functions as fn
from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
from product_factory import create_product


def capture_display(product):
    """Call display_information() and return everything it printed."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        product.display_information()
    return buffer.getvalue()


class AbstractProductTests(unittest.TestCase):
    """Section 3 - Product is abstract and cannot be instantiated."""

    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("P001", "Generic", 10.0, 1)

    def test_subclasses_are_products(self):
        self.assertIsInstance(PhysicalProduct("P001", "Guitar", 899.0, 3, 4.5), Product)
        self.assertIsInstance(DigitalProduct("P002", "Editor", 49.9, 10, 1200), Product)


class PhysicalProductTests(unittest.TestCase):
    """Sections 1.2, 2.1, 3.2 and 4.2."""

    def setUp(self):
        self.guitar = PhysicalProduct("P010", "Guitar", 899.0, 3, 4.5)

    def test_weight_is_stored(self):
        self.assertEqual(self.guitar.get_weight(), 4.5)

    def test_display_shows_parent_and_child_information(self):
        output = capture_display(self.guitar)
        self.assertIn("ID: P010 | Name: Guitar | Price: $899.00 | Stock: 3", output)
        self.assertIn("Weight: 4.50 kg", output)
        self.assertIn(self.guitar.get_fulfilment_info(), output)
        self.assertIn("Shipping cost: $14.00", output)

    def test_fulfilment_info(self):
        self.assertIn("shipping", self.guitar.get_fulfilment_info().lower())

    def test_implements_can_be_shipped(self):
        self.assertIsInstance(self.guitar, CanBeShipped)

    def test_shipping_cost_uses_weight(self):
        light = PhysicalProduct("P011", "Earbuds", 29.9, 5, 0.5)
        heavy = PhysicalProduct("P012", "Monitor", 299.9, 5, 10.0)
        self.assertLess(light.calculate_shipping_cost(), heavy.calculate_shipping_cost())
        self.assertEqual(light.calculate_shipping_cost(), 6.0)
        self.assertEqual(heavy.calculate_shipping_cost(), 25.0)

    def test_negative_weight_is_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P013", "Broken", 1.0, 1, -2)

    def test_missing_weight_is_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P014", "No weight", 1.0, 1)


class DigitalProductTests(unittest.TestCase):
    """Sections 1.3, 2.1, 3.2 and 4.2."""

    def setUp(self):
        self.editor = DigitalProduct("P020", "Photo Editor", 49.9, 999, 1200)

    def test_download_size_is_stored(self):
        self.assertEqual(self.editor.get_download_size(), 1200.0)

    def test_display_shows_parent_and_child_information(self):
        output = capture_display(self.editor)
        self.assertIn("ID: P020 | Name: Photo Editor | Price: $49.90 | Stock: 999", output)
        self.assertIn("Download size: 1200.00 MB", output)
        self.assertIn(self.editor.get_fulfilment_info(), output)

    def test_fulfilment_info(self):
        self.assertIn("download", self.editor.get_fulfilment_info().lower())

    def test_does_not_implement_can_be_shipped(self):
        self.assertNotIsInstance(self.editor, CanBeShipped)

    def test_non_positive_download_size_is_rejected(self):
        with self.assertRaises(ValueError):
            DigitalProduct("P021", "Empty", 1.0, 1, 0)


class FactoryTests(unittest.TestCase):
    """Section 5 - JSON persistence preserves the product type."""

    def test_creates_physical_from_dict(self):
        product = create_product({
            "type": "physical", "id": "P030", "name": "Desk",
            "price": 199.0, "stock": 4, "weight": 12.5,
        })
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.get_weight(), 12.5)

    def test_creates_digital_from_dict(self):
        product = create_product({
            "type": "digital", "id": "P031", "name": "Suite",
            "price": 99.0, "stock": 50, "download_size": 800.0,
        })
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 800.0)

    def test_legacy_record_without_type_loads_as_physical(self):
        product = create_product({
            "id": "P032", "name": "Legacy", "price": 5.0, "stock": 1,
        })
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.get_weight(), 0.0)

    def test_unknown_type_is_rejected(self):
        with self.assertRaises(ValueError):
            create_product({
                "type": "subscription", "id": "P033", "name": "Plan",
                "price": 9.9, "stock": 1,
            })

    def test_to_dict_round_trip(self):
        original = PhysicalProduct("P034", "Guitar", 899.0, 3, 4.5)
        rebuilt = create_product(original.to_dict())
        self.assertIsInstance(rebuilt, PhysicalProduct)
        self.assertEqual(rebuilt.to_dict(), original.to_dict())


class InventoryIntegrationTests(unittest.TestCase):
    """Section 5 - Inventory keeps working with both product types."""

    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_product(PhysicalProduct("P040", "Guitar", 899.0, 3, 4.5))
        self.inventory.add_product(DigitalProduct("P041", "Editor", 49.9, 999, 1200))

    def test_mixed_types_are_stored(self):
        products = self.inventory.get_all_products()
        self.assertEqual(len(products), 2)
        self.assertIsInstance(products[0], PhysicalProduct)
        self.assertIsInstance(products[1], DigitalProduct)

    def test_search_and_update_still_work(self):
        found = self.inventory.search_product("P041")
        self.assertIsNotNone(found)
        self.assertTrue(self.inventory.update_stock_for_product("P041", 50))
        self.assertEqual(found.get_stock(), 50)

    def test_duplicate_id_is_rejected(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            added = self.inventory.add_product(
                DigitalProduct("P040", "Clone", 1.0, 1, 1)
            )
        self.assertFalse(added)

    def test_save_and_load_preserve_types(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "inventory.json")
            self.assertTrue(fn.save_inventory(self.inventory, path))

            with open(path, "r", encoding="utf-8") as file:
                saved = json.load(file)

            self.assertEqual([item["type"] for item in saved],
                             ["physical", "digital"])
            self.assertEqual(saved[0]["weight"], 4.5)
            self.assertEqual(saved[1]["download_size"], 1200.0)

            with redirect_stdout(io.StringIO()):
                loaded = fn.load_inventory(path)

            rebuilt = [create_product(item) for item in loaded]
            self.assertIsInstance(rebuilt[0], PhysicalProduct)
            self.assertIsInstance(rebuilt[1], DigitalProduct)
            self.assertEqual(rebuilt[0].to_dict(), saved[0])
            self.assertEqual(rebuilt[1].to_dict(), saved[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
