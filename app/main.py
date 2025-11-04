import streamlit as st
from PIL import Image

# -----------------------------
# 🎯 Configuration de la page
# -----------------------------
st.set_page_config(
    page_title="SmartMeal - Planificateur de repas intelligent",
    page_icon="🥗",
    layout="wide"
)

# -----------------------------
# 🏷️ En-tête
# -----------------------------
st.title("🥗 SmartMeal")
st.subheader("Ton assistant repas intelligent 🍴")

st.write("""
Bienvenue sur **SmartMeal**, l'application qui t'aide à :
- planifier tes repas de la semaine 🍽️  
- générer automatiquement ta liste de courses 🛒  
- et scanner ton frigo/placard pour savoir ce qu'il te manque 📸  
""")

# -----------------------------
# 🧭 Barre latérale : préférences utilisateur
# -----------------------------
st.sidebar.header("⚙️ Paramètres de ton menu")

regime = st.sidebar.selectbox(
    "Régime alimentaire",
    ["Aucun", "Végétarien", "Végan", "Sans gluten", "Pescetarien"]
)

budget = st.sidebar.select_slider(
    "Budget par repas (€)",
    options=[3, 5, 7, 10, 15]
)

temps = st.sidebar.select_slider(
    "Temps max de préparation (min)",
    options=[10, 20, 30, 45, 60]
)

personnes = st.sidebar.number_input(
    "Nombre de personnes",
    min_value=1,
    max_value=8,
    value=2
)

# -----------------------------
# 🧩 Onglets principaux
# -----------------------------
tab1, tab2 = st.tabs(["📅 Planificateur de repas", "📸 Scan de frigo / placard"])

# === Onglet 1 : Planificateur ===
with tab1:
    st.header("📅 Génère ton menu hebdomadaire")

    st.write("Clique sur le bouton ci-dessous pour générer un planning personnalisé.")

    if st.button("🧠 Générer mon menu"):
        with st.spinner("Génération du menu en cours..."):
            # TODO: ici on intégrera le LLM (GPT, Llama, etc.)
            st.success("✅ Menu généré avec succès ! (placeholder)")
            st.info("Exemple : Lundi midi — Salade de lentilles aux légumes rôtis 🥕")

    st.divider()
    st.write("👉 Les repas générés s’afficheront ici avec leur liste d’ingrédients et étapes.")

# === Onglet 2 : Scan frigo ===
with tab2:
    st.header("📸 Scanner ton frigo ou tes placards")

    uploaded_file = st.file_uploader("Prends une photo de ton frigo ou placard :", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Image importée", use_column_width=True)

        if st.button("🔍 Analyser le contenu"):
            with st.spinner("Analyse en cours..."):
                # TODO: intégrer modèle vision ici (ex: GPT-4o vision ou CLIP)
                st.success("✅ Analyse terminée ! (placeholder)")
                st.info("Objets détectés : œufs, lait, beurre, tomates 🍅")

    st.divider()
    st.write("Les ingrédients détectés seront ensuite comparés à ta liste de courses.")

# -----------------------------
# 🔚 Pied de page
# -----------------------------
st.divider()
st.caption("© 2025 SmartMeal — Projet Albert School (Benjamin Caujolle)")
