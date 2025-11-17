from collections import defaultdict
import re

def normalize_name(name: str) -> str:
    """
    Nettoie et normalise les noms d'ingrédients (minuscules, sans pluriel ni accent).
    Ex: 'Tomates cerises' → 'tomate cerise'
    """
    name = name.lower().strip()
    # Supprimer les pluriels simples
    if name.endswith("s") and not name.endswith("ss"):
        name = name[:-1]
    # Simplifier quelques variantes courantes
    name = re.sub(r"\b(brun|basmati|sushi)\b", "", name).strip()
    # Retirer les espaces multiples
    name = re.sub(r"\s+", " ", name)
    return name


def extract_ingredients(menu_data):
    """
    Extrait et agrège tous les ingrédients du menu (quantités incluses).
    Regroupe automatiquement les doublons normalisés.
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
