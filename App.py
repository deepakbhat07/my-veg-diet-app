      
import streamlit as st
import pandas as pd
import requests

# App Ka Look Aur Layout
st.set_page_config(page_title="Smart Veg Diet Tracker", page_icon="🌱", layout="centered")

st.title("🏋️‍♂️ Smart Veg Muscle Tracker")
st.markdown("### 🔍 Gram Input Aur Auto-Nutrition Fetch Ke Sath")
st.write("---")

# Aapke Targets (5'9" Height aur Gym Ke Hisab Se)
TARGET_CALORIES = 2700
TARGET_PROTEIN = 130
TARGET_CARBS = 350
TARGET_FATS = 80

# --- APNI API KEY YAHAN DALEIN ---
API_KEY = "YAHAN_APNI_API_KEY_DALEIN" 

# Database State initialized
if 'custom_db' not in st.session_state:
    st.session_state.custom_db = {
        "Daliya": {"cal": 170, "prot": 6.0, "carb": 36.0, "fat": 0.5, "base_wt": 50},
        "Milk": {"cal": 180, "prot": 10.0, "carb": 14.0, "fat": 9.0, "base_wt": 300},
    }

if 'meals_logged' not in st.session_state:
    st.session_state.meals_logged = []

# ==========================================
# 1. SMART ONLINE SEARCH (Gram Option Ke Sath)
# ==========================================
st.subheader("🌐 Naya Khana Search Karein")
st.info("Khane ka naam aur vazan (grams) alag se dalein. Internet se nutrition apne aap aa jayega!")

col_name, col_gram = st.columns([2, 1])
with col_name:
    search_query = st.text_input("Khane Ka Naam (Veg Only):", placeholder="e.g. Paneer, Tofu, Oats")
with col_gram:
    search_grams = st.number_input("Kitne Gram (Weight in g):", min_value=1, value=100, step=10)

search_btn = st.button("🔍 Internet Se Auto-Fetch Karein", use_container_width=True)

if search_btn and search_query:
    if API_KEY == "YAHAN_APNI_API_KEY_DALEIN":
        st.error("⚠️ Pehle code me apni CalorieNinjas ki API Key dalein!")
    else:
        with st.spinner('Internet database se data nikal raha hu... ⏳'):
            # Dono fields ko jod kar query banana (e.g. "100g paneer")
            full_query = f"{search_grams}g {search_query}"
            api_url = f'https://api.calorieninjas.com/v1/nutrition?query={full_query}'
            response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
            
            if response.status_code == requests.codes.ok:
                data = response.json()
                if data['items']:
                    # Items ka nutrition nikalna
                    total_cal = sum(item['calories'] for item in data['items'])
                    total_prot = sum(item['protein_g'] for item in data['items'])
                    total_carb = sum(item['carbohydrates_total_g'] for item in data['items'])
                    total_fat = sum(item['fat_total_g'] for item in data['items'])
                    
                    display_name = f"{search_query.title()} ({search_grams}g)"
                    
                    # Database me save karna
                    st.session_state.custom_db[display_name] = {
                        "cal": total_cal, "prot": total_prot, "carb": total_carb, "fat": total_fat, "base_wt": search_grams
                    }
                    st.success(f"✅ {display_name} Mil Gaya! (Protein: {total_prot}g, Calories: {total_cal}) - List me save ho gaya.")
                    st.rerun()
                else:
                    st.warning("❌ Data nahi mila! Kripya simple naam likhein (Jaise: Almonds, Rice, Rajma).")
            else:
                st.error("❌ Server Error! Kripya apni API Key check karein.")

st.write("---")

# ==========================================
# 2. DIET LOG (Aaj Kya Khaya)
# ==========================================
st.subheader("📝 Daily Diet Entry Log")

if list(st.session_state.custom_db.keys()):
    col_select, col_qty = st.columns([2, 1])
    with col_select:
        selected_food = st.selectbox("Apni Saved List Se Chunein:", list(st.session_state.custom_db.keys()))
    with col_qty:
        # Quantity dynamic multiply karne ke liye (e.g. 1 serving, 2 serving)
        quantity = st.number_input("Quantity (Kitni Baar Khaya):", min_value=0.5, value=1.0, step=0.5)

    if st.button("➕ Add to Log", use_container_width=True):
        st.session_state.meals_logged.append({"Food": selected_food, "Qty": quantity})
        st.success(f"{selected_food} successfully log ho gaya!")
        st.rerun()

# ==========================================
# 3. LIVE DASHBOARD & PROGRESS
# ==========================================
total_cal, total_prot, total_carb, total_fat = 0, 0, 0, 0
log_data = []

for item in st.session_state.meals_logged:
    food = item["Food"]
    qty = item["Qty"]
    if food in st.session_state.custom_db:
        nutrients = st.session_state.custom_db[food]
        c = nutrients["cal"] * qty
        p = nutrients["prot"] * qty
        ch = nutrients["carb"] * qty
        f = nutrients["fat"] * qty
        
        total_cal += c
        total_prot += p
        total_carb += ch
        total_fat += f
        log_data.append([food, qty, f"{c:.0f} kcal", f"{p:.1f}g", f"{ch:.1f}g", f"{f:.1f}g"])

st.write("---")
st.subheader("📊 Aaj Ki Diet Progress")
m1, m2 = st.columns(2)
m1.metric("Calories Consumed", f"{total_cal:.0f} / {TARGET_CALORIES} kcal")
m2.metric("Protein Intake", f"{total_prot:.1f} / {TARGET_PROTEIN}g")

# Remaining info text
st.caption(f"💡 Target poora karne ke liye abhi **{max(0.0, TARGET_PROTEIN - total_prot):.1f}g Protein** aur khana hai.")
st.progress(min(1.0, total_prot / TARGET_PROTEIN))

if total_prot >= TARGET_PROTEIN and total_cal >= TARGET_CALORIES:
    st.balloons()
    st.success("🎉 Shabaash Deepak! Aaj ka muscle building target complete!")

if log_data:
    st.write("---")
    df = pd.DataFrame(log_data, columns=["Food Item", "Servings", "Calories", "Protein", "Carbs", "Fats"])
    st.dataframe(df, use_container_width=True)
    
    if st.button("🗑️ Reset (Naya Din Shuru Karein)"):
        st.session_state.meals_logged = []
        st.rerun()
