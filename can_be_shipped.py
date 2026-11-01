"""
CanBeShipped Module - Lab 7 (Interfaces using abstract base classes)
====================================================================

This module defines an INTERFACE, not a parent class.

A guitar is not "a shipped", so CanBeShipped is not part of the product
inheritance tree. It describes a capability: a "must-be-able-to" contract.
Python has no interface keyword, so an abstract base class is used to
declare the methods that any class signing this contract must provide.

Only the contract lives here - no product attributes and no shipping
implementation details. PhysicalProduct signs the contract and provides
the implementation.
"""

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """
    Interface-style abstract base class for anything that can be shipped.

    Any class that implements this interface must provide
    calculate_shipping_cost(). Digital products do not implement it,
    because they are not physically shipped.
    """

    @abstractmethod
    def calculate_shipping_cost(self):
        """
        Calculate the cost of shipping this object.

        Returns:
            float: The shipping cost in dollars.
        """
        raise NotImplementedError
