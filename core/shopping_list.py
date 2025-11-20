# shopping_list.py
def normalize_name(name):
    """Force un nom à être une string en minuscules propre."""
    if not isinstance(name, str):
        return ""
    return name.lower().strip()


def compute_missing_items(menu_ingredients, fridge_items):
    """
    menu_ingredients : [
        {"name": "...", "quantity": 100, "unit": "g"},
        ...
    ]
    fridge_items : [
        {"name": "..."},
        "avocat",
        ...
    ]
    """

    present = []
    missing = []

    # 🔥 Normaliser les noms du frigo
    fridge_clean = []

    for item in fridge_items:
        if isinstance(item, dict) and "name" in item:
            fridge_clean.append(normalize_name(item["name"]))
        elif isinstance(item, str):
            fridge_clean.append(normalize_name(item))

    # 🔥 Comparaison simple : normaliser aussi les ingrédients du menu
    for ing in menu_ingredients:
        ing_name = normalize_name(ing["name"])

        if ing_name in fridge_clean:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing
