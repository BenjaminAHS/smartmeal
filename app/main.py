import re
import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from dotenv import load_dotenv
import os
import json
load_dotenv(dotenv_path="C:\\Users\\hp\\Documents\\Albert School\\M1\\Gen AI\\smartmeal\\.env")

# Imports internes
from core.menu_generator import generate_meal_plan
from core.fridge_scanner import detect_food_items
from core.ingredient_extractor import extract_ingredients
from core.shopping_list import compute_missing_items

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()
print("🔑 API KEY détectée :", os.getenv("OPENAI_API_KEY"))

def clean_json_like(text: str):
    """
    Nettoie les sorties du modèle en retirant le bruit AVANT le vrai JSON.
    Conserve tout à partir du premier '{'.
    """

    # Supprimer index type 0:, 1:
    text = re.sub(r'\b\d+\s*:', '', text)

    # Supprimer balises markdown
    text = text.replace("```json", "").replace("```", "").strip()

    # ⚠️ IMPORTANT : trouver le vrai début du JSON
    if "{" in text:
        text = text[text.index("{"):]

    return text.strip()

def apply_lunchbox_rules(menu, lunchbox_days):
    """
    Pour chaque jour dans lunchbox_days :
    - Le repas du soir = master lunchbox (quantités doublées)
    - Le lendemain midi = copie EXACTE du repas du soir (quantités normales)
    - Tous les autres repas restent inchangés
    """

    days_order = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    index_map = {day: i for i, day in enumerate(days_order)}

    from copy import deepcopy

    for day in lunchbox_days:
        if day not in index_map:
            continue

        i = index_map[day]
        if i >= len(menu):
            continue

        current_day = menu[i]

        # Trouver le repas du soir du jour J
        dinner = next((r for r in current_day["repas"] if r["moment"] == "soir"), None)
        if dinner is None:
            continue

        # Marquer comme lunchbox
        dinner["lunchbox"] = True

        # Doubler les quantités du soir
        for ing in dinner["ingredients"]:
            ing["quantity"] = ing["quantity"] * 2

        # Déterminer le lendemain (modulo 7)
        next_i = (i + 1) % len(menu)
        next_day = menu[next_i]

        # Créer la copie du dîner → midi du lendemain
        lunch_copy = deepcopy(dinner)

        # Remettre quantités normales pour la lunchbox du lendemain
        for ing in lunch_copy["ingredients"]:
            ing["quantity"] = ing["quantity"] / 2  

        lunch_copy["moment"] = "midi"
        lunch_copy["lunchbox"] = True

        # REMPLACER le midi du lendemain par la copie
        found = False
        for j, repas in enumerate(next_day["repas"]):
            if repas["moment"].lower() == "midi":
                next_day["repas"][j] = lunch_copy
                found = True
                break

        # Si pas de midi, on l'ajoute
        if not found:
            next_day["repas"].insert(0, lunch_copy)

    return menu
# -----------------------------
# 🎯 Configuration de la page
# -----------------------------
st.set_page_config(
    page_title="SmartMeal - Planificateur de repas intelligent",
    page_icon="🥗",
    layout="wide"
)
# Style pour centrer le titre
st.markdown("""
    <style>
    .center-title {
        text-align: center !important;
        font-size: 42px !important;
        font-weight: 900 !important;
        margin-top: -20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='center-title'>🥗 SmartMeal</h1>", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Centrer uniquement la barre des onglets */
    div[data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: center !important;
        margin-top: 10px !important;
        margin-bottom: 20px !important;
    }

    /* Style des onglets */
    div[data-baseweb="tab"] {
        font-size: 18px !important;
        padding: 10px 20px !important;
        margin: 0 8px !important;
        border-radius: 10px !important;
        background-color: #f7f7f7 !important;
        color: #444 !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="tab"]:hover {
        background-color: #e6e6e6 !important;
    }

    div[data-baseweb="tab"][aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: 700 !important;
    }

    /* IMPORTANT : empêcher le style des tabs d'affecter le contenu */
    section.main > div {
        padding-top: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)



# -----------------------------
# 🏷️ En-tête
# -----------------------------
st.subheader("Ton assistant repas intelligent 🍴")

st.write("""
Bienvenue sur **SmartMeal**, l'application qui t'aide à :
- planifier tes repas de la semaine 🍽️  
- générer automatiquement ta liste de courses 🛒  
- et scanner ton frigo/placard pour savoir ce qu'il te manque 📸  
""")

# -----------------------------
# 🧩 Onglets principaux
# -----------------------------
tab1, tab2, tab3 = st.tabs(["🧠 Planificateur de repas", "📸 Scanner frigo/placard", "🛒 Liste de courses"])


# === Onglet 1 : Planificateur ===
with tab1:
    st.header("📅 Génère ton menu hebdomadaire")

    st.markdown("### ⚙️ Paramètres du menu")
    
    with st.container():
        colA, colB = st.columns(2)

        with colA:
            type_menu = st.selectbox(
                "🍽️ Style de menu",
                ["Healthy 🥗", "Gourmand 🍕", "Mixte 🍴"]
            )

            regime = st.selectbox(
                "🥦 Régime alimentaire",
                ["Aucun", "Végétarien", "Végan", "Sans gluten", "Pescetarien"]
            )

            personnes = st.number_input(
                "👥 Nombre de personnes",
                min_value=1, max_value=8, value=1
            )

        with colB:
            aliments_eviter = st.text_area(
                "🚫 Aliments à éviter",
                placeholder="poisson, brocoli, tofu, champignons..."
            )

            budget = st.slider(
                "💰 Budget max par repas (€)",
                3, 15, value=5
            )

            temps = st.slider(
                "⏱️ Temps max de préparation (minutes)",
                10, 60, value=20
            )

    st.markdown("### 🥡 Options Lunchbox")

    colL1, colL2 = st.columns(2)

    with colL1:
        lunchbox_count = st.slider(
            "🥡 Nombre de lunchboxes",
            0, 5, 0
        )

    with colL2:
        microwave = st.radio(
            "🔥 Micro-ondes disponible ?",
            ["Oui", "Non"],
            horizontal=True
        )
        has_microwave = (microwave == "Oui")

    st.divider()

    # Centrage du bouton
    col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])

    with col_btn_center:
        generate_button = st.button("🧠 Générer mon menu", type="primary", use_container_width=True)


    # 🔘 Bouton
    if generate_button:
        with st.spinner("Génération du menu en cours..."):
            raw_text = generate_meal_plan(
                regime, budget, temps, personnes, 
                type_menu, aliments_eviter,
                lunchbox_count, has_microwave
            )
            cleaned_text = clean_json_like(raw_text)

            try:
                parsed = json.loads(cleaned_text)

                # Jours lunchbox choisis par l'utilisateur
                days_order = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
                lunchbox_days = days_order[:lunchbox_count]

                # Récupération du menu généré par le modèle
                menu_data = parsed.get("menu", [])

                # 🔥 Application stricte de la logique lunchbox (soir → lendemain midi)
                menu_data = apply_lunchbox_rules(menu_data, lunchbox_days)

                # Stockage
                st.session_state["menu_data"] = menu_data
                st.session_state["lunchbox_days"] = lunchbox_days

                st.success("✅ Menu généré et parsé avec succès !")
            except Exception as e:
                st.error(f"Erreur JSON : {e}")
                st.text_area("Texte renvoyé :", cleaned_text, height=300)

            # -------------------------------
            # 👉 Affichage stylé du menu ici
            # -------------------------------
            if menu_data:
                st.divider()
                st.header("🍽️ Ton planning de repas")
                for day in menu_data:
                    st.markdown(f"### 📅 {day['jour']}")
                    for repas in day["repas"]:
                        with st.expander(f"🍴 {repas['moment'].capitalize()} – {repas['plat']}"):
                            st.write("**Ingrédients :**")
                            # 👉 ici
                            ingredients_list = [
                                f"{ing['name'].capitalize()} — {ing['quantity']} {ing['unit']}"
                                for ing in repas["ingredients"]
                            ]
                            st.markdown("- " + "\n- ".join(ingredients_list))

                            st.write("**Instructions :**")
                            instructions = repas["instructions"]
                            cleaned_instructions = []

                            for step in instructions:
                                # Parfois le modèle renvoie "0: '1. ....'" donc on nettoie
                                clean = step
                                clean = clean.replace("0:", "").replace("1:", "").replace("2:", "").replace("3:", "")
                                clean = clean.replace('"', '').strip()

                                cleaned_instructions.append(clean)

                            # Affichage propre
                            for step in cleaned_instructions:
                                st.markdown(f"- {step}")

# === Onglet 2 : Scan frigo ===
with tab2:
    st.header("📸 Scanner ton frigo ou tes placards")

    # === Upload de l'image ===
    uploaded_file = st.file_uploader("Prends une photo de ton frigo ou placard :", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:

        # Charger et afficher l'image
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Image importée", use_column_width=True)

        # === Bouton d'analyse ===
        if st.button("🔍 Analyser le contenu"):
            with st.spinner("Analyse en cours..."):
                
                detected = detect_food_items(image)

                # Sauvegarde en session pour éviter de perdre après refresh
                st.session_state["detected_items"] = detected
                st.session_state["confirmed_items"] = detected.copy()

            st.success("✅ Analyse terminée !")

    # 👉 Si déjà analysé auparavant, afficher bloc édition
    if "detected_items" in st.session_state:

        detected = st.session_state["detected_items"]
        selected = st.session_state["confirmed_items"]

        st.markdown("### 🍏 Aliments détectés")
        st.write(", ".join([f"**{item.capitalize()}**" for item in detected]))

        st.subheader("📝 Modifie ton inventaire")

        # === MULTISELECT persistant ===
        selected_new = st.multiselect(
            "Sélectionne les aliments que tu confirmes avoir :",
            options=detected,
            default=selected,
            key="multiselect_detected"
        )

        # Mise à jour de la liste sélectionnée
        st.session_state["confirmed_items"] = selected_new

        # === AJOUT d'un aliment manuel ===
        new_item = st.text_input("➕ Ajouter un aliment manquant :", placeholder="ex: beurre, riz, pommes...", key="add_item_input")

        if st.button("Ajouter cet aliment", key="add_item_button"):
            if new_item.strip():
                item = new_item.strip().lower()
                
                # Ajouter seulement s'il n'existe pas déjà
                if item not in [i.lower() for i in st.session_state["confirmed_items"]]:
                    st.session_state["confirmed_items"].append(item)
                    st.success(f"✔ '{new_item}' ajouté à ton inventaire !")
                else:
                    st.warning("⚠ Cet aliment est déjà présent.")
            else:
                st.warning("⚠ Entre un nom d’aliment valide.")

        # Affichage résumé
        selected = st.session_state["confirmed_items"]  # mise à jour
        st.info(f"Tu as confirmé **{len(selected)}** aliment(s) présent(s).")

        # Nettoyage
        selected = [s.lower().strip() for s in selected]

        st.divider()

        # === COMPARAISON AVEC LE MENU ===
        if "menu_data" in st.session_state:
            current_menu = st.session_state["menu_data"]
            ingredients = extract_ingredients(current_menu)

            # Normalisation des aliments du frigo
            selected = [s.lower().strip() for s in selected]

            # Conversion en objets homogènes
            selected_objects = [
                {"name": s, "quantity": None, "unit": None}
                for s in selected
            ]

            # 🔥 Correction : stocker dans la session pour éviter des incohérences
            st.session_state["confirmed_objects"] = selected_objects
            # Comparaison finale
            present, missing = compute_missing_items(
                ingredients,
                st.session_state["confirmed_objects"]
            )


            st.header("🧾 Résumé de ton inventaire")

            # Déjà dans le frigo
            st.subheader("✅ Déjà dans ton frigo :")
            if present:
                for p in present:
                    st.write(f"• {p['name'].capitalize()} — {p['quantity']} {p['unit']}")
            else:
                st.text("Aucun ingrédient du menu détecté dans ton frigo 😢")

            # À acheter
            st.subheader("❌ À acheter :")
            if missing:
                for m in missing:
                    st.write(f"• {m['name'].capitalize()} — {m['quantity']} {m['unit']}")

                st.download_button(
                    "💾 Télécharger la liste de courses",
                    data="\n".join([f"{m['name']} — {m['quantity']} {m['unit']}" for m in missing]),
                    file_name="liste_courses.txt",
                    mime="text/plain",
                    key="download_missing_tab2"
                )
            else:
                st.success("🎉 Ton frigo contient déjà tout pour ton menu !")

        else:
            st.warning("⚠️ Génère d'abord ton menu dans l'onglet Planificateur.")

# === Onglet 3 : Liste de courses ===
with tab3:
    st.header("🛒 Liste de courses automatique")

    # 1. Vérifier si un menu existe
    if "menu_data" not in st.session_state:
        st.warning("⚠️ Génère d'abord ton menu dans l'onglet 'Planificateur de repas'.")
        st.stop()

    # Extraire les ingrédients consolidés du menu
    menu_ingredients = extract_ingredients(st.session_state["menu_data"])

    # 2. Vérifier si un scan frigo existe
    fridge_items = []
    if os.path.exists("data/fridge.json"):
        with open("data/fridge.json", "r", encoding="utf-8") as f:
            fridge_items = json.load(f)

    # 3. Si on a un scan → comparer
    if fridge_items:
        present, missing = compute_missing_items(menu_ingredients, fridge_items)
    else:
        # Sinon → tout est manquant
        present = []
        missing = menu_ingredients

    # 4. Affichage de la liste
    st.subheader("❌ À acheter")

    if not missing:
        st.success("🎉 Tu as tout ce qu'il faut !")
    else:
        for ing in missing:
            st.write(f"- **{ing['name'].capitalize()}** — {ing['quantity']} {ing['unit']}")

        # 5. Bouton de téléchargement
        shopping_text = "\n".join([
            f"{ing['name']} — {ing['quantity']} {ing['unit']}" for ing in missing
        ])

        st.download_button(
            "💾 Télécharger la liste de courses",
            data=shopping_text,
            file_name="liste_courses.txt",
            mime="text/plain",
            key="download_missing_tab3"
        )

    # Si scan frigo existant → afficher aussi ce qu'on a
    if fridge_items:
        st.subheader("🧊 Déjà dans ton frigo")
        for p in present:
            st.write(f"- {p['name'].capitalize()} — {p['quantity']} {p['unit']}")


# -----------------------------
# 🔚 Pied de page
# -----------------------------
st.divider()
st.caption("© 2025 SmartMeal — Projet Albert School (Benjamin Caujolle)")
