import sys
from datetime import datetime, date
from src.models.ingredient import Ingredient
from src.models.recipe import Recipe, RecipeIngredient
from src.services.ingredient_service import IngredientService
from src.services.recipe_service import RecipeService


class RecipeOptimizerCLI:
    """Simple command-line interface for Recipe Optimizer"""

    def __init__(self):
        self.ingredient_service = IngredientService()
        self.recipe_service = RecipeService()
        self.running = True

    def run(self):
        """Start the CLI application"""
        print("\n" + "=" * 50)
        print("🍳 Welcome to Recipe Optimizer!")
        print("=" * 50)

        while self.running:
            self.show_main_menu()
            choice = input("\nEnter your choice (1-5): ").strip()
            self.handle_menu_choice(choice)

        print("\n👋 Thank you for using Recipe Optimizer!")
        print("Happy cooking! 🍳\n")

    def show_main_menu(self):
        """Display main menu"""
        print("\n" + "=" * 50)
        print("📋 MAIN MENU")
        print("=" * 50)
        print("1. 🥬 Manage Ingredients")
        print("2. 📖 Manage Recipes")
        print("3. 🔍 Find Matching Recipes")
        print("4. 📊 View Statistics")
        print("5. 🚪 Exit")

    def handle_menu_choice(self, choice: str):
        """Handle main menu selection"""
        if choice == '1':
            self.ingredient_menu()
        elif choice == '2':
            self.recipe_menu()
        elif choice == '3':
            self.find_recipes()
        elif choice == '4':
            self.view_statistics()
        elif choice == '5':
            self.running = False
        else:
            print("❌ Invalid choice. Please enter 1-5.")

    def ingredient_menu(self):
        """Ingredient management submenu"""
        while True:
            print("\n" + "=" * 50)
            print("🥬 INGREDIENT MANAGEMENT")
            print("=" * 50)
            print("1. View All Ingredients")
            print("2. Add Ingredient")
            print("3. Delete Ingredient")
            print("4. Back to Main Menu")

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == '1':
                self.view_ingredients()
            elif choice == '2':
                self.add_ingredient()
            elif choice == '3':
                self.delete_ingredient()
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice.")

    def view_ingredients(self):
        """Display all ingredients"""
        ingredients = self.ingredient_service.get_all_ingredients()

        if not ingredients:
            print("\n📭 No ingredients found.")
            return

        print(f"\n🥬 YOUR INGREDIENTS ({len(ingredients)} total)")
        print("-" * 50)
        for ingredient in sorted(ingredients, key=lambda x: x.name):
            print(f"  • {ingredient}")

    def add_ingredient(self):
        """Add new ingredient"""
        print("\n➕ ADD NEW INGREDIENT")
        print("-" * 30)

        try:
            name = input("Ingredient name: ").strip()
            if not name:
                print("❌ Name cannot be empty.")
                return

            quantity_str = input("Quantity: ").strip()
            quantity = float(quantity_str)
            if quantity <= 0:
                print("❌ Quantity must be positive.")
                return

            unit = input("Unit (cups, grams, pieces, etc.): ").strip()
            if not unit:
                print("❌ Unit cannot be empty.")
                return

            category = input("Category (vegetables, fruits, dairy, grains, spices, other): ").strip()
            if not category:
                category = "other"

            ingredient = Ingredient(
                name=name,
                quantity=quantity,
                unit=unit,
                category=category.lower()
            )

            success = self.ingredient_service.add_ingredient(ingredient)
            if success:
                print(f"✅ Added: {ingredient}")
            else:
                print("⚠️ Could not add ingredient.")

        except ValueError:
            print("❌ Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def delete_ingredient(self):
        """Delete an ingredient"""
        print("\n🗑️ DELETE INGREDIENT")
        print("-" * 30)

        name = input("Ingredient name to delete: ").strip()
        if not name:
            print("❌ Name cannot be empty.")
            return

        success = self.ingredient_service.delete_ingredient(name)
        if success:
            print(f"✅ Deleted: {name}")
        else:
            print(f"❌ Ingredient '{name}' not found.")

    def recipe_menu(self):
        """Recipe management submenu"""
        while True:
            print("\n" + "=" * 50)
            print("📖 RECIPE MANAGEMENT")
            print("=" * 50)
            print("1. View All Recipes")
            print("2. Add Recipe")
            print("3. Delete Recipe")
            print("4. Back to Main Menu")

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == '1':
                self.view_recipes()
            elif choice == '2':
                self.add_recipe()
            elif choice == '3':
                self.delete_recipe()
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice.")

    def view_recipes(self):
        """Display all recipes"""
        recipes = self.recipe_service.get_all_recipes()

        if not recipes:
            print("\n📭 No recipes found.")
            return

        print(f"\n📖 YOUR RECIPES ({len(recipes)} total)")
        print("-" * 50)
        for recipe in sorted(recipes, key=lambda x: x.name):
            print(f"  • {recipe}")

    def add_recipe(self):
        """Add new recipe"""
        print("\n➕ ADD NEW RECIPE")
        print("-" * 30)

        try:
            name = input("Recipe name: ").strip()
            if not name:
                print("❌ Name cannot be empty.")
                return

            servings_str = input("Number of servings: ").strip()
            servings = int(servings_str)
            if servings <= 0:
                print("❌ Servings must be positive.")
                return

            prep_str = input("Prep time (minutes): ").strip()
            prep_time = int(prep_str) if prep_str else 0

            cook_str = input("Cook time (minutes): ").strip()
            cook_time = int(cook_str) if cook_str else 0

            difficulty = input("Difficulty (easy/medium/hard): ").strip().lower()
            if difficulty not in ['easy', 'medium', 'hard']:
                difficulty = 'medium'

            print("Add ingredients (type 'done' when finished)")
            ingredients = []
            while True:
                ing_name = input("  Ingredient name (or 'done'): ").strip()
                if ing_name.lower() == 'done':
                    break

                try:
                    quantity_str = input("  Quantity: ").strip()
                    quantity = float(quantity_str)
                    unit = input("  Unit: ").strip()

                    ingredients.append(RecipeIngredient(ing_name, quantity, unit))
                    print(f"  ✅ Added: {quantity} {unit} {ing_name}")
                except ValueError:
                    print("  ❌ Invalid quantity.")

            if not ingredients:
                print("❌ Recipe must have at least one ingredient.")
                return

            print("Add instructions (type 'done' when finished)")
            instructions = []
            step = 1
            while True:
                instruction = input(f"  Step {step}: ").strip()
                if instruction.lower() == 'done':
                    break
                instructions.append(instruction)
                step += 1

            if not instructions:
                print("❌ Recipe must have at least one instruction.")
                return

            recipe = Recipe(
                name=name,
                servings=servings,
                ingredients=ingredients,
                instructions=instructions,
                prep_time=prep_time,
                cook_time=cook_time,
                difficulty=difficulty
            )

            success = self.recipe_service.add_recipe(recipe)
            if success:
                print(f"✅ Added recipe: {recipe}")
            else:
                print("⚠️ Could not add recipe.")

        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def delete_recipe(self):
        """Delete a recipe"""
        print("\n🗑️ DELETE RECIPE")
        print("-" * 30)

        name = input("Recipe name to delete: ").strip()
        if not name:
            print("❌ Name cannot be empty.")
            return

        success = self.recipe_service.delete_recipe(name)
        if success:
            print(f"✅ Deleted: {name}")
        else:
            print(f"❌ Recipe '{name}' not found.")

    def find_recipes(self):
        """Find recipes that match available ingredients"""
        print("\n🔍 FIND MATCHING RECIPES")
        print("-" * 30)

        available_ingredients = self.ingredient_service.get_all_ingredients()
        all_recipes = self.recipe_service.get_all_recipes()

        if not available_ingredients:
            print("❌ No ingredients available. Add ingredients first!")
            return

        if not all_recipes:
            print("❌ No recipes available. Add recipes first!")
            return

        matching_recipes = []
        for recipe in all_recipes:
            score, missing, matched = recipe.calculate_match_score(available_ingredients)
            if score > 0:
                matching_recipes.append((recipe, score, missing, matched))

        if not matching_recipes:
            print("❌ No recipes can be made with available ingredients.")
            return

        # Sort by match score
        matching_recipes.sort(key=lambda x: -x[1])

        print(f"\n🍳 MATCHING RECIPES ({len(matching_recipes)} found)")
        print("-" * 50)
        for i, (recipe, score, missing, matched) in enumerate(matching_recipes, 1):
            print(f"\n{i}. {recipe.name}")
            print(f"   Match: {score * 100:.0f}% | Time: {recipe.total_time} min")
            print(f"   Available: {', '.join(matched[:3])}" if matched else "   Available: None")
            if missing:
                print(f"   Missing: {', '.join(missing[:2])}")

    def view_statistics(self):
        """Display statistics"""
        ingredients = self.ingredient_service.get_all_ingredients()
        recipes = self.recipe_service.get_all_recipes()

        print("\n📊 STATISTICS")
        print("=" * 50)
        print(f"Total ingredients: {len(ingredients)}")
        print(f"Total recipes: {len(recipes)}")

        if recipes:
            avg_time = sum(r.total_time for r in recipes) / len(recipes)
            print(f"Average recipe time: {avg_time:.1f} minutes")

        print("=" * 50)


def main():
    """Main entry point"""
    cli = RecipeOptimizerCLI()
    cli.run()


if __name__ == "__main__":
    main()