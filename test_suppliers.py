"""Tests for Lab 8 supplier-product association."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import functions as fn
from app import option_2_add_product
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product_factory import create_product
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("SUP-001", "Acme Supplies", "contact@acme.example")


class SupplierAssociationTests(unittest.TestCase):
    def test_products_retain_and_display_their_supplier(self) -> None:
        supplier = make_supplier()
        products = [
            PhysicalProduct("P101", "Desk", 120.0, 3, 10.0, supplier=supplier),
            DigitalProduct("P102", "Editor", 25.0, 20, 500.0, supplier=supplier),
        ]
        self.assertIs(products[0].get_supplier(), supplier)
        self.assertIs(products[1].get_supplier(), supplier)

        del supplier
        with redirect_stdout(io.StringIO()) as output:
            for product in products:
                product.display_information()
        self.assertEqual(output.getvalue().count("Acme Supplies"), 2)
        self.assertEqual(output.getvalue().count("contact@acme.example"), 2)

    def test_supplier_remains_usable_without_a_product(self) -> None:
        supplier = make_supplier()
        product = PhysicalProduct(
            "P105", "Crate", 12.0, 1, 2.0, supplier=supplier
        )
        del product

        with redirect_stdout(io.StringIO()) as output:
            supplier.display_information()
        self.assertIn("Acme Supplies", output.getvalue())

    def test_supplier_is_preserved_in_product_and_inventory_json(self) -> None:
        inventory = Inventory()
        inventory.add_product(
            DigitalProduct(
                "P107", "Photo editor", 30.0, 5, 600.0,
                supplier=make_supplier(),
            )
        )

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "inventory.json")
            self.assertTrue(fn.save_inventory(inventory, path))
            with redirect_stdout(io.StringIO()):
                loaded = fn.load_inventory(path)
            restored = create_product(loaded[0])

        original = inventory.find_product("P107")
        self.assertIsNotNone(original)
        assert original is not None
        self.assertEqual(
            restored.get_supplier().to_dict(),
            original.get_supplier().to_dict(),
        )

    def test_add_product_flow_collects_supplier_details(self) -> None:
        inventory = Inventory()
        answers = [
            "P106", "Desk lamp", "SUP-106", "Bright Supply",
            "sales@bright.example", "1", "",
        ]
        with (
            patch("builtins.input", side_effect=answers),
            patch("functions.get_valid_price", return_value=25.0),
            patch("functions.get_valid_stock", return_value=4),
            patch("functions.get_valid_weight", return_value=1.5),
            redirect_stdout(io.StringIO()),
        ):
            option_2_add_product(inventory)

        product = inventory.find_product("P106")
        self.assertIsInstance(product, PhysicalProduct)
        assert product is not None
        self.assertEqual(product.get_supplier().name, "Bright Supply")

    def test_legacy_record_uses_unknown_supplier(self) -> None:
        product = create_product({
            "type": "digital",
            "id": "P104",
            "name": "Legacy download",
            "price": 5.0,
            "stock": 1,
            "download_size": 10.0,
        })
        self.assertEqual(product.get_supplier().supplier_id, "SUP-UNKNOWN")


if __name__ == "__main__":
    unittest.main(verbosity=2)
