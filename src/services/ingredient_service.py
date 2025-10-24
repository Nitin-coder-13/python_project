from typing import List, Optional
from src.models.ingredient import Ingredient
from src.utils.filehandler import FileHandler


class IngredientService:
    """Service layer for managing ingredients"""

    def __init__(self, data_dir: str = "data"):
        self.file_handler = FileHandler(data_dir)

    def add_ingredient(self, ingredient: Ingredient) -> bool:
        """Add a new ingredient or update existing one"""
        return self.file_handler.add_ingredient(ingredient.to_dict())

    def get_all_ingredients(self) -> List[Ingredient]:
        """Get all ingredients from file"""
        ingredients_data = self.file_handler.load_ingredients()
        return [Ingredient.from_dict(ing_data) for ing_data in ingredients_data]

    def get_ingredient_by_name(self, name: str) -> Optional[Ingredient]:
        """Get a specific ingredient by name"""
        ing_data = self.file_handler.get_ingredient_by_name(name)
        if ing_data:
            return Ingredient.from_dict(ing_data)
        return None

    def delete_ingredient(self, name: str) -> bool:
        """Delete an ingredient by name"""
        return self.file_handler.delete_ingredient(name)

    def get_expiring_ingredients(self, days: int = 7) -> List[Ingredient]:
        """Get ingredients expiring within specified days"""
        all_ingredients = self.get_all_ingredients()
        expiring = []

        for ingredient in all_ingredients:
            days_left = ingredient.days_until_expiry()
            if days_left is not None and days_left <= days:
                expiring.append(ingredient)

        return sorted(expiring, key=lambda x: x.days_until_expiry() or 999)

    def clear_all_ingredients(self) -> bool:
        """Clear all ingredients"""
        return self.file_handler.clear_all_ingredients()

    def backup_data(self, backup_path: str) -> bool:
        """Create a backup of ingredients"""
        return self.file_handler.backup_data(backup_path)

    def get_total_count(self) -> int:
        """Get total number of ingredients"""
        return len(self.get_all_ingredients())

    def get_expiring_soon(self, days: int = 7) -> List[Ingredient]:
        """Get ingredients expiring within specified days"""
        all_ingredients = self.get_all_ingredients()
        expiring = []

        for ingredient in all_ingredients:
            if ingredient.expiration_date:
                days_left = ingredient.days_until_expiry()
                if days_left is not None and 0 <= days_left <= days:
                    expiring.append(ingredient)

        return sorted(expiring, key=lambda x: x.days_until_expiry() or 999)

    def get_expired_ingredients(self) -> List[Ingredient]:
        """Get all expired ingredients"""
        all_ingredients = self.get_all_ingredients()
        return [ing for ing in all_ingredients if ing.is_expired()]

    def get_ingredients_by_category(self, category: str) -> List[Ingredient]:
        """Get ingredients filtered by category"""
        all_ingredients = self.get_all_ingredients()
        return [ing for ing in all_ingredients if ing.category.lower() == category.lower()]