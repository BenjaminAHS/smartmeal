def compute_missing_items(menu_ingredients, fridge_items):
    """
    This function compares the ingredients required by the weekly menu with the food items detected in the user’s fridge.
    It identifies which ingredients are already available and which ones still need to be purchased based on name matching.
    The output consists of two lists: present items with their quantities, and missing items to buy.
    """
    fridge_set = {f.lower().strip() for f in fridge_items}
    present, missing = [], []

    for ing in menu_ingredients:
        name = ing["name"]
        qty = ing["quantity"]
        unit = ing["unit"]

        # Si un aliment du frigo correspond au nom de l'ingrédient
        if any(f in name for f in fridge_set):
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing
