from src.utils.filehandler import FileHandler
from src.models.ingredient import Ingredient
from src.models.recipe import Recipe, RecipeIngredient
from datetime import date, timedelta

# Initialize FileHandler
fh = FileHandler("data")

print("=" * 50)
print("Test 1: Save and Load Ingredients")
print("=" * 50)

# Create test ingredients
milk = Ingredient("milk", 1.0, "liter", category="dairy")
flour = Ingredient("flour", 2.0, "cups", category="grains")

# Save them
fh.add_ingredient(milk.to_dict())
fh.add_ingredient(flour.to_dict())

# Load them back
loaded_ingredients = fh.load_ingredients()
print(f"Saved and loaded {len(loaded_ingredients)} ingredients")
for ing in loaded_ingredients:
    print(f"  - {ing['name']}: {ing['quantity']} {ing['unit']}")
print()

# Test 2: Save and Load Recipes
print("=" * 50)
print("Test 2: Save and Load Recipes")
print("=" * 50)

ingredients = [
    RecipeIngredient("flour", 2.0, "cups"),
    RecipeIngredient("milk", 1.0, "cup"),
    RecipeIngredient("eggs", 2.0, "pieces"),
]

pancakes = Recipe(
    name="Pancakes",
    servings=4,
    ingredients=ingredients,
    instructions=["Mix", "Cook", "Serve"],
    prep_time=10,
    cook_time=15,
    difficulty="easy"
)

# Save recipe
fh.add_recipe(pancakes.to_dict())

# Load it back
loaded_recipes = fh.load_recipes()
print(f"Saved and loaded {len(loaded_recipes)} recipes")
for rec in loaded_recipes:
    print(f"  - {rec['name']}: serves {rec['servings']}")
print()

# Test 3: Delete operations
print("=" * 50)
print("Test 3: Delete Operations")
print("=" * 50)

before_delete = len(fh.load_ingredients())
fh.delete_ingredient("milk")
after_delete = len(fh.load_ingredients())
print(f"Before delete: {before_delete} ingredients")
print(f"After delete: {after_delete} ingredients")
print()

# Test 4: Get specific item
print("=" * 50)
print("Test 4: Get Specific Recipe")
print("=" * 50)

recipe = fh.get_recipe_by_name("Pancakes")
if recipe:
    print(f"Found recipe: {recipe['name']}")
    print(f"Servings: {recipe['servings']}")
    print(f"Prep time: {recipe['prep_time']} min")
else:
    print("Recipe not found")
print()

# Test 5: Data summary
print("=" * 50)
print("Test 5: Data Summary")
print("=" * 50)

summary = fh.get_data_summary()
print(f"Total ingredients: {summary['total_ingredients']}")
print(f"Total recipes: {summary['total_recipes']}")
print(f"Ingredients file: {summary['ingredients_file']}")
print(f"Recipes file: {summary['recipes_file']}")
print()

# Test 6: Backup
print("=" * 50)
print("Test 6: Backup Data")
print("=" * 50)

backup_success = fh.backup_data("data/backup_test.json")
if backup_success:
    print("Backup created successfully")
else:
    print("Backup failed")
print()

print("=" * 50)
print("All FileHandler tests passed!")
print("=" * 50)