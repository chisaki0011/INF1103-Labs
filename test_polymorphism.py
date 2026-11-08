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


if __name__ == "__main__":
    unittest.main(verbosity=2)
