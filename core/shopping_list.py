import unicodedata
import re

def normalize_name(candidate):
    """
    Nettoie le nom pour gérer les pluriels, accents et formats différents.
    Ex: "Des carottes" -> "carotte", "Bœuf" -> "boeuf".
    """
    # 1. Extraction du texte si c'est un dictionnaire
    if isinstance(candidate, dict):
        candidate = candidate.get("name", "")

    # 2. Sécurité si vide ou autre type
    if not isinstance(candidate, str):
        return ""

    # 3. Minuscules et nettoyage de base
    name = candidate.lower().strip()

    # 4. Suppression des accents (ex: Pâtes -> pates)
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )

    # 5. Suppression du pluriel simple 's' final (si mot > 3 lettres)
    # Ex: "oeufs" -> "oeuf", "carottes" -> "carotte"
    if name.endswith("s") and len(name) > 3:
        name = name[:-1]

    # 6. Suppression des mots parasites courants
    name = re.sub(r"\b(cuit|cuite|frais|fraiche|bio|rouge|blanc)\b", "", name).strip()
    
    # 7. Suppression des espaces multiples
    name = re.sub(r"\s+", " ", name).strip()

    return name


def compute_missing_items(menu_ingredients, fridge_items):
    """
    Compare le menu et le frigo en utilisant la normalisation avancée.
    """
    present = []
    missing = []

    # --- 1. Préparer le contenu du frigo (Set de noms normalisés) ---
    fridge_normalized = set()
    
    if not fridge_items:
        fridge_items = []

    for item in fridge_items:
        clean = normalize_name(item)
        if clean:
            fridge_normalized.add(clean)

    # --- 2. Comparer avec le menu ---
    if not menu_ingredients:
        menu_ingredients = []

    for ing in menu_ingredients:
        # On normalise le nom demandé par le menu
        ing_name_clean = normalize_name(ing)

        # Si le nom normalisé est dans le frigo normalisé -> C'est bon !
        if ing_name_clean in fridge_normalized:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing