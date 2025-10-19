import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


class FileHandler:
    """Handle reading and writing recipe and ingredient data to JSON files"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.ingredients_file = self.data_dir / "ingredients.json"
        self.recipes_file = self.data_dir / "recipes.json"

        # Create data directory if it doesn't exist
        self.data_dir.mkdir(exist_ok=True)

        # Initialize JSON files if they don't exist
        self._initialize_files()

    def _initialize_files(self) -> None:
        """Create empty JSON files if they don't exist"""
        if not self.ingredients_file.exists():
            self._write_json(self.ingredients_file, [])

        if not self.recipes_file.exists():
            self._write_json(self.recipes_file, [])

    def _read_json(self, filepath: Path) -> List[Dict]:
        """Read and parse JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return []

    def _write_json(self, filepath: Path, data: List[Dict]) -> bool:
        """Write data to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")
            return False

    # Ingredient operations
    def load_ingredients(self) -> List[Dict]:
        """Load all ingredients from JSON file"""
        return self._read_json(self.ingredients_file)

    def save_ingredients(self, ingredients: List[Dict]) -> bool:
        """Save ingredients to JSON file"""
        return self._write_json(self.ingredients_file, ingredients)

    def add_ingredient(self, ingredient_dict: Dict) -> bool:
        """Add a single ingredient to the file"""
        ingredients = self.load_ingredients()

        # Check if ingredient already exists (by name)
        for ing in ingredients:
            if ing['name'].lower() == ingredient_dict['name'].lower():
                # Update existing ingredient
                ingredients.remove(ing)
                break

        ingredients.append(ingredient_dict)
        return self.save_ingredients(ingredients)

    def get_ingredient_by_name(self, name: str) -> Optional[Dict]:
        """Get a specific ingredient by name"""
        ingredients = self.load_ingredients()
        for ing in ingredients:
            if ing['name'].lower() == name.lower():
                return ing
        return None

    def delete_ingredient(self, name: str) -> bool:
        """Delete an ingredient by name"""
        ingredients = self.load_ingredients()
        original_count = len(ingredients)
        ingredients = [ing for ing in ingredients if ing['name'].lower() != name.lower()]

        if len(ingredients) < original_count:
            return self.save_ingredients(ingredients)
        return False

    def clear_all_ingredients(self) -> bool:
        """Clear all ingredients"""
        return self._write_json(self.ingredients_file, [])

    # Recipe operations
    def load_recipes(self) -> List[Dict]:
        """Load all recipes from JSON file"""
        return self._read_json(self.recipes_file)

    def save_recipes(self, recipes: List[Dict]) -> bool:
        """Save recipes to JSON file"""
        return self._write_json(self.recipes_file, recipes)

    def add_recipe(self, recipe_dict: Dict) -> bool:
        """Add a single recipe to the file"""
        recipes = self.load_recipes()

        # Check if recipe already exists (by name)
        for rec in recipes:
            if rec['name'].lower() == recipe_dict['name'].lower():
                # Update existing recipe
                recipes.remove(rec)
                break

        recipes.append(recipe_dict)
        return self.save_recipes(recipes)

    def get_recipe_by_name(self, name: str) -> Optional[Dict]:
        """Get a specific recipe by name"""
        recipes = self.load_recipes()
        for rec in recipes:
            if rec['name'].lower() == name.lower():
                return rec
        return None

    def delete_recipe(self, name: str) -> bool:
        """Delete a recipe by name"""
        recipes = self.load_recipes()
        original_count = len(recipes)
        recipes = [rec for rec in recipes if rec['name'].lower() != name.lower()]

        if len(recipes) < original_count:
            return self.save_recipes(recipes)
        return False

    def clear_all_recipes(self) -> bool:
        """Clear all recipes"""
        return self._write_json(self.recipes_file, [])

    # Utility operations
    def export_all_data(self, export_path: str) -> bool:
        """Export all data to a single JSON file"""
        try:
            data = {
                'ingredients': self.load_ingredients(),
                'recipes': self.load_recipes(),
                'exported_at': datetime.now().isoformat()
            }
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data exported to {export_path}")
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False

    def import_all_data(self, import_path: str) -> bool:
        """Import all data from an export file"""
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)

            self.save_ingredients(data.get('ingredients', []))
            self.save_recipes(data.get('recipes', []))
            print(f"Data imported from {import_path}")
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False

    def backup_data(self, backup_path: str) -> bool:
        """Create a backup of current data"""
        return self.export_all_data(backup_path)

    def get_data_summary(self) -> Dict:
        """Get summary statistics of stored data"""
        ingredients = self.load_ingredients()
        recipes = self.load_recipes()

        return {
            'total_ingredients': len(ingredients),
            'total_recipes': len(recipes),
            'ingredients_file': str(self.ingredients_file),
            'recipes_file': str(self.recipes_file)
        }