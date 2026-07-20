import streamlit as st
import pandas as pd
import requests

# App Ka Look Aur Layout
st.set_page_config(page_title="Global Veg Diet Tracker Pro", page_icon="🏋️‍♂️", layout="centered")

st.title("🏋️‍♂️ Global Veg Muscle Tracker Pro")
st.markdown("### 🌍 World Recipe Search & Custom Kitchen Dashboard")
st.write("---")

# Daily Gym Targets
TARGET_CALORIES = 2700
TARGET_PROTEIN = 130
TARGET_CARBS = 350
TARGET_FATS = 80

# --- APNI API KEY YAHAN DALEIN ---
API_KEY = "YAHAN_APNI_API_KEY_DALEIN" 

# Session State Initialize karna taaki data safe rahe
if 'custom_db' not in st.session_state:
    st.session_state.custom_db = {
        "Standard Paneer (100g)": {"cal": 265, "prot": 18.0, "carb": 1.2, "fat": 20.0},
        "Oats Milk Shake (1 Glass)": {"cal": 310, "prot": 12.5, "carb": 45.0, "fat": 7.0},
    }

if 'meals_logged' not in st.session_state:
    st.session_state.meals_logged = []

# ==========================================
# ⚡ DO MAIN OPTIONS (TABS SYSTEM)
# ==========================================
tab1, tab2 = st.tabs(["🌍 World Recipe Search", "🍳 My Custom Kitchen (Apni Recipe)"])

# ------------------------------------------
# TAB 1: DUNIYA KI KOI BHI RECIPE SEARCH KAREIN
# ------------------------------------------
with tab1:
    st.subheader("🔍 Global Food & Recipe Search")
    st.info("Duniya ki koi bhi dish aur uska weight yahan likhein. Internet se data turant add ho jayega.")
    
    col_dish, col_wt = st.columns([2, 1])
    with col_dish:
        global_dish = st.text_input("Dish / Recipe Ka Naam:", placeholder="e.g. Rajma Chawal, Veg Biryani, Tofu Salad", key="g_dish")
    with col_wt:
        global_wt = st.number_input("Weight (Grams me):", min_value=1, value=150, key="g_wt")
        
    if st.button("🌐 Internet Se Dhundo Aur Add Karo", use_container_width=True):
        if global_dish and API_KEY != "YAHAN_APNI_API_KEY_DALEIN":
            with st.spinner('Global server se recipe dhoondh raha hu... ⏳'):
                # API ko command dena (e.g., "150g Rajma Chawal")
                full_q = f"{global_wt}g {global_dish}"
                api_url = f'https://api.calorieninjas.com/v1/nutrition?query={full_q}'
                response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
                
                if response.status_code == requests.codes.ok:
                    data = response.json()
                    if data['items']:
                        t_cal = sum(i['calories'] for i in data['items'])
                        t_prot = sum(i['protein_g'] for i in data['items'])
                        t_carb = sum(i['carbohydrates_total_g'] for i in data['items'])
                        t_fat = sum(i['fat_total_g'] for i in data['items'])
                        
                        d_name = f"{global_dish.title()} ({global_wt}g)"
                        st.session_state.custom_db[d_name] = {"cal": t_cal, "prot": t_prot, "carb": t_carb, "fat": t_fat}
                        st.session_state.meals_logged.append({"Food": d_name, "Qty": 1.0})
                        st.success(f"✅ {d_name} mil gaya aur aapke aaj ke Diet Log me add ho gaya!")
                        st.rerun()
                    else:
                        st.warning("❌ Yeh dish nahi mili! Kripya thoda simple English naam likhein.")
                else:
                    st.error("❌ Connection Error! Apni API Key check karein.")
        else:
            st.warning("⚠️ Kripya dish ka naam likhein aur code me API key check karein.")

# ------------------------------------------
# TAB 2: APNI PASAND KI RECIPE BANAKAR SAVE KAREIN
# ------------------------------------------
with tab2:
    st.subheader("🍳 Create Your Own Recipe")
    st.info("Agar aap ghar par koi mix khana bana rahe hain, toh uske ingredients yahan ek baar me daal kar apni permanent recipe banayein.")
    
    custom_recipe_name = st.text_input("Nayi Recipe Ka Naam Rakhein:", placeholder="e.g. Deepak Special Muscle Salad")
    ingredients_list = st.text_area("Recipe Me Kya-Kya Dala? (Vazan Ke Sath Likhein):", 
                                    placeholder="e.g. 100g paneer, 50g soya chunks, 10g almonds")
    
    if st.button("💾 Apni Recipe Banakar Save Karein", use_container_width=True):
        if custom_recipe_name and ingredients_list and API_KEY != "YAHAN_APNI_API_KEY_DALEIN":
            with st.spinner('Aapki recipe ka nutrition calculate ho raha hai... 🍳'):
                api_url = f'https://api.calorieninjas.com/v1/nutrition?query={ingredients_list}'
                response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
                
                if response.status_code == requests.codes.ok:
                    data = response.json()
                    if data['items']:
                        t_cal = sum(i['calories'] for i in data['items'])
                        t_prot = sum(i['protein_g'] for i in data['items'])
                        t_carb = sum(i['carbohydrates_total_g'] for i in data['items'])
                        t_fat = sum(i['fat_total_g'] for i in data['items'])
                        
                        # Database me hamesha ke liye save ho jayega
                        st.session_state.custom_db[custom_recipe_name] = {"cal": t_cal, "prot": t_prot, "carb": t_carb, "fat": t_fat}
                        st.success(f"🎉 Aalishan! '{custom_recipe_name}' save ho gayi. Ab aap ise niche list se kabhi bhi add kar sakte hain!")
                        st.rerun()
                    else:
                        st.warning("❌ Items ki sahi details nahi mil payi.")
                else:
                    st.error("❌ Server Error.")
        else:
            st.warning("⚠️ Kripya Naam aur Ingredients dono bharein!")

st.write("---")

# ==========================================
# 📂 SAVED LIST SE ADD KARNA (Dropdown)
# ==========================================
st.subheader("📂 Saved Recipes & Items Dropdown")
c_sel, c_qt = st.columns([2, 1])
with c_sel:
    saved_food = st.selectbox("Apni Saved List Se Chunein (Yahan Aapki Banayi Recipes Bhi Dikhengi):", list(st.session_state.custom_db.keys()))
with c_qt:
    saved_qty = st.number_input("Quantity / Serving:", min_value=0.5, value=1.0, step=0.5, key="saved_qty_input")
if st.button("➕ Log Selected Item", use_container_width=True):
    st.session_state.meals_logged.append({"Food": saved_food, "Qty": saved_qty})
    st.success(f"{saved_food} add ho gaya!")
    st.rerun()

# ==========================================
# 📊 LIVE DASHBOARD & EDIT/DELETE LOGS
# ==========================================
st.write("---")
st.subheader("📊 Aaj Ka Live Tracker Dashboard")

total_cal, total_prot, total_carb, total_fat = 0, 0, 0, 0
for item in st.session_state.meals_logged:
    food = item["Food"]
    qty = item["Qty"]
    if food in st.session_state.custom_db:
        total_cal += st.session_state.custom_db[food]["cal"] * qty
        total_prot += st.session_state.custom_db[food]["prot"] * qty
        total_carb += st.session_state.custom_db[food]["carb"] * qty
        total_fat += st.session_state.custom_db[food]["fat"] * qty

m1, m2 = st.columns(2)
m1.metric("Calories Consumed", f"{total_cal:.0f} / {TARGET_CALORIES} kcal")
m2.metric("Protein Intake", f"{total_prot:.1f} / {TARGET_PROTEIN}g")
st.progress(min(1.0, total_prot / TARGET_PROTEIN))
st.caption(f"💡 Target ke liye baki Protein: **{max(0.0, TARGET_PROTEIN - total_prot):.1f}g**")

if total_prot >= TARGET_PROTEIN and total_cal >= TARGET_CALORIES:
    st.balloons()
    st.success("🎉 Shabaash! Aaj ka Muscle Gain Target Poora Hua!")

# DIET LOG MEIN EDIT AUR DELETE
if st.session_state.meals_logged:
    st.write("### 🍽️ Aaj Ka Khana (Diet Log)")
    
    for index, item in enumerate(st.session_state.meals_logged):
        food_item = item["Food"]
        current_qty = item["Qty"]
        nutr = st.session_state.custom_db[food_item]
        
        c_disp, p_disp = nutr['cal'] * current_qty, nutr['prot'] * current_qty
        
        col_text, col_edit, col_del = st.columns([3, 1, 1])
        with col_text:
            st.write(f"**{food_item}** x {current_qty} | 🥩 {p_disp:.1f}g P | 🔥 {c_disp:.0f} kcal")
        
        with col_edit:
            new_qty = st.number_input("Edit", min_value=0.1, max_value=10.0, value=float(current_qty), key=f"edit_{index}", step=0.5)
            if new_qty != current_qty:
                st.session_state.meals_logged[index]["Qty"] = new_qty
                st.rerun()
                
        with col_del:
            if st.button("🗑️ Hataen", key=f"del_{index}"):
                st.session_state.meals_logged.pop(index)
                st.rerun()

    if st.button("🔄 Reset Whole Day", use_container_width=True):
        st.session_state.meals_logged = []
        st.rerun()
