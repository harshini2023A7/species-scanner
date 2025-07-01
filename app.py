import streamlit as st
from utils.wiki_api import get_species_info, get_species_images
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import pandas as pd
import random

st.set_page_config(page_title="Agrimetric", layout="wide")
st.title("🌾 Agrimetric")
st.sidebar.title("🚜 Agrimetric Navigation")

app_mode = st.sidebar.selectbox("Choose Agrimetric Mode:", [
    "🌿 Species Identification", 
    "🩻 Pest Identification", 
    "💰 Crop Market Prices", 
    "🌱 Crop Health Tips"
])

@st.cache_resource
def load_model():
    return MobileNetV2(weights='imagenet')

model = load_model()

def predict_species(img_file):
    img = Image.open(img_file).convert('RGB')
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    decoded = decode_predictions(preds, top=1)[0][0]
    return decoded[1].replace('_', ' ')

def get_dynamic_prices(location):
    price_base = {
        "Rice": 2800,
        "Wheat": 2150,
        "Maize": 1900,
        "Cotton": 6700,
        "Sugarcane": 375,
        "Soybean": 4100
    }
    variation_map = {
        "Delhi": 50,
        "Mumbai": 70,
        "Bangalore": 30,
        "Chennai": 40,
        "Kolkata": 20,
        "Hyderabad": 60
    }
    variation = variation_map.get(location, 40)
    dynamic_prices = {}
    for crop, base in price_base.items():
        fluctuation = random.randint(-variation, variation)
        current_price = base + fluctuation
        last_week_price = current_price - random.randint(-10, 20)
        dynamic_prices[crop] = {
            "current": current_price,
            "last_week": last_week_price,
            "unit": "₹/quintal"
        }
    return dynamic_prices

PEST_CONTROL_DB = {
    "aphid": {"organic": ["Neem oil spray", "Ladybug release"], "chemical": ["Imidacloprid"], "description": "Feed on sap."},
    "caterpillar": {"organic": ["Bt", "Hand picking"], "chemical": ["Chlorpyrifos"], "description": "Feed on leaves."}
}

CROP_HEALTH_TIPS = {
    "Rice": {"Kharif": "Watch for blast disease.", "soil_tips": "pH 5.5-7.0.", "rainfall_alert": "Avoid waterlogging."},
    "Wheat": {"Rabi": "Watch for rust.", "soil_tips": "pH 6.0-7.5.", "rainfall_alert": "Avoid excessive moisture."},
    "Tomato": {"Kharif": "Protect from fruit borer.", "Rabi": "Monitor for late blight.", "soil_tips": "pH 6.0-7.0.", "rainfall_alert": "Mulch to avoid rot."},
    "Potato": {"Kharif": "Prevent leaf curl.", "Rabi": "Ideal sowing time.", "soil_tips": "pH 5.5-6.5.", "rainfall_alert": "Avoid tuber rot."},
    "Onion": {"Kharif": "Control damping-off.", "Rabi": "Irrigate carefully.", "soil_tips": "pH 6.0-7.5.", "rainfall_alert": "Avoid bulb rot."},
    "Chili": {"Kharif": "Resist wilt.", "Rabi": "Check for thrips.", "soil_tips": "pH 6.0-7.0.", "rainfall_alert": "Prevent water stagnation."},
    "Brinjal": {"Kharif": "Use pheromone traps.", "Rabi": "Ensure sunlight.", "soil_tips": "pH 5.5-6.8.", "rainfall_alert": "Ensure drainage."},
    "Cabbage": {"Kharif": "Use neem oil.", "Rabi": "Maintain spacing.", "soil_tips": "pH 6.0-7.0.", "rainfall_alert": "Avoid root damage."},
    "Cauliflower": {"Kharif": "Control boron deficiency.", "Rabi": "Monitor for curd development.", "soil_tips": "pH 6.0-6.5.", "rainfall_alert": "Ensure no waterlogging."},
    "Carrot": {"Kharif": "Thin seedlings timely.", "Rabi": "Prevent cracking of roots.", "soil_tips": "pH 6.0-6.8.", "rainfall_alert": "Maintain consistent moisture."},
    "Peas": {"Kharif": "Watch for powdery mildew.", "Rabi": "Avoid aphid infestation.", "soil_tips": "pH 6.0-7.5.", "rainfall_alert": "Avoid excess moisture."},
    "Spinach": {"Kharif": "Control leaf spot.", "Rabi": "Ensure fast drainage.", "soil_tips": "pH 6.5-7.0.", "rainfall_alert": "Avoid waterlogging."},
    "Cucumber": {"Kharif": "Prevent downy mildew.", "Rabi": "Support vine growth.", "soil_tips": "pH 5.5-6.8.", "rainfall_alert": "Ensure good drainage."}
}

if app_mode == "🌿 Species Identification":
    st.header("Species Identification")
    option = st.radio("Choose input method:", ["Enter Species Name", "Upload Image"])
    if option == "Enter Species Name":
        species_name = st.text_input("Enter species name (e.g., Panthera leo):")
        if st.button("Scan"):
            if not species_name:
                st.warning("Please enter a species name.")
            else:
                st.info("🔍 Searching...")
                info = get_species_info(species_name)
                images = get_species_images(species_name)
                if info:
                    st.success("✅ Species found!")
                    st.subheader("🧬 Classification")
                    st.json(info.get("classification", {}))
                    st.subheader("😁 Fun Facts")
                    st.write(info.get("summary", "No interesting facts found."))
                    if images:
                        st.subheader("🖼 Images")
                        for img in images:
                            st.image(img, use_column_width=True)
                else:
                    st.error("❌ Species not found.")
    elif option == "Upload Image":
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            predicted_species = predict_species(uploaded_file)
            st.success(f"🧠 Predicted species: {predicted_species}")
            info = get_species_info(predicted_species)
            images = get_species_images(predicted_species)
            if info:
                st.subheader("🧬 Classification")
                st.json(info.get("classification", {}))
                st.subheader("😁 Fun Facts")
                st.write(info.get("summary", "No interesting facts found."))
                if images:
                    st.subheader("🖼 Images")
                    for img in images:
                        st.image(img, use_column_width=True)
            else:
                st.warning("⚠ No species info found for this prediction.")
elif app_mode == "🩻 Pest Identification":
    st.header("Pest Identification")
    uploaded_pest_file = st.file_uploader("Upload pest image", type=["jpg", "png"], key="pest")
    if uploaded_pest_file is not None:
        st.image(uploaded_pest_file, caption="Uploaded Pest Image", use_column_width=True)
        predicted_pest = predict_species(uploaded_pest_file).lower()
        pest_type = "aphid"
        for pest in PEST_CONTROL_DB:
            if pest in predicted_pest:
                pest_type = pest
                break
        st.success(f"🩯 Identified Pest: {pest_type.title()}")
        st.write(f"Description: {PEST_CONTROL_DB[pest_type]['description']}")
        st.subheader("Organic Measures")
        for measure in PEST_CONTROL_DB[pest_type]['organic']:
            st.write(f"- {measure}")
        st.subheader("Chemical Measures")
        for measure in PEST_CONTROL_DB[pest_type]['chemical']:
            st.write(f"- {measure}")
elif app_mode == "💰 Crop Market Prices":
    st.header("Crop Market Prices")
    location = st.selectbox("Select your location:", ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad"])
    st.subheader(f"Prices for {location}")
    SAMPLE_CROP_PRICES = get_dynamic_prices(location)
    price_data = []
    for crop, data in SAMPLE_CROP_PRICES.items():
        change = data['current'] - data['last_week']
        change_pct = (change / data['last_week']) * 100 if data['last_week'] else 0
        trend = "📈" if change > 0 else "📉" if change < 0 else "➡"
        price_data.append({
            "Crop": crop,
            "Current Price": f"{data['current']} {data['unit']}",
            "Last Week": f"{data['last_week']} {data['unit']}",
            "Change": f"{trend} {change:+} ({change_pct:.1f}%)"
        })
    st.table(pd.DataFrame(price_data))
elif app_mode == "🌱 Crop Health Tips":
    st.header("Crop Health Tips")
    col1, col2 = st.columns(2)
    with col1:
        selected_crop = st.selectbox("Select your crop:", list(CROP_HEALTH_TIPS.keys()))
    with col2:
        season = st.selectbox("Season:", ["Kharif", "Rabi"])
    tips = CROP_HEALTH_TIPS[selected_crop]
    st.subheader(f"Tips for {selected_crop} in {season} season")
    st.success(tips.get(season, "No specific tips."))
    st.info(f"Soil Tip: {tips['soil_tips']}")
    st.warning(f"Rainfall Alert: {tips['rainfall_alert']}")

st.sidebar.markdown("---")
st.sidebar.info("Built for farmers and agri researchers")
