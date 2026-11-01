"""
DigitalProduct Module - Lab 7 (Inheritance and Overriding)
==========================================================

A DigitalProduct "is-a" Product that exists only in the virtual realm: it
has no weight, but it does have a download size.

This class:
- inherits from Product and reuses its constructor with super();
- adds the download_size attribute;
- overrides display_information() and reuses the parent version first;
- implements the abstract get_fulfilment_info() from Product.

It deliberately does NOT implement CanBeShipped: digital products are
delivered by download, so shipping is not part of their contract.
"""

from product import Product


class DigitalProduct(Product):
    """
    A product that is delivered digitally and has a download size.

    Example:
        >>> editor = DigitalProduct("P011", "Photo Editor", 49.90, 999, 1200)
        >>> editor.display_information()
        ID: P011 | Name: Photo Editor | Price: $49.90 | Stock: 999
          Type: Digital | Download size: 1200.00 MB
          Fulfilment: Delivered digitally via download link.
    """

    PRODUCT_TYPE = "digital"

    def __init__(self, product_id, name=None, price=None, stock=None,
                 download_size=None):
        """
        Initialize a DigitalProduct.

        Args:
            product_id (str | dict): The product ID, or a dictionary containing
                the keys 'id', 'name', 'price', 'stock' and 'download_size'.
            name (str): Product name (ignored when a dictionary is supplied).
            price (float): Product price (ignored when a dictionary is supplied).
            stock (int): Current stock quantity (ignored when a dictionary is supplied).
            download_size (float): Size of the download in megabytes
                (ignored when a dictionary is supplied).

        Raises:
            ValueError: If no download size is supplied or it is not positive.
        """
        # Pull the extra attribute out before the parent handles the common ones
        if isinstance(product_id, dict):
            download_size = product_id.get("download_size", download_size)

        # Reuse the existing Product constructor (Lab 7, Section 1.3)
        super().__init__(product_id, name, price, stock)

        if download_size is None:
            raise ValueError("DigitalProduct requires a download size in megabytes.")

        self.__download_size = float(download_size)
        if self.__download_size <= 0:
            raise ValueError("Download size must be greater than zero.")

    def get_download_size(self):
        """
        Get the product's download size (getter for the encapsulated attribute).

        Returns:
            float: Download size in megabytes.
        """
        return self.__download_size

    def display_information(self):
        """
        Display the common product information plus the digital details.

        The parent implementation prints the shared fields, then this
        override adds the download size and the fulfilment method.

        Returns:
            str: The full multi-line product information.
        """
        # Reuse the parent behaviour instead of duplicating the common fields
        information = super().display_information()

        detail = f"  Type: Digital | Download size: {self.__download_size:.2f} MB"
        print(detail)

        fulfilment = f"  Fulfilment: {self.get_fulfilment_info()}"
        print(fulfilment)

        return "\n".join([information, detail, fulfilment])

    def get_fulfilment_info(self):
        """
        Implement the abstract method from Product.

        Returns:
            str: Description of how a digital product is delivered.
        """
        return "Delivered digitally via download link."

    def to_dict(self):
        """
        Extend the parent dictionary with the digital attributes.

        Returns:
            dict: Common product fields plus 'type' and 'download_size'.
        """
        data = super().to_dict()
        data["download_size"] = self.__download_size
        return data
