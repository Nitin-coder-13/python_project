import pytest
from src.models.recipe import Recipe, RecipeIngredient
from src.models.ingredient import Ingredient


class TestRecipeIngredient:
    """Test RecipeIngredient class"""

    def test_recipe_ingredient_creation(self):
        """Test creating a recipe ingredient"""
        ing = RecipeIngredient("flour", 2.0, "cups")

        assert ing.name == "flour"
        assert ing.quantity == 2.0
        assert ing.unit == "cups"
        assert ing.optional is False

    def test_recipe_ingredient_optional(self):
        """Test creating optional recipe ingredient"""
        ing = RecipeIngredient("salt", 1.0, "tsp", optional=True)

        assert ing.optional is True

    def test_recipe_ingredient_to_dict(self):
        """Test converting recipe ingredient to dict"""
        ing = RecipeIngredient("flour", 2.0, "cups", optional=False)
        data = ing.to_dict()

        assert data['name'] == "flour"
        assert data['quantity'] == 2.0
        assert data['unit'] == "cups"
        assert data['optional'] is False

    def test_recipe_ingredient_from_dict(self):
        """Test creating recipe ingredient from dict"""
        data = {'name': 'flour', 'quantity': 2.0, 'unit': 'cups', 'optional': False}
        ing = RecipeIngredient.from_dict(data)

        assert ing.name == "flour"
        assert ing.quantity == 2.0
        assert ing.unit == "cups"


class TestRecipeCreation:
    """Test recipe creation and basic properties"""

    def test_recipe_basic_creation(self):
        """Test creating a basic recipe"""
        ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("milk", 1.0, "cup")
        ]
        instructions = ["Mix ingredients", "Cook"]

        recipe = Recipe(
            name="Pancakes",
            servings=4,
            ingredients=ingredients,
            instructions=instructions
        )

        assert recipe.name == "Pancakes"
        assert recipe.servings == 4
        assert len(recipe.ingredients) == 2
        assert len(recipe.instructions) == 2

    def test_recipe_with_times(self):
        """Test recipe with prep and cook times"""
        ingredients = [RecipeIngredient("flour", 2.0, "cups")]
        instructions = ["Mix", "Cook"]

        recipe = Recipe(
            name="Test Recipe",
            servings=4,
            ingredients=ingredients,
            instructions=instructions,
            prep_time=10,
            cook_time=15
        )

        assert recipe.prep_time == 10
        assert recipe.cook_time == 15
        assert recipe.total_time == 25

    def test_recipe_difficulty(self):
        """Test recipe difficulty levels"""
        ingredients = [RecipeIngredient("flour", 2.0, "cups")]
        instructions = ["Mix"]

        easy_recipe = Recipe("Easy", 2, ingredients, instructions, difficulty="easy")
        hard_recipe = Recipe("Hard", 2, ingredients, instructions, difficulty="hard")

        assert easy_recipe.difficulty == "easy"
        assert hard_recipe.difficulty == "hard"

    def test_recipe_dietary_tags(self):
        """Test recipe with dietary tags"""
        ingredients = [RecipeIngredient("flour", 2.0, "cups")]
        instructions = ["Mix"]

        recipe = Recipe(
            "Test",
            2,
            ingredients,
            instructions,
            dietary_tags=["vegetarian", "gluten-free"]
        )

        assert "vegetarian" in recipe.dietary_tags
        assert "gluten-free" in recipe.dietary_tags


class TestRecipeScaling:
    """Test recipe scaling functionality"""

    def test_scale_recipe_double(self):
        """Test scaling recipe to double servings"""
        ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("milk", 1.0, "cup")
        ]
        instructions = ["Mix", "Cook"]

        recipe = Recipe("Pancakes", 4, ingredients, instructions)
        scaled = recipe.scale_recipe(8)

        assert scaled.servings == 8
        assert scaled.ingredients[0].quantity == 4.0  # flour: 2 -> 4
        assert scaled.ingredients[1].quantity == 2.0  # milk: 1 -> 2

    def test_scale_recipe_half(self):
        """Test scaling recipe to half servings"""
        ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("milk", 1.0, "cup")
        ]
        instructions = ["Mix", "Cook"]

        recipe = Recipe("Pancakes", 4, ingredients, instructions)
        scaled = recipe.scale_recipe(2)

        assert scaled.servings == 2
        assert scaled.ingredients[0].quantity == 1.0  # flour: 2 -> 1
        assert scaled.ingredients[1].quantity == 0.5  # milk: 1 -> 0.5

    def test_smart_scaling_spices(self):
        """Test that spices scale conservatively"""
        ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("salt", 1.0, "tsp")
        ]
        instructions = ["Mix"]

        recipe = Recipe("Test", 2, ingredients, instructions)
        scaled = recipe.scale_recipe(4)  # Double

        # Flour should double exactly
        assert scaled.ingredients[0].quantity == 4.0

        # Salt should scale conservatively (less than double)
        salt_scaled = scaled.ingredients[1].quantity
        assert salt_scaled < 2.0  # Less than full double
        assert salt_scaled > 1.0  # But more than original

    def test_scaled_recipe_name(self):
        """Test that scaled recipe has appropriate name"""
        ingredients = [RecipeIngredient("flour", 2.0, "cups")]
        instructions = ["Mix"]

        recipe = Recipe("Pancakes", 4, ingredients, instructions)
        scaled = recipe.scale_recipe(8)

        assert "8" in scaled.name
        assert "Pancakes" in scaled.name


class TestRecipeMatching:
    """Test recipe matching with available ingredients"""

    def test_perfect_match(self):
        """Test recipe with all ingredients available"""
        recipe_ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("milk", 1.0, "cup")
        ]
        recipe = Recipe("Pancakes", 4, recipe_ingredients, ["Cook"])

        available = [
            Ingredient("flour", 3.0, "cups"),
            Ingredient("milk", 2.0, "cups")
        ]

        score, missing, matched = recipe.calculate_match_score(available)

        assert score == 1.0  # 100% match
        assert len(missing) == 0
        assert "flour" in matched
        assert "milk" in matched

    def test_partial_match(self):
        """Test recipe with some ingredients missing"""
        recipe_ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("milk", 1.0, "cup"),
            RecipeIngredient("eggs", 2.0, "pieces")
        ]
        recipe = Recipe("Pancakes", 4, recipe_ingredients, ["Cook"])

        available = [
            Ingredient("flour", 3.0, "cups"),
            Ingredient("milk", 2.0, "cups")
            # eggs missing
        ]

        score, missing, matched = recipe.calculate_match_score(available)

        assert score < 1.0  # Not perfect match
        assert score > 0.5  # But more than half
        assert len(missing) > 0
        assert any("eggs" in item for item in missing)

    def test_no_match(self):
        """Test recipe with no ingredients available"""
        recipe_ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("milk", 1.0, "cup")
        ]
        recipe = Recipe("Pancakes", 4, recipe_ingredients, ["Cook"])

        available = [
            Ingredient("sugar", 1.0, "cup"),
            Ingredient("salt", 1.0, "tsp")
        ]

        score, missing, matched = recipe.calculate_match_score(available)

        assert score == 0.0
        assert len(matched) == 0

    def test_insufficient_quantity(self):
        """Test when ingredient is available but quantity insufficient"""
        recipe_ingredients = [
            RecipeIngredient("flour", 2.0, "cups")
        ]
        recipe = Recipe("Test", 4, recipe_ingredients, ["Cook"])

        available = [
            Ingredient("flour", 1.0, "cups")  # Not enough
        ]

        score, missing, matched = recipe.calculate_match_score(available)

        assert score == 0.0  # Insufficient counts as missing
        assert len(missing) > 0

    def test_optional_ingredients_ignored(self):
        """Test that optional ingredients don't affect match score"""
        recipe_ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("salt", 1.0, "tsp", optional=True)
        ]
        recipe = Recipe("Test", 4, recipe_ingredients, ["Cook"])

        available = [
            Ingredient("flour", 3.0, "cups")
            # salt missing but it's optional
        ]

        score, missing, matched = recipe.calculate_match_score(available)

        assert score == 1.0  # Still 100% because salt is optional


class TestRecipeSerialization:
    """Test recipe serialization to/from dict"""

    def test_recipe_to_dict(self):
        """Test converting recipe to dictionary"""
        ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("milk", 1.0, "cup")
        ]
        instructions = ["Mix", "Cook"]

        recipe = Recipe(
            "Pancakes",
            4,
            ingredients,
            instructions,
            prep_time=10,
            cook_time=15,
            difficulty="easy"
        )

        data = recipe.to_dict()

        assert data['name'] == "Pancakes"
        assert data['servings'] == 4
        assert len(data['ingredients']) == 2
        assert data['prep_time'] == 10
        assert data['cook_time'] == 15
        assert 'created_at' in data

    def test_recipe_from_dict(self):
        """Test creating recipe from dictionary"""
        data = {
            'name': 'Pancakes',
            'servings': 4,
            'ingredients': [
                {'name': 'flour', 'quantity': 2.0, 'unit': 'cups', 'optional': False}
            ],
            'instructions': ['Mix', 'Cook'],
            'prep_time': 10,
            'cook_time': 15,
            'difficulty': 'easy',
            'cuisine': 'american',
            'dietary_tags': ['vegetarian']
        }

        recipe = Recipe.from_dict(data)

        assert recipe.name == "Pancakes"
        assert recipe.servings == 4
        assert len(recipe.ingredients) == 1

    def test_serialization_roundtrip(self):
        """Test that serialization roundtrip preserves data"""
        ingredients = [RecipeIngredient("flour", 2.0, "cups")]
        instructions = ["Mix", "Cook"]

        original = Recipe("Test", 4, ingredients, instructions, prep_time=10)

        data = original.to_dict()
        recreated = Recipe.from_dict(data)

        assert recreated.name == original.name
        assert recreated.servings == original.servings
        assert recreated.prep_time == original.prep_time


class TestRecipeUtilityMethods:
    """Test recipe utility methods"""

    def test_get_shopping_list(self):
        """Test generating shopping list"""
        recipe_ingredients = [
            RecipeIngredient("flour", 2.0, "cups"),
            RecipeIngredient("milk", 1.0, "cup"),
            RecipeIngredient("eggs", 2.0, "pieces")
        ]
        recipe = Recipe("Pancakes", 4, recipe_ingredients, ["Cook"])

        available = [
            Ingredient("flour", 3.0, "cups")
            # milk and eggs missing
        ]

        shopping_list = recipe.get_shopping_list(available)

        assert len(shopping_list) == 2
        assert any("milk" in item for item in shopping_list)
        assert any("eggs" in item for item in shopping_list)

    def test_string_representation(self):
        """Test string representation"""
        ingredients = [RecipeIngredient("flour", 2.0, "cups")]
        instructions = ["Mix"]

        recipe = Recipe("Pancakes", 4, ingredients, instructions, prep_time=10, cook_time=15)

        recipe_str = str(recipe)
        assert "Pancakes" in recipe_str
        assert "4" in recipe_str  # servings
        assert "25" in recipe_str  # total time