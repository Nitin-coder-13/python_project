import pytest
from datetime import date, timedelta
from src.models.ingredient import Ingredient


class TestIngredientCreation:
    """Test ingredient creation and initialization"""

    def test_ingredient_basic_creation(self):
        """Test creating a basic ingredient without expiration"""
        ingredient = Ingredient("flour", 2.0, "cups")

        assert ingredient.name == "flour"
        assert ingredient.quantity == 2.0
        assert ingredient.unit == "cups"
        assert ingredient.category == "other"
        assert ingredient.cost_per_unit == 0.0

    def test_ingredient_with_category(self):
        """Test creating ingredient with category"""
        ingredient = Ingredient("milk", 1.0, "liter", category="dairy")

        assert ingredient.name == "milk"
        assert ingredient.category == "dairy"

    def test_ingredient_name_normalization(self):
        """Test that ingredient names are lowercased and stripped"""
        ingredient = Ingredient("  FLOUR  ", 2.0, "cups")

        assert ingredient.name == "flour"
        assert ingredient.unit == "cups"

    def test_ingredient_with_expiration(self):
        """Test creating ingredient with expiration date"""
        future_date = date.today() + timedelta(days=7)
        ingredient = Ingredient("milk", 1.0, "liter", expiration_date=future_date)

        assert ingredient.expiration_date == future_date


class TestIngredientExpiration:
    """Test expiration-related methods"""

    def test_ingredient_not_expired(self):
        """Test ingredient that hasn't expired"""
        future_date = date.today() + timedelta(days=7)
        ingredient = Ingredient("milk", 1.0, "liter", expiration_date=future_date)

        assert not ingredient.is_expired()

    def test_ingredient_is_expired(self):
        """Test ingredient that has expired"""
        past_date = date.today() - timedelta(days=1)
        ingredient = Ingredient("milk", 1.0, "liter", expiration_date=past_date)

        assert ingredient.is_expired()

    def test_ingredient_no_expiration(self):
        """Test ingredient with no expiration date"""
        ingredient = Ingredient("salt", 1.0, "kg")

        assert not ingredient.is_expired()

    def test_days_until_expiry_future(self):
        """Test days until expiry for future expiration"""
        future_date = date.today() + timedelta(days=7)
        ingredient = Ingredient("milk", 1.0, "liter", expiration_date=future_date)

        assert ingredient.days_until_expiry() == 7

    def test_days_until_expiry_past(self):
        """Test days until expiry for past expiration"""
        past_date = date.today() - timedelta(days=3)
        ingredient = Ingredient("milk", 1.0, "liter", expiration_date=past_date)

        assert ingredient.days_until_expiry() == -3

    def test_days_until_expiry_none(self):
        """Test days until expiry when no expiration date"""
        ingredient = Ingredient("salt", 1.0, "kg")

        assert ingredient.days_until_expiry() is None


class TestIngredientQuantity:
    """Test quantity-related operations"""

    def test_update_quantity(self):
        """Test updating ingredient quantity"""
        ingredient = Ingredient("flour", 5.0, "cups")
        ingredient.update_quantity(3.0)

        assert ingredient.quantity == 3.0

    def test_update_quantity_to_zero(self):
        """Test updating quantity to zero"""
        ingredient = Ingredient("flour", 5.0, "cups")
        ingredient.update_quantity(0.0)

        assert ingredient.quantity == 0.0

    def test_update_quantity_negative_becomes_zero(self):
        """Test that negative quantity becomes zero"""
        ingredient = Ingredient("flour", 5.0, "cups")
        ingredient.update_quantity(-5.0)

        assert ingredient.quantity == 0.0

    def test_use_quantity_successful(self):
        """Test using quantity successfully"""
        ingredient = Ingredient("flour", 5.0, "cups")
        success = ingredient.use_quantity(2.0)

        assert success is True
        assert ingredient.quantity == 3.0

    def test_use_quantity_insufficient(self):
        """Test using quantity when insufficient"""
        ingredient = Ingredient("flour", 2.0, "cups")
        success = ingredient.use_quantity(5.0)

        assert success is False
        assert ingredient.quantity == 2.0  # Unchanged

    def test_use_quantity_exact_amount(self):
        """Test using exact amount available"""
        ingredient = Ingredient("flour", 2.0, "cups")
        success = ingredient.use_quantity(2.0)

        assert success is True
        assert ingredient.quantity == 0.0

    def test_is_sufficient_true(self):
        """Test is_sufficient returns True when enough"""
        ingredient = Ingredient("flour", 5.0, "cups")

        assert ingredient.is_sufficient(3.0) is True
        assert ingredient.is_sufficient(5.0) is True

    def test_is_sufficient_false(self):
        """Test is_sufficient returns False when insufficient"""
        ingredient = Ingredient("flour", 2.0, "cups")

        assert ingredient.is_sufficient(3.0) is False


class TestIngredientSerialization:
    """Test converting ingredient to/from dictionary"""

    def test_to_dict_basic(self):
        """Test converting ingredient to dictionary"""
        ingredient = Ingredient("flour", 2.0, "cups", category="grains")
        data = ingredient.to_dict()

        assert data['name'] == "flour"
        assert data['quantity'] == 2.0
        assert data['unit'] == "cups"
        assert data['category'] == "grains"
        assert 'created_at' in data
        assert 'last_updated' in data

    def test_to_dict_with_expiration(self):
        """Test converting ingredient with expiration to dictionary"""
        future_date = date.today() + timedelta(days=7)
        ingredient = Ingredient("milk", 1.0, "liter", expiration_date=future_date, category="dairy")
        data = ingredient.to_dict()

        assert data['expiration_date'] is not None
        assert data['expiration_date'] == future_date.isoformat()

    def test_from_dict_basic(self):
        """Test creating ingredient from dictionary"""
        data = {
            'name': 'flour',
            'quantity': 2.0,
            'unit': 'cups',
            'expiration_date': None,
            'category': 'grains',
            'cost_per_unit': 0.5,
            'created_at': date.today().isoformat(),
            'last_updated': date.today().isoformat()
        }

        ingredient = Ingredient.from_dict(data)

        assert ingredient.name == "flour"
        assert ingredient.quantity == 2.0
        assert ingredient.unit == "cups"

    def test_serialization_roundtrip(self):
        """Test that serialization and deserialization preserve data"""
        original = Ingredient("flour", 2.0, "cups", category="grains", cost_per_unit=1.5)

        # Convert to dict and back
        data = original.to_dict()
        recreated = Ingredient.from_dict(data)

        assert recreated.name == original.name
        assert recreated.quantity == original.quantity
        assert recreated.unit == original.unit
        assert recreated.category == original.category
        assert recreated.cost_per_unit == original.cost_per_unit


class TestIngredientStringRepresentation:
    """Test string representations"""

    def test_str_basic(self):
        """Test string representation of basic ingredient"""
        ingredient = Ingredient("flour", 2.0, "cups")

        assert "2.0 cups flour" in str(ingredient)

    def test_str_with_expiration(self):
        """Test string representation with expiration"""
        future_date = date.today() + timedelta(days=7)
        ingredient = Ingredient("milk", 1.0, "liter", expiration_date=future_date)

        assert "1.0 liter milk" in str(ingredient)
        assert "expires" in str(ingredient)

    def test_repr(self):
        """Test repr representation"""
        ingredient = Ingredient("flour", 2.0, "cups")
        repr_str = repr(ingredient)

        assert "Ingredient" in repr_str
        assert "flour" in repr_str
        assert "2.0" in repr_str