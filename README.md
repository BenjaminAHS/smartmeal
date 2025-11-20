SmartMeal - Intelligent Meal Planner
A Streamlit web application that streamlines your weekly nutrition by combining AI-powered meal planning, image-based fridge scanning, and automated shopping list generation.

Features
AI Meal Planning: Generates a complete weekly menu (meals, ingredients, steps) based on diet, budget, and time constraints using GPT-4o-mini.

Visual Fridge Scanner: Analyze photos of your fridge or pantry to automatically detect available ingredients using OpenAI Vision.

Smart Lunchbox Logic: Automatically manages leftovers by duplicating dinner portions for the next day's lunch.

Automated Shopping List: Calculates missing items by comparing the generated menu ingredients against your current inventory.

Dietary Customization: Supports various diets (Vegetarian, Vegan, Gluten-free) and excludes specific allergens.

Prerequisites
Python 3.x

OpenAI API key

Internet connection (for OpenAI API calls)

Installation
1. Install Dependencies
The app requires several Python packages. Install them using pip based on the imports used in the project:

Bash

pip install streamlit openai pillow python-dotenv
Note: Derived from imports found in source files.

2. Set Up OpenAI API Key
You need to set your OpenAI API key as an environment variable. The application uses python-dotenv to load this configuration.

Create a .env file in the project root:

OPENAI_API_KEY=your-api-key-here
The app will automatically load the API key from this file.

Usage
Launching the App
Navigate to the project directory:

Bash

cd smartmeal/
Run the Streamlit app:

Bash

streamlit run main.py
Access the web interface:

The app will open automatically in your default web browser (usually http://localhost:8501).

Using the App
Tab 1: 🧠 Meal Planner (Planificateur)
Define your constraints:

Style: Healthy, Gourmand, or Mixed.

Diet: Vegetarian, Vegan, etc.

Budget & Time: Set limits per meal.

Lunchboxes: Choose how many days you need leftovers for lunch.

Click "Générer mon menu".

The AI generates a structured JSON plan with recipes and instructions.

Tab 2: 📸 Fridge Scanner (Scanner)
Upload a photo of your fridge or pantry.

Click "Analyser le contenu".

The AI detects visible food items.

Verify the list using the multi-select tool or manually add missed items.

The app immediately compares your inventory with the menu to show what you already have.

Tab 3: 🛒 Shopping List (Liste de courses)
Ensure a menu is generated and inventory is checked.

View the consolidated list of missing ingredients.

Click "Télécharger la liste de courses" to download a .txt file of items to buy.

🛠️ Technical Details
Architecture
Frontend: Streamlit (Python-based web UI).

AI Model: OpenAI gpt-4o-mini used for both text generation (JSON menus) and vision tasks (ingredient detection).

Data Handling:

Menus are generated in strict JSON format.

Ingredients are normalized (lowercase, stripped) to ensure accurate matching between the menu and the fridge.

Key Components
menu_generator.py: Constructs a strict prompt for GPT-4o-mini to return a valid JSON object containing the weekly schedule, ingredients, and cooking steps.

fridge_scanner.py: Processes images via PIL and sends them to OpenAI's vision model to output a Python list of detected strings.

shopping_list.py: Contains the logic to normalize ingredient names and compute the difference between menu_ingredients and fridge_items.

main.py: Handles the UI, session state, lunchbox logic (doubling dinner quantities for next-day lunch), and orchestrates the data flow between modules.

Troubleshooting
Common Issues
"API Key not found"

Ensure your .env file is in the correct directory and strictly named .env.

Check the console output for "🔑 API KEY détectée".

JSON Parsing Errors

The menu generator relies on the LLM outputting strict JSON. Occasionally, the model might add text. The clean_json_like function in main.py attempts to fix this, but regenerating the menu usually solves the issue.

Ingredient Matching Issues

If the scanner sees "Tomatoes" but the menu asks for "Tomato", the app tries to normalize names using normalize_name, but minor discrepancies may still occur.

Notes
Lunchbox Logic: If you select lunchboxes, the app automatically doubles the quantities for the previous night's dinner and assigns the leftovers to the next day's lunch.

Session State: Data (menus, scanned items) is stored in Streamlit's session state and will be lost if you refresh the browser page.

Future Enhancements
User Accounts: Save preferences and menus persistently.

Barcode Scanning: Add support for scanning product barcodes.

Recipe Export: Export recipes to PDF.
