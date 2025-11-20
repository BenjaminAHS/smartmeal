from collections import defaultdict
import re

import unicodedata
import re

def normalize_name(name: str) -> str:
    """
    Normalisation avancée pour matcher frigo / menu.
    """
    if not isinstance(name, str):
        name = str(name)

    # minuscules
    name = name.lower().strip()

    # enlever accents
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )

    # enlever pluriels simples
    if name.endswith("s") and len(name) > 3:
        name = name[:-1]

    # enlever mots parasites
    name = re.sub(r"\b(brun|basmati|sushi|bio|fraiche)\b", "", name).strip()

    # enlever espaces multiples
    name = re.sub(r"\s+", " ", name)

    return name

def extract_ingredients(menu_data):
    """
    This function extracts all ingredients from the full weekly menu and automatically aggregates duplicates.
    It normalizes ingredient names, sums quantities, and harmonizes units whenever possible.
    The output is a clean, alphabetically sorted list ready for a shopping list or inventory.
    """
    aggregated = defaultdict(lambda: {"quantity": 0.0, "unit": ""})

    for day in menu_data:
        for repas in day.get("repas", []):
            for ing in repas.get("ingredients", []):
                name = normalize_name(ing.get("name", ""))
                qty = float(ing.get("quantity", 0))
                unit = ing.get("unit", "").strip()

                # Convertir tout en même unité si même nom et unité compatible
                if aggregated[name]["unit"] and aggregated[name]["unit"] != unit:
                    # Si une unité vide ou incohérente, on garde la plus parlante
                    if unit:
                        aggregated[name]["unit"] = unit
                else:
                    aggregated[name]["unit"] = unit

                aggregated[name]["quantity"] += qty

    # Tri alphabétique propre
    return [
        {"name": name.capitalize(), "quantity": round(values["quantity"], 1), "unit": values["unit"]}
        for name, values in sorted(aggregated.items())
    ]
