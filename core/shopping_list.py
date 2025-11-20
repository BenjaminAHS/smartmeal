from core.ingredient_extractor import normalize_name

def compute_missing_items(menu_ingredients, fridge_items):
    present = []
    missing = []

    # Normaliser le frigo
    fridge_clean = [normalize_name(item["name"] if isinstance(item, dict) else item)
                    for item in fridge_items]

    for ing in menu_ingredients:
        ing_name = normalize_name(ing["name"])

        if ing_name in fridge_clean:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing