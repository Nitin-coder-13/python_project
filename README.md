# 🍳 Recipe Optimizer

A Python-based recipe management system that helps you optimize your cooking with intelligent ingredient tracking, recipe matching, and smart shopping list generation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [What I Learned](#what-i-learned)
- [Future Enhancements](#future-enhancements)

## ✨ Features

### 🥬 Ingredient Management
- Add, view, and delete ingredients with quantities and units
- Track expiration dates
- Categorize ingredients (dairy, vegetables, grains, etc.)
- Get alerts for expiring ingredients

### 📖 Recipe Management
- Create and store custom recipes
- Include prep time, cook time, and difficulty levels
- Add detailed instructions and ingredient lists
- Scale recipes for different serving sizes

### 🔍 Intelligent Recipe Matching
- Find recipes based on available ingredients
- **Automatic unit conversion** (cups ↔ ml, pounds ↔ grams)
- Match scoring system (shows % of ingredients you have)
- Ingredient substitution suggestions (e.g., milk → almond milk)

### 🛒 Smart Shopping List
- Generate shopping lists for multiple recipes
- Automatically calculates missing ingredients
- Groups items by category for easier shopping
- Accounts for quantities you already have
- Export shopping lists to text files

### ⚠️ Expiration Management
- Track ingredient expiration dates
- Get warnings for items expiring soon
- Receive recipe suggestions using expiring ingredients
- Reduce food waste intelligently

### 📊 Statistics Dashboard
- View total ingredients and recipes
- Track average cooking times
- Analyze your inventory

## 🎬 Demo

### Main Menu
```
📋 MAIN MENU
==================================================
1. 🥬 Manage Ingredients
2. 📖 Manage Recipes
3. 🔍 Find Matching Recipes
4. 🛒 Generate Shopping List
5. ⚠️  Check Expiring Ingredients
6. 📊 View Statistics
7. 🚪 Exit
```

### Example: Find Matching Recipes
```
🍳 MATCHING RECIPES (2 found)
============================================================

1. Pancakes
   Match: 100% | Time: 25 min | Difficulty: easy
   ✅ Available: flour, milk, eggs
   
2. Chocolate Cake
   Match: 75% | Time: 60 min | Difficulty: medium
   ✅ Available: flour, eggs, sugar
   ❌ Missing: 200g chocolate, 100ml oil
```

## 🛠️ Technologies Used

- **Python 3.8+** - Core programming language
- **JSON** - Data persistence
- **pytest** - Unit testing framework
- **Git/GitHub** - Version control

### Python Libraries
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `python-dateutil` - Date handling

### Design Patterns
- **MVC Architecture** - Separation of concerns
- **Service Layer Pattern** - Business logic isolation
- **Repository Pattern** - Data access abstraction

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/Nitin-coder-13/python_project.git
cd python_project
```

2. **Create virtual environment**
```bash
python -m venv recipe_env

# Activate (Windows)
recipe_env\Scripts\activate

# Activate (Mac/Linux)
source recipe_env/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python -m src.interfaces.cli
```

## 🚀 Usage

### Adding Ingredients
```
Choose option 1 → Manage Ingredients → Add Ingredient
Enter: Name, Quantity, Unit, Expiration Date (optional), Category
Example: milk, 500, ml, 2024-12-31, dairy
```

### Creating a Recipe
```
Choose option 2 → Manage Recipes → Add Recipe
Follow prompts to add:
- Recipe name, servings, prep/cook time
- Ingredients with quantities
- Step-by-step instructions
```

### Finding Matching Recipes
```
Choose option 3 → Find Matching Recipes
- Set minimum match percentage (e.g., 70%)
- View recipes you can make with available ingredients
- See what's missing for recipes you can't fully make
```

### Generating Shopping List
```
Choose option 4 → Generate Shopping List
- Select multiple recipes you want to cook
- Get organized shopping list grouped by category
- Option to export to text file
```

### Checking Expiring Ingredients
```
Choose option 5 → Check Expiring Ingredients
- View ingredients expiring in next 7 days
- See expired ingredients
- Get recipe suggestions using expiring items
```

### View Statistics
```
Choose option 6 → View Statistics
- Total ingredients count
- Total recipes count
- Average cooking time
```
### Exit
```
For exit, press option 7.
```

## 📁 Project Structure

```
python_project/
├── src/
│   ├── models/              # Data models (Ingredient, Recipe)
│   ├── services/            # Business logic layer
│   │   ├── ingredient_service.py
│   │   ├── recipe_service.py
│   │   ├── matching_service.py
│   │   └── shopping_service.py
│   ├── utils/               # Utility functions
│   │   ├── filehandler.py
│   │   └── unit_converter.py
│   └── interfaces/          # User interfaces
│       └── cli.py
├── tests/                   # Unit tests
│   ├── test_ingredient.py
│   └── test_recipe.py
├── data/                    # JSON data storage
├── requirements.txt
└── README.md
```

## 🎓 What I Learned

### Technical Skills
- **Object-Oriented Programming**: Implemented classes, inheritance, and encapsulation
- **Data Structures**: Used dictionaries, lists, and sets for efficient data management
- **Algorithm Design**: Created matching algorithms and unit conversion systems
- **File I/O**: Implemented JSON-based data persistence
- **Testing**: Wrote comprehensive unit tests with pytest
- **Git Workflow**: Used feature branches, pull requests, and proper commit messages

### Software Engineering Practices
- MVC architecture for clean code separation
- Service layer pattern for business logic
- Comprehensive error handling
- Code documentation and type hints
- Test-driven development mindset

### Problem-Solving
- Unit conversion between different measurement systems
- Intelligent recipe matching with partial ingredients
- Shopping list consolidation and optimization
- Expiration tracking and waste reduction

## 🔮 Future Enhancements

- [ ] Web-based UI with Flask/FastAPI
- [ ] Nutrition API integration for calorie tracking
- [ ] Meal planning calendar
- [ ] Barcode scanning for ingredient entry
- [ ] Recipe import from popular cooking websites
- [ ] Multi-user support with authentication
- [ ] Mobile app version
- [ ] Cloud deployment (AWS/Heroku)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📝 License

This project is [MIT](LICENSE) licensed.

## 👤 Author

**Your Name**
- GitHub: [Nitin-coder-13](https://github.com/Nitin-coder-13/python_project)
- LinkedIn: [Nitin pandey](https://www.linkedin.com/in/nitin-pandey-0aa5b5324?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

## 🙏 Acknowledgments

- Thanks to the Python community for excellent documentation
- Inspired by the need to reduce food waste and optimize grocery shopping

---

⭐ If you found this project helpful, please give it a star!