"""Tests for Lab 8 substitutability and polymorphic product behavior."""

import io
import unittest
from contextlib import redirect_stdout

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> str:
    product.display_information()
    return product.get_fulfilment_info()


class SubstitutabilityTests(unittest.TestCase):
    def test_product_types_work_through_the_product_abstraction(self) -> None:
        products: list[Product] = [
            PhysicalProduct(
                "P401", "Book", 10.0, 2, 0.5,
                supplier=Supplier("SUP-1", "Books Ltd", "books@example.test"),
            ),
            DigitalProduct(
                "P402", "E-book", 7.0, 5, 15.0,
                supplier=Supplier("SUP-2", "Media Ltd", "media@example.test"),
            ),
        ]
        inventory = Inventory()
        for product in products:
            inventory.add_product(product)

        with redirect_stdout(io.StringIO()):
            fulfilment = [
                show_product_details(product)
                for product in inventory.products
            ]
            for product in inventory.products:
                product.update_stock(product.get_stock() + 1)

        self.assertIn("shipping", fulfilment[0].lower())
        self.assertIn("download", fulfilment[1].lower())
        self.assertEqual(
            [product.get_stock() for product in inventory.products], [3, 6]
        )

    def test_inventory_displays_each_subclass_without_type_checks(self) -> None:
        inventory = Inventory()
        inventory.add_product(
            PhysicalProduct(
                "P403", "Mug", 8.0, 3, 0.4,
                supplier=Supplier("SUP-3", "Kitchen Ltd", "k@example.test"),
            )
        )
        inventory.add_product(
            DigitalProduct(
                "P404", "Recipe book", 5.0, 8, 2.0,
                supplier=Supplier("SUP-4", "Food Ltd", "f@example.test"),
            )
        )

        with redirect_stdout(io.StringIO()) as output:
            inventory.display_all()

        self.assertIn("Weight: 0.40 kg", output.getvalue())
        self.assertIn("Download size: 2.00 MB", output.getvalue())
        self.assertIn("Requires physical shipping", output.getvalue())
        self.assertIn("Delivered digitally", output.getvalue())

    def test_one_product_loop_invokes_each_fulfilment_implementation(self) -> None:
        inventory = Inventory()
        inventory.add_product(
            PhysicalProduct(
                "P405", "Parcel", 14.0, 2, 1.0,
                supplier=Supplier("SUP-5", "Parcel Ltd", "p@example.test"),
            )
        )
        inventory.add_product(
            DigitalProduct(
                "P406", "Manual", 3.0, 7, 1.0,
                supplier=Supplier("SUP-6", "Docs Ltd", "d@example.test"),
            )
        )

        with redirect_stdout(io.StringIO()):
            fulfilment = [
                product.get_fulfilment_info()
                for product in inventory.products
            ]

        self.assertIn("physical shipping", fulfilment[0])
        self.assertIn("digitally", fulfilment[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
