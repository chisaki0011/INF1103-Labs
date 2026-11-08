"""Tests for Lab 8 order-line composition."""

import io
import unittest
from contextlib import redirect_stdout

from digital_product import DigitalProduct
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("SUP-001", "Acme Supplies", "contact@acme.example")


class OrderCompositionTests(unittest.TestCase):
    def test_orders_create_separate_lines_for_a_shared_product(self) -> None:
        product = DigitalProduct(
            "P301", "Design app", 19.95, 10, 800.0, supplier=make_supplier()
        )
        first = Order("O-001")
        second = Order("O-002")

        first.add_order_line(product, 2)
        first.add_order_line(product, 1)
        second.add_order_line(product, 3)

        first_lines = first.order_lines
        second_lines = second.order_lines
        self.assertEqual(len(first_lines), 2)
        self.assertEqual(len(second_lines), 1)
        self.assertIsNot(first_lines[0], second_lines[0])
        self.assertIs(first_lines[0].product, product)
        self.assertIs(second_lines[0].product, product)
        self.assertAlmostEqual(first_lines[0].calculate_subtotal(), 39.9)
        self.assertAlmostEqual(first.calculate_total(), 59.85)
        self.assertAlmostEqual(second.calculate_total(), 59.85)

    def test_order_displays_lines_and_total(self) -> None:
        product = PhysicalProduct(
            "P302", "Lamp", 15.0, 4, 1.0, supplier=make_supplier()
        )
        order = Order("O-003")
        order.add_order_line(product, 2)

        with redirect_stdout(io.StringIO()) as output:
            information = order.display_information()

        self.assertIn("Lamp x 2", information)
        self.assertIn("Total: $30.00", output.getvalue())

    def test_order_removes_lines_through_its_own_api(self) -> None:
        product = DigitalProduct(
            "P303", "Icon pack", 8.0, 3, 20.0, supplier=make_supplier()
        )
        order = Order("O-004")
        order.add_order_line(product, 1)
        order.add_order_line(product, 2)

        order.remove_order_line(0)

        self.assertEqual(len(order.order_lines), 1)
        self.assertEqual(order.calculate_total(), 16.0)
        with self.assertRaises(IndexError):
            order.remove_order_line(1)

    def test_order_line_rejects_invalid_quantity(self) -> None:
        product = DigitalProduct(
            "P304", "Template", 2.0, 2, 10.0, supplier=make_supplier()
        )

        with self.assertRaises(ValueError):
            OrderLine(product, 0)
        with self.assertRaises(TypeError):
            OrderLine(product, 1.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
