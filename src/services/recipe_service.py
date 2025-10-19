from typing import List, Optional
from src.models.recipe import Recipe
from src.utils.filehandler import FileHandler


class RecipeService:
    """Service layer for managing recipes"""

    def __init__(self, data_dir: str = "data"):
        self.file_handler = FileHandler(data_dir)

    def add_recipe(self, recipe: Recipe) -> bool:
        """Add a new recipe or update existing one"""
        return self.file_handler.add_recipe(recipe.to_dict())

    def get_all_recipes(self) -> List[Recipe]:
        """Get all recipes from file"""
        recipes_data = self.file_handler.load_recipes()
        return [Recipe.from_dict(rec_data) for rec_data in recipes_data]

    def get_recipe_by_name(self, name: str) -> Optional[Recipe]:
        """Get a specific recipe by name"""
        rec_data = self.file_handler.get_recipe_by_name(name)
        if rec_data:
            return Recipe.from_dict(rec_data)
        return None

    def delete_recipe(self, name: str) -> bool:
        """Delete a recipe by name"""
        return self.file_handler.delete_recipe(name)

    def get_recipes_by_difficulty(self, difficulty: str) -> List[Recipe]:
        """Get recipes filtered by difficulty level"""
        all_recipes = self.get_all_recipes()
        return [rec for rec in all_recipes if rec.difficulty.lower() == difficulty.lower()]

    def get_recipes_by_time(self, max_time: int) -> List[Recipe]:
        """Get recipes that can be made within specified time"""
        all_recipes = self.get_all_recipes()
        return [rec for rec in all_recipes if rec.total_time <= max_time]

    def clear_all_recipes(self) -> bool:
        """Clear all recipes"""
        return self.file_handler.clear_all_recipes()

    def get_total_count(self) -> int:
        """Get total number of recipes"""
        return len(self.get_all_recipes())