from typing import List, Dict, Optional, Tuple
from datetime import datetime
from .ingredient import Ingredient


class RecipeIngredient:
    """Represents an ingredient in a recipe with specific quantity and unit"""

    def __init__(self, name: str, quantity: float, unit: str, optional: bool = False):
        self.name = name.lower().strip()
        self.quantity = float(quantity)
        self.unit = unit.lower().strip()
        self.optional = optional

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'optional': self.optional
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecipeIngredient':
        return cls(
            name=data['name'],
            quantity=data['quantity'],
            unit=data['unit'],
            optional=data.get('optional', False)
        )

    def __str__(self) -> str:
        optional_text = " (optional)" if self.optional else ""
        return f"{self.quantity} {self.unit} {self.name}{optional_text}"

    def __repr__(self) -> str:
        return f"RecipeIngredient(name='{self.name}', quantity={self.quantity}, unit='{self.unit}')"


class Recipe:
    """Represents a recipe with ingredients, instructions, and metadata"""

    def __init__(
            self,
            name: str,
            servings: int,
            ingredients: List[RecipeIngredient],
            instructions: List[str],
            prep_time: int = 0,
            cook_time: int = 0,
            difficulty: str = "medium",
            cuisine: str = "other",
            dietary_tags: List[str] = None
    ):
        self.name = name.strip()
        self.servings = int(servings)
        self.ingredients = ingredients
        self.instructions = instructions
        self.prep_time = prep_time  # minutes
        self.cook_time = cook_time  # minutes
        self.difficulty = difficulty  # easy, medium, hard
        self.cuisine = cuisine
        self.dietary_tags = dietary_tags or []
        self.created_at = datetime.now()
        self.rating = 0.0
        self.times_made = 0

    @property
    def total_time(self) -> int:
        """Total cooking time in minutes"""
        return self.prep_time + self.cook_time

    def scale_recipe(self, new_servings: int) -> 'Recipe':
        """Create a new recipe scaled for different servings"""
        scale_factor = new_servings / self.servings

        # Scale ingredients
        scaled_ingredients = []
        for ingredient in self.ingredients:
            scaled_quantity = self._smart_scale_ingredient(
                ingredient.name,
                ingredient.quantity,
                scale_factor
            )
            scaled_ingredients.append(RecipeIngredient(
                name=ingredient.name,
                quantity=scaled_quantity,
                unit=ingredient.unit,
                optional=ingredient.optional
            ))

        # Create scaled recipe
        scaled_recipe = Recipe(
            name=f"{self.name} (scaled for {new_servings})",
            servings=new_servings,
            ingredients=scaled_ingredients,
            instructions=self.instructions.copy(),
            prep_time=self.prep_time,
            cook_time=self.cook_time,
            difficulty=self.difficulty,
            cuisine=self.cuisine,
            dietary_tags=self.dietary_tags.copy()
        )
        return scaled_recipe

    def _smart_scale_ingredient(self, ingredient_name: str, quantity: float, scale_factor: float) -> float:
        """Apply intelligent scaling based on ingredient type"""
        # Ingredients that don't scale linearly
        spices_and_seasonings = {
            'salt', 'pepper', 'garlic powder', 'onion powder', 'paprika',
            'cumin', 'oregano', 'basil', 'thyme', 'rosemary', 'sage',
            'cayenne', 'chili powder', 'black pepper', 'vanilla extract'
        }

        leavening_agents = {
            'baking powder', 'baking soda', 'yeast', 'cream of tartar'
        }

        if ingredient_name in spices_and_seasonings:
            # Scale spices more conservatively
            if scale_factor > 1:
                return quantity * (1 + (scale_factor - 1) * 0.8)
            else:
                return quantity * scale_factor
        elif ingredient_name in leavening_agents:
            # Leavening agents need careful scaling
            if scale_factor <= 2:
                return quantity * scale_factor
            else:
                # For large scaling, increase more conservatively
                return quantity * (2 + (scale_factor - 2) * 0.5)
        else:
            # Regular ingredients scale normally
            return quantity * scale_factor

    def calculate_match_score(self, available_ingredients: List[Ingredient]) -> Tuple[float, List[str], List[str]]:
        """
        Calculate how well available ingredients match this recipe
        Returns: (match_score, missing_ingredients, available_ingredients)
        """
        available_dict = {ing.name: ing for ing in available_ingredients}
        total_ingredients = len([ing for ing in self.ingredients if not ing.optional])
        matched_ingredients = 0
        missing_ingredients = []
        matched_list = []

        for recipe_ingredient in self.ingredients:
            if recipe_ingredient.optional:
                continue

            if recipe_ingredient.name in available_dict:
                available_ing = available_dict[recipe_ingredient.name]
                # Check if we have enough quantity (simplified - assumes same units)
                if available_ing.quantity >= recipe_ingredient.quantity:
                    matched_ingredients += 1
                    matched_list.append(recipe_ingredient.name)
                else:
                    missing_ingredients.append(
                        f"{recipe_ingredient.name} (need {recipe_ingredient.quantity} {recipe_ingredient.unit}, "
                        f"have {available_ing.quantity} {available_ing.unit})"
                    )
            else:
                missing_ingredients.append(
                    f"{recipe_ingredient.quantity} {recipe_ingredient.unit} {recipe_ingredient.name}"
                )

        match_score = matched_ingredients / total_ingredients if total_ingredients > 0 else 0
        return match_score, missing_ingredients, matched_list

    def get_shopping_list(self, available_ingredients: List[Ingredient]) -> List[str]:
        """Generate shopping list for missing ingredients"""
        _, missing_ingredients, _ = self.calculate_match_score(available_ingredients)
        return missing_ingredients

    def to_dict(self) -> dict:
        """Convert recipe to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'servings': self.servings,
            'ingredients': [ing.to_dict() for ing in self.ingredients],
            'instructions': self.instructions,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'difficulty': self.difficulty,
            'cuisine': self.cuisine,
            'dietary_tags': self.dietary_tags,
            'created_at': self.created_at.isoformat(),
            'rating': self.rating,
            'times_made': self.times_made
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Recipe':
        """Create recipe from dictionary"""
        ingredients = [RecipeIngredient.from_dict(ing_data) for ing_data in data['ingredients']]
        recipe = cls(
            name=data['name'],
            servings=data['servings'],
            ingredients=ingredients,
            instructions=data['instructions'],
            prep_time=data.get('prep_time', 0),
            cook_time=data.get('cook_time', 0),
            difficulty=data.get('difficulty', 'medium'),
            cuisine=data.get('cuisine', 'other'),
            dietary_tags=data.get('dietary_tags', [])
        )

        if 'created_at' in data:
            recipe.created_at = datetime.fromisoformat(data['created_at'])
        if 'rating' in data:
            recipe.rating = data['rating']
        if 'times_made' in data:
            recipe.times_made = data['times_made']

        return recipe

    def __str__(self) -> str:
        return f"{self.name} (serves {self.servings}, {self.total_time} min total)"

    def __repr__(self) -> str:
        return f"Recipe(name='{self.name}', servings={self.servings})"