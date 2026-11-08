"""Supplier model for the inventory management system."""


class Supplier:
    """A supplier that exists independently of the products it supplies."""

    def __init__(
        self, supplier_id: str, name: str, contact_email: str
    ) -> None:
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> str:
        """Print and return the supplier's identifying information."""
        information = (
            f"Supplier: {self.supplier_id} | Name: {self.name} | "
            f"Email: {self.contact_email}"
        )
        print(information)
        return information

    def to_dict(self) -> dict[str, str]:
        """Return the supplier details in a JSON-serialisable form."""
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Supplier":
        """Build a Supplier from persisted supplier details."""
        return cls(
            supplier_id=str(data["supplier_id"]),
            name=str(data["name"]),
            contact_email=str(data["contact_email"]),
        )


DEFAULT_SUPPLIER: Supplier = Supplier(
    "SUP-UNKNOWN", "Unknown Supplier", "unknown@example.invalid"
)
