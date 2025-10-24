import sys
from datetime import datetime, date, timedelta
from src.models.ingredient import Ingredient
from src.models.recipe import Recipe, RecipeIngredient
from src.services.ingredient_service import IngredientService
from src.services.recipe_service import RecipeService
from src.services.shopping_service import ShoppingService



class RecipeOptimizerCLI:
    """Simple command-line interface for Recipe Optimizer"""

    def __init__(self):
        self.ingredient_service = IngredientService()
        self.recipe_service = RecipeService()
        self.shopping_service = ShoppingService()
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
        print("4. 🛒 Generate Shopping List")
        print("5. ⚠️  Check Expiring Ingredients")
        print("6. 📊 View Statistics")
        print("7. 🚪 Exit")

    def handle_menu_choice(self, choice: str):
        """Handle main menu selection"""
        if choice == '1':
            self.ingredient_menu()
        elif choice == '2':
            self.recipe_menu()
        elif choice == '3':
            self.find_recipes()
        elif choice == '4':
            self.generate_shopping_list()
        elif choice == '5':
            self.check_expiring_ingredients()
        elif choice == '6':
            self.view_statistics()
        elif choice == '7':
            self.running = False
        else:
            print("❌ Invalid choice. Please enter 1-7.")

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

            # Ask for expiration date
            expiration_str = input("Expiration date (YYYY-MM-DD, or press Enter to skip): ").strip()
            expiration_date = None
            if expiration_str:
                try:
                    expiration_date = datetime.strptime(expiration_str, "%Y-%m-%d").date()
                except ValueError:
                    print("⚠️  Invalid date format, skipping expiration date")

            category = input("Category (vegetables, fruits, dairy, grains, spices, other): ").strip()
            if not category:
                category = "other"

            ingredient = Ingredient(
                name=name,
                quantity=quantity,
                unit=unit,
                expiration_date=expiration_date,
                category=category.lower()
            )

            success = self.ingredient_service.add_ingredient(ingredient)
            if success:
                print(f"✅ Added: {ingredient}")
            else:
                print("⚠️  Could not add ingredient.")

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
        """Find recipes matching available ingredients with unit conversion"""
        print("\n🔍 FIND MATCHING RECIPES")
        print("-" * 30)

        ingredients = self.ingredient_service.get_all_ingredients()
        recipes = self.recipe_service.get_all_recipes()

        if not ingredients:
            print("❌ No ingredients available. Add ingredients first!")
            return

        if not recipes:
            print("❌ No recipes available. Add recipes first!")
            return

        # Get search parameters
        min_match_str = input("Minimum match percentage (default 70): ").strip()
        min_match = 0.7
        if min_match_str:
            try:
                min_match = float(min_match_str) / 100
                min_match = max(0.0, min(1.0, min_match))
            except ValueError:
                print("⚠️ Invalid percentage, using default 70%")

        # Use the new matching service
        from src.services.matching_service import RecipeMatchingService
        matcher = RecipeMatchingService()

        all_matches = matcher.find_matching_recipes(
            ingredients, recipes, min_match, allow_substitutions=True
        )

        if not all_matches:
            print(f"\n❌ No recipes found with {min_match * 100:.0f}% match or better.")
            return

        print(f"\n🍳 MATCHING RECIPES ({len(all_matches)} found)")
        print("=" * 60)
        for i, (recipe, score, missing, matched) in enumerate(all_matches, 1):
            print(f"\n{i}. {recipe.name}")
            print(f"   Match: {score * 100:.0f}% | Time: {recipe.total_time} min | Difficulty: {recipe.difficulty}")

            if matched:
                print(f"   ✅ Available: {', '.join(matched[:3])}")
                if len(matched) > 3:
                    print(f"       ... and {len(matched) - 3} more")

            if missing and score < 1.0:
                print(f"   ❌ Missing: {', '.join(missing[:2])}")
                if len(missing) > 2:
                    print(f"       ... and {len(missing) - 2} more")

        input("\nPress Enter to continue...")
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

    def generate_shopping_list(self):
        """Generate shopping list for selected recipes"""
        print("\n🛒 GENERATE SHOPPING LIST")
        print("-" * 50)

        recipes = self.recipe_service.get_all_recipes()
        ingredients = self.ingredient_service.get_all_ingredients()

        if not recipes:
            print("❌ No recipes available. Add recipes first!")
            return

        # Show available recipes
        print("\nAvailable recipes:")
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe.name} (serves {recipe.servings})")

        # Select recipes
        try:
            selections = input(f"\nSelect recipes (comma-separated, 1-{len(recipes)}): ").strip()
            if not selections:
                print("❌ No recipes selected.")
                return

            selected_indices = [int(x.strip()) - 1 for x in selections.split(',')]
            selected_recipes = []

            for index in selected_indices:
                if 0 <= index < len(recipes):
                    selected_recipes.append(recipes[index])

            if not selected_recipes:
                print("❌ No valid recipes selected.")
                return

            # Generate shopping list
            shopping_list = self.shopping_service.generate_shopping_list(
                selected_recipes,
                ingredients
            )

            if not shopping_list:
                print("\n✅ You have all ingredients needed!")
                return

            # Display shopping list
            formatted = self.shopping_service.format_shopping_list(shopping_list)
            print(f"\n{formatted}")

            # Show statistics
            stats = self.shopping_service.calculate_estimated_items_count(shopping_list)
            print(f"\n📊 Total items to buy: {stats['total_items']}")

            # Offer to save
            save_choice = input("\n💾 Save shopping list to file? (y/n): ").strip().lower()
            if save_choice == 'y':
                filename = f"shopping_list_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                if self.shopping_service.export_shopping_list(shopping_list, filename):
                    print(f"✅ Shopping list saved to {filename}")
                else:
                    print("❌ Failed to save shopping list")

        except ValueError:
            print("❌ Invalid input. Please enter numbers separated by commas.")
        except Exception as e:
            print(f"❌ Error generating shopping list: {e}")

        input("\nPress Enter to continue...")

    def check_expiring_ingredients(self):
        """Check for ingredients expiring soon"""
        print("\n⚠️  EXPIRING INGREDIENTS")
        print("-" * 50)

        # Get expiring and expired ingredients
        expiring_soon = self.ingredient_service.get_expiring_soon(days=7)
        expired = self.ingredient_service.get_expired_ingredients()

        if not expiring_soon and not expired:
            print("✅ No ingredients expiring in the next 7 days!")
            input("\nPress Enter to continue...")
            return

        # Show expired ingredients first
        if expired:
            print("\n❌ EXPIRED INGREDIENTS:")
            for ing in expired:
                days_ago = abs(ing.days_until_expiry())
                print(f"  • {ing.name} - Expired {days_ago} days ago")
            print("\n⚠️  Consider removing expired ingredients!")

        # Show expiring soon
        if expiring_soon:
            print("\n⏰ EXPIRING SOON (next 7 days):")
            for ing in expiring_soon:
                days_left = ing.days_until_expiry()
                if days_left == 0:
                    print(f"  • {ing.name} - EXPIRES TODAY!")
                elif days_left == 1:
                    print(f"  • {ing.name} - Expires tomorrow")
                else:
                    print(f"  • {ing.name} - Expires in {days_left} days")

        # Suggest recipes using expiring ingredients
        print("\n💡 SUGGESTED RECIPES (using expiring ingredients):")

        all_recipes = self.recipe_service.get_all_recipes()
        all_ingredients = self.ingredient_service.get_all_ingredients()

        if all_recipes:
            from src.services.matching_service import RecipeMatchingService
            matcher = RecipeMatchingService()

            # Find recipes we can make
            matches = matcher.find_matching_recipes(
                all_ingredients,
                all_recipes,
                min_match_score=0.7
            )

            # Filter to recipes that use expiring ingredients
            expiring_names = {ing.name for ing in expiring_soon}
            suggested = []

            for recipe, score, missing, matched in matches:
                recipe_ing_names = {ing.name for ing in recipe.ingredients}
                if recipe_ing_names & expiring_names:  # Has overlap
                    suggested.append((recipe, score))

            if suggested:
                for recipe, score in suggested[:3]:  # Show top 3
                    print(f"  • {recipe.name} ({score * 100:.0f}% match, {recipe.total_time} min)")
            else:
                print("  No recipes found using expiring ingredients")
        else:
            print("  No recipes available")

        input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    cli = RecipeOptimizerCLI()
    cli.run()


if __name__ == "__main__":
    main()