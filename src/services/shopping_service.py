from typing import List, Dict
from collections import defaultdict
from src.models.recipe import Recipe
from src.models.ingredient import Ingredient
from src.utils.unit_converter_ import UnitConverter


class ShoppingService:
    """Service for generating shopping lists"""

    def __init__(self):
        self.unit_converter = UnitConverter()
        self.category_mapping = {
            'vegetables': '🥬 Vegetables',
            'fruits': '🍎 Fruits',
            'dairy': '🥛 Dairy',
            'meat': '🥩 Meat & Poultry',
            'grains': '🌾 Grains & Bread',
            'spices': '🧂 Spices & Seasonings',
            'pantry': '🥫 Pantry Staples',
            'other': '📦 Other'
        }

    def generate_shopping_list(
            self,
            recipes: List[Recipe],
            available_ingredients: List[Ingredient],
            servings_multiplier: Dict[str, float] = None
    ) -> List[Dict]:
        """
        Generate shopping list for multiple recipes

        Args:
            recipes: List of recipes to make
            available_ingredients: What you already have
            servings_multiplier: Optional dict mapping recipe names to serving multipliers

        Returns:
            List of items to buy with quantities and categories
        """
        if servings_multiplier is None:
            servings_multiplier = {}

        # Calculate total needed ingredients
        needed_ingredients = defaultdict(lambda: {'quantity': 0, 'unit': None, 'category': 'other'})

        for recipe in recipes:
            multiplier = servings_multiplier.get(recipe.name, 1.0)

            for recipe_ing in recipe.ingredients:
                if recipe_ing.optional:
                    continue

                # Scale quantity if needed
                scaled_quantity = recipe_ing.quantity * multiplier

                # Convert to standard unit for aggregation
                standard_quantity = self.unit_converter.convert_to_standard_unit(
                    scaled_quantity, recipe_ing.unit
                )

                # Store in standard units for now
                key = recipe_ing.name
                needed_ingredients[key]['quantity'] += standard_quantity
                needed_ingredients[key]['unit'] = recipe_ing.unit  # Keep original unit
                needed_ingredients[key]['category'] = self._guess_category(recipe_ing.name)

        # Subtract what we already have
        available_dict = {ing.name: ing for ing in available_ingredients}
        shopping_list = []

        for ing_name, needed_data in needed_ingredients.items():
            needed_quantity = needed_data['quantity']
            needed_unit = needed_data['unit']
            category = needed_data['category']

            if ing_name in available_dict:
                available_ing = available_dict[ing_name]
                available_standard = self.unit_converter.convert_to_standard_unit(
                    available_ing.quantity, available_ing.unit
                )

                if available_standard >= needed_quantity:
                    continue  # We have enough

                # Calculate shortfall
                shortfall = needed_quantity - available_standard

                # Convert back to original unit
                final_quantity = self.unit_converter.convert_units(
                    shortfall,
                    self._get_standard_unit_for_type(needed_unit),
                    needed_unit
                )
            else:
                # Don't have this ingredient at all
                final_quantity = self.unit_converter.convert_units(
                    needed_quantity,
                    self._get_standard_unit_for_type(needed_unit),
                    needed_unit
                )

            if final_quantity and final_quantity > 0:
                shopping_list.append({
                    'name': ing_name,
                    'quantity': round(final_quantity, 2),
                    'unit': needed_unit,
                    'category': category
                })

        return sorted(shopping_list, key=lambda x: (x['category'], x['name']))

    def _get_standard_unit_for_type(self, unit: str) -> str:
        """Get standard unit based on unit type"""
        unit_type = self.unit_converter._get_unit_type(unit)
        if unit_type == 'volume':
            return 'ml'
        elif unit_type == 'weight':
            return 'g'
        return unit

    def _guess_category(self, ingredient_name: str) -> str:
        """Guess ingredient category based on name"""
        name_lower = ingredient_name.lower()

        vegetables = ['lettuce', 'tomato', 'onion', 'garlic', 'potato', 'carrot', 'pepper',
                      'broccoli', 'spinach', 'cucumber', 'celery']
        fruits = ['apple', 'banana', 'orange', 'lemon', 'lime', 'berry', 'strawberry',
                  'grape', 'melon', 'peach']
        dairy = ['milk', 'cheese', 'butter', 'yogurt', 'cream', 'sour cream', 'buttermilk']
        meat = ['chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon', 'tuna', 'shrimp',
                'bacon', 'ham']
        grains = ['flour', 'bread', 'rice', 'pasta', 'oats', 'cereal', 'tortilla']
        spices = ['salt', 'pepper', 'cinnamon', 'paprika', 'cumin', 'oregano', 'basil',
                  'thyme', 'vanilla', 'garlic powder', 'onion powder']

        for veg in vegetables:
            if veg in name_lower:
                return 'vegetables'
        for fruit in fruits:
            if fruit in name_lower:
                return 'fruits'
        for d in dairy:
            if d in name_lower:
                return 'dairy'
        for m in meat:
            if m in name_lower:
                return 'meat'
        for g in grains:
            if g in name_lower:
                return 'grains'
        for s in spices:
            if s in name_lower:
                return 'spices'

        return 'other'

    def format_shopping_list(self, shopping_list: List[Dict]) -> str:
        """Format shopping list as readable text"""
        if not shopping_list:
            return "✅ You have all ingredients needed!"

        output = []
        output.append("🛒 SHOPPING LIST")
        output.append("=" * 50)

        # Group by category
        by_category = defaultdict(list)
        for item in shopping_list:
            category = item['category']
            by_category[category].append(item)

        for category in sorted(by_category.keys()):
            category_name = self.category_mapping.get(category, f"📦 {category.title()}")
            output.append(f"\n{category_name}:")

            for item in sorted(by_category[category], key=lambda x: x['name']):
                quantity_str = self.unit_converter.format_quantity(item['quantity'], item['unit'])
                output.append(f"  ☐ {quantity_str} {item['name']}")

        return "\n".join(output)

    def export_shopping_list(self, shopping_list: List[Dict], filename: str) -> bool:
        """Export shopping list to text file"""
        try:
            formatted = self.format_shopping_list(shopping_list)
            with open(filename, 'w') as f:
                f.write(formatted)
            return True
        except Exception as e:
            print(f"Error exporting shopping list: {e}")
            return False

    def calculate_estimated_items_count(self, shopping_list: List[Dict]) -> Dict[str, int]:
        """Calculate statistics about shopping list"""
        by_category = defaultdict(int)
        for item in shopping_list:
            by_category[item['category']] += 1

        return {
            'total_items': len(shopping_list),
            'by_category': dict(by_category)
        }