from typing import List, Dict, Tuple, Optional
from src.models.ingredient import Ingredient
from src.models.recipe import Recipe
from src.utils.unit_converter_ import UnitConverter


class RecipeMatchingService:
    """Service for matching recipes with available ingredients"""

    def __init__(self):
        self.unit_converter = UnitConverter()
        self.substitutions = self._load_substitutions()

    def find_matching_recipes(
            self,
            available_ingredients: List[Ingredient],
            all_recipes: List[Recipe],
            min_match_score: float = 0.7,
            allow_substitutions: bool = True
    ) -> List[Tuple[Recipe, float, List[str], List[str]]]:
        """
        Find recipes that match available ingredients

        Args:
            available_ingredients: List of ingredients user has
            all_recipes: All recipes to search through
            min_match_score: Minimum match percentage (0.0 to 1.0)
            allow_substitutions: Whether to consider ingredient substitutions

        Returns:
            List of tuples: (recipe, match_score, missing_ingredients, matched_ingredients)
        """
        matches = []

        for recipe in all_recipes:
            match_score, missing, matched = self._calculate_detailed_match_score(
                recipe, available_ingredients, allow_substitutions
            )

            if match_score >= min_match_score:
                matches.append((recipe, match_score, missing, matched))

        # Sort by match score (highest first), then by recipe rating
        matches.sort(key=lambda x: (-x[1], -x[0].rating))

        return matches

    def _calculate_detailed_match_score(
            self,
            recipe: Recipe,
            available_ingredients: List[Ingredient],
            allow_substitutions: bool = True
    ) -> Tuple[float, List[str], List[str]]:
        """
        Calculate detailed match score with unit conversion and substitution support

        Returns:
            (match_score, missing_ingredients, matched_ingredients)
        """
        available_dict = {ing.name: ing for ing in available_ingredients}
        required_ingredients = [ing for ing in recipe.ingredients if not ing.optional]
        total_required = len(required_ingredients)

        if total_required == 0:
            return 1.0, [], []

        matched_count = 0
        missing_ingredients = []
        matched_ingredients = []

        for recipe_ingredient in required_ingredients:
            found = False

            # Try direct match first
            if recipe_ingredient.name in available_dict:
                available_ing = available_dict[recipe_ingredient.name]

                # Convert units for comparison
                required_quantity = self.unit_converter.convert_to_standard_unit(
                    recipe_ingredient.quantity, recipe_ingredient.unit
                )
                available_quantity = self.unit_converter.convert_to_standard_unit(
                    available_ing.quantity, available_ing.unit
                )

                if available_quantity >= required_quantity:
                    matched_count += 1
                    matched_ingredients.append(recipe_ingredient.name)
                    found = True
                else:
                    missing_ingredients.append(
                        f"{recipe_ingredient.name} (need {recipe_ingredient.quantity} "
                        f"{recipe_ingredient.unit}, have {available_ing.quantity} {available_ing.unit})"
                    )
                    found = True  # Found but insufficient

            # Try substitutions if direct match not found
            if not found and allow_substitutions:
                substitute_found = False

                if recipe_ingredient.name in self.substitutions:
                    for substitute in self.substitutions[recipe_ingredient.name]:
                        if substitute['ingredient'] in available_dict:
                            available_ing = available_dict[substitute['ingredient']]

                            # Apply conversion ratio for substitute
                            needed_quantity = recipe_ingredient.quantity * substitute.get('ratio', 1.0)

                            if available_ing.quantity >= needed_quantity:
                                matched_count += 0.8  # Partial credit for substitution
                                matched_ingredients.append(
                                    f"{substitute['ingredient']} (sub for {recipe_ingredient.name})"
                                )
                                substitute_found = True
                                break

                if not substitute_found:
                    missing_ingredients.append(
                        f"{recipe_ingredient.quantity} {recipe_ingredient.unit} {recipe_ingredient.name}"
                    )

            # If no direct match and substitutions not allowed/found
            elif not found:
                missing_ingredients.append(
                    f"{recipe_ingredient.quantity} {recipe_ingredient.unit} {recipe_ingredient.name}"
                )

        match_score = matched_count / total_required if total_required > 0 else 0
        return match_score, missing_ingredients, matched_ingredients

    def _load_substitutions(self) -> Dict[str, List[Dict]]:
        """Load ingredient substitution rules"""
        return {
            'milk': [
                {'ingredient': 'buttermilk', 'ratio': 1.0, 'notes': 'Add 1 tbsp lemon juice'},
                {'ingredient': 'almond milk', 'ratio': 1.0, 'notes': 'May alter flavor slightly'},
                {'ingredient': 'coconut milk', 'ratio': 1.0, 'notes': 'Use light coconut milk'},
                {'ingredient': 'soy milk', 'ratio': 1.0, 'notes': 'Good dairy-free option'},
            ],
            'butter': [
                {'ingredient': 'oil', 'ratio': 0.75, 'notes': 'Use 3/4 the amount'},
                {'ingredient': 'margarine', 'ratio': 1.0, 'notes': 'Direct substitution'},
                {'ingredient': 'applesauce', 'ratio': 0.5, 'notes': 'For baking, use half the amount'},
                {'ingredient': 'coconut oil', 'ratio': 1.0, 'notes': 'Good for baking'},
            ],
            'egg': [
                {'ingredient': 'flax egg', 'ratio': 1.0, 'notes': '1 tbsp ground flaxseed + 3 tbsp water'},
                {'ingredient': 'banana', 'ratio': 0.25, 'notes': '1/4 cup mashed banana per egg'},
                {'ingredient': 'applesauce', 'ratio': 0.25, 'notes': '1/4 cup unsweetened applesauce'},
            ],
            'all-purpose flour': [
                {'ingredient': 'whole wheat flour', 'ratio': 1.0, 'notes': 'May need extra liquid'},
                {'ingredient': 'almond flour', 'ratio': 1.0, 'notes': 'Different texture, gluten-free'},
                {'ingredient': 'oat flour', 'ratio': 1.0, 'notes': 'Gluten-free option'},
            ],
            'sugar': [
                {'ingredient': 'honey', 'ratio': 0.75, 'notes': 'Reduce liquid by 1/4 cup'},
                {'ingredient': 'maple syrup', 'ratio': 0.75, 'notes': 'Reduce liquid by 3 tbsp'},
                {'ingredient': 'brown sugar', 'ratio': 1.0, 'notes': 'Direct substitution'},
            ],
            'yogurt': [
                {'ingredient': 'sour cream', 'ratio': 1.0, 'notes': 'Direct substitution'},
                {'ingredient': 'buttermilk', 'ratio': 1.0, 'notes': 'For baking'},
                {'ingredient': 'cottage cheese', 'ratio': 1.0, 'notes': 'Blend until smooth'},
            ],
        }

    def suggest_recipes_by_time(
            self,
            available_ingredients: List[Ingredient],
            all_recipes: List[Recipe],
            max_time: int,
            min_match_score: float = 0.8
    ) -> List[Tuple[Recipe, float]]:
        """Find recipes that can be made within time limit"""
        quick_recipes = [recipe for recipe in all_recipes if recipe.total_time <= max_time]
        matches = self.find_matching_recipes(available_ingredients, quick_recipes, min_match_score)

        return [(recipe, score) for recipe, score, _, _ in matches]

    def suggest_recipes_by_difficulty(
            self,
            available_ingredients: List[Ingredient],
            all_recipes: List[Recipe],
            difficulty: str,
            min_match_score: float = 0.8
    ) -> List[Tuple[Recipe, float]]:
        """Find recipes by difficulty level"""
        filtered_recipes = [recipe for recipe in all_recipes if recipe.difficulty == difficulty]
        matches = self.find_matching_recipes(available_ingredients, filtered_recipes, min_match_score)

        return [(recipe, score) for recipe, score, _, _ in matches]

    def get_substitution_suggestions(self, ingredient_name: str) -> List[Dict]:
        """Get substitution suggestions for a specific ingredient"""
        ingredient_name = ingredient_name.lower().strip()
        return self.substitutions.get(ingredient_name, [])

    def can_make_recipe(
            self,
            recipe: Recipe,
            available_ingredients: List[Ingredient],
            allow_substitutions: bool = True
    ) -> Tuple[bool, List[str]]:
        """
        Check if a recipe can be made with available ingredients

        Returns:
            (can_make, missing_ingredients)
        """
        match_score, missing, _ = self._calculate_detailed_match_score(
            recipe, available_ingredients, allow_substitutions
        )

        can_make = match_score >= 1.0
        return can_make, missing