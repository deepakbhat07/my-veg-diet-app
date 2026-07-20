import streamlit as st
import pandas as pd

# Page Configuration (App Ka Look)
st.set_page_config(page_title="Veg Gym Diet Tracker", page_icon="🌱", layout="centered")

st.title("🏋️‍♂️ Pure Veg Muscle Gain Tracker")
st.markdown("### Height: 5'9\" | Target Weight: 72-75 kg")
st.write("---")

# 1. Daily Targets (Aapka Target)
TARGET_CALORIES = 2700
TARGET_PROTEIN = 130
TARGET_CARBS = 350
TARGET_FATS = 80

# 2. Pure Veg Food Database
veg_database = {
    "Daliya (Dry) - 50g": {"cal": 170, "prot": 6.0, "carb": 36.0, "fat": 0.5},
    "Full Cream Milk - 300ml": {"cal": 180, "prot": 10.0, "carb": 14.0, "fat": 9.0},
    "Toned Milk - 250ml": {"cal": 120, "prot": 8.0, "carb": 12.0, "fat": 4.5},
    "Paneer - 100g": {"cal": 265, "prot": 18.0, "carb": 1.2, "fat": 20.0},
    "Tofu - 100g": {"cal": 144, "prot": 14.0, "carb": 2.5, "fat": 8.0},
    "Peanut Butter - 1 tbsp": {"cal": 95, "prot": 4.0, "carb": 3.0, "fat": 8.0},
    "Banana (Kela) - 1 Medium": {"cal": 105, "prot": 1.3, "carb": 27.0, "fat": 0.3},
    "Moong Dal (Cooked) - 1 Katori": {"cal": 150, "prot": 8.0, "carb": 24.0, "fat": 0.5},
    "Kala Chana (Boiled) - 1 Katori": {"cal": 200, "prot": 11.0, "carb": 32.0, "fat": 2.0},
    "Rajma (Cooked) - 1 Katori": {"cal": 180, "prot": 9.0, "carb": 28.0, "fat": 0.6},
    "Soya Chunks (Dry) - 30g": {"cal": 105, "prot": 15.0, "carb": 10.0, "fat": 0.2},
    "Roti (Wheat) - 1 Roti": {"cal": 85, "prot": 3.0, "carb": 18.0, "fat": 0.4},
    "Rice (Cooked) - 1 Katori": {"cal": 200, "prot": 4.0, "carb": 44.0, "fat": 0.4},
    "Almonds (Badam) - 10 pcs": {"cal": 70, "prot": 2.5, "carb": 2.5, "fat": 6.0},
    "Oats (Dry) - 40g": {"cal": 150, "prot": 5.0, "carb": 27.0, "fat": 2.5},
    "Curd (Dahi) - 1 Katori": {"cal": 100, "prot": 5.0, "carb": 6.0, "fat": 6.0},
}

# Session State for storing meals (Taaki data save rahe)
if 'meals_logged' not in st.session_state:
    # Pehle se daliya breakfast add kar dete hain sample ke liye
    st.session_state.meals_logged = [
        {"Food": "Daliya (Dry) - 50g", "Qty": 1.0},
        {"Full Cream Milk - 300ml": "Full Cream Milk - 300ml", "Food": "Full Cream Milk - 300ml", "Qty": 1.0},
        {"Food": "Peanut Butter - 1 tbsp", "Qty": 1.0},
        {"Food": "Banana (Kela) - 1 Medium", "Qty": 1.5}
    ]

# 3. Input Section (Khana Add Karne Ke Liye)
st.subheader("📝 Aaj Kya Khaya? (Add Meal)")
col1, col2 = st.columns([2, 1])

with col1:
    selected_food = st.selectbox("Khana Chunein (Dropdown):", list(veg_database.keys()))
with col2:
    quantity = st.number_input("Quantity (Servings):", min_value=0.1, value=1.0, step=0.5)

if st.button("➕ Add to Diet Log", use_container_width=True):
    st.session_state.meals_logged.append({"Food": selected_food, "Qty": quantity})
    st.success(f"{selected_food} x {quantity} add ho gaya!")

# 4. Calculate Totals
total_cal, total_prot, total_carb, total_fat = 0, 0, 0, 0
log_data = []

for item in st.session_state.meals_logged:
    food = item["Food"]
    qty = item["Qty"]
    nutrients = veg_database[food]
    
    c = nutrients["cal"] * qty
    p = nutrients["prot"] * qty
    ch = nutrients["carb"] * qty
    f = nutrients["fat"] * qty
    
    total_cal += c
    total_prot += p
    total_carb += ch
    total_fat += f
    
    log_data.append([food, qty, f"{c:.0f} kcal", f"{p:.1f}g", f"{ch:.1f}g", f"{f:.1f}g"])

# 5. Live Dashboard Metrics
st.write("---")
st.subheader("📊 Aapka Live Dashboard")

m1, m2, m3 = st.columns(3)
m1.metric("Calories Consumed", f"{total_cal:.0f} / {TARGET_CALORIES} kcal")
m2.metric("Protein Intake", f"{total_prot:.1f} / {TARGET_PROTEIN}g")
st.caption(f"Baki Protein: {max(0.0, TARGET_PROTEIN - total_prot):.1f}g")

# Progress Bars
prot_percent = min(1.0, total_prot / TARGET_PROTEIN)
st.write("**Protein Progress:**")
st.progress(prot_percent)

# Goal Check
if total_prot >= TARGET_PROTEIN and total_cal >= TARGET_CALORIES:
    st.balloons()
    st.success("🎉 Shabaash! Aaj ka Protein aur Calorie target poora hua. Muscles grow kar rahi hain!")

# 6. Display Logged Meals Table
if log_data:
    st.write("---")
    st.subheader("🍽️ Aaj Ka Khana (Diet Log)")
    df = pd.DataFrame(log_data, columns=["Food Item", "Quantity", "Calories", "Protein", "Carbs", "Fats"])
    st.dataframe(df, use_container_width=True)
    
    if st.button("🗑️ Clear All (Naya Din Shuru Karein)"):
        st.session_state.meals_logged = []
        st.rerun()
      
