from datetime import datetime, date
from typing import Optional


class Ingredient:
    def __init__(
            self,
            name: str,
            quantity: float,
            unit: str,
            expiration_date: Optional[date] = None,
            category: str = "other",
            cost_per_unit: float = 0.0
    ):
        self.name = name.lower().strip()
        self.quantity = float(quantity)
        self.unit = unit.lower().strip()
        self.expiration_date = expiration_date
        self.category = category
        self.cost_per_unit = cost_per_unit
        self.created_at = datetime.now()
        self.last_updated = datetime.now()

    def is_expired(self) -> bool:
        """Check if ingredient is past expiration date"""
        if not self.expiration_date:
            return False
        return date.today() > self.expiration_date

    def days_until_expiry(self) -> Optional[int]:
        """Calculate days until expiration"""
        if not self.expiration_date:
            return None
        delta = self.expiration_date - date.today()
        return delta.days

    def update_quantity(self, new_quantity: float) -> None:
        """Update ingredient quantity"""
        self.quantity = max(0, float(new_quantity))
        self.last_updated = datetime.now()

    def use_quantity(self, amount: float) -> bool:
        """Use specified amount, return True if successful"""
        if self.quantity >= amount:
            self.quantity -= amount
            self.last_updated = datetime.now()
            return True
        return False

    def is_sufficient(self, required_amount: float) -> bool:
        """Check if we have enough quantity"""
        return self.quantity >= required_amount

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'category': self.category,
            'cost_per_unit': self.cost_per_unit,
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Ingredient':
        """Create ingredient from dictionary"""
        expiration_date = None
        if data.get('expiration_date'):
            expiration_date = datetime.fromisoformat(data['expiration_date']).date()

        ingredient = cls(
            name=data['name'],
            quantity=data['quantity'],
            unit=data['unit'],
            expiration_date=expiration_date,
            category=data.get('category', 'other'),
            cost_per_unit=data.get('cost_per_unit', 0.0)
        )

        if 'created_at' in data:
            ingredient.created_at = datetime.fromisoformat(data['created_at'])
        if 'last_updated' in data:
            ingredient.last_updated = datetime.fromisoformat(data['last_updated'])

        return ingredient

    def __str__(self) -> str:
        expiry_info = f" (expires {self.expiration_date})" if self.expiration_date else ""
        return f"{self.quantity} {self.unit} {self.name}{expiry_info}"

    def __repr__(self) -> str:
        return f"Ingredient(name='{self.name}', quantity={self.quantity}, unit='{self.unit}')"