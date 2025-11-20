def compute_missing_items(menu_ingredients, fridge_items):
    """
    This function compares the ingredients required by the weekly menu with the food items detected in the user’s fridge.
    It identifies which ingredients are already available and which ones still need to be purchased based on name matching.
    The output consists of two lists: present items with their quantities, and missing items to buy.
    """
    present = []
    missing = []

    # transformer en set pour accélérer les comparaisons
    fridge_names = {item["name"].lower().strip() for item in fridge_items}

    for ing in menu_ingredients:
        ing_name = ing["name"].lower().strip()

        if ing_name in fridge_names:
            # déjà dans le frigo
            present.append(ing)
        else:
            # à acheter
            missing.append(ing)

    return present, missing

