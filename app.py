import streamlit as st
from utils.fetch_data import get_species_info, get_commons_image
from utils.farmer_helpers import identify_pest, get_crop_prices, get_health_tips

st.set_page_config(page_title="AgriScan - Smart Farming Tool", layout="centered")
st.title("🌾 AgriScan")
st.write("Identify pests, get market prices, and crop health tips — all in one place!")

st.sidebar.title("Choose a Feature")
feature = st.sidebar.radio("Select", ["Species Identifier", "Pest Identifier", "Crop Market Prices", "Crop Health Tips"])

if feature == "Species Identifier":
    query = st.text_input("Enter species name", placeholder="e.g. Panthera tigris")
    if query:
        with st.spinner("Fetching data..."):
            info = get_species_info(query)
            img_url = get_commons_image(query)
            if img_url:
                st.image(img_url, caption=query)
            st.markdown("### Classification and Details")
            st.markdown(info if info else "No details found.")

elif feature == "Pest Identifier":
    uploaded_file = st.file_uploader("Upload an image of the pest", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        with st.spinner("Identifying pest..."):
            result = identify_pest(uploaded_file)
            st.image(uploaded_file, caption="Uploaded Pest Image")
            st.success(f"Detected Pest: {result['name']}")
            st.markdown(f"**Control Tips:** {result['tips']}")

elif feature == "Crop Market Prices":
    crop = st.text_input("Enter crop name", placeholder="e.g. Tomato")
    if crop:
        prices = get_crop_prices(crop)
        st.markdown(f"### Market Prices for {crop.capitalize()}")
        st.table(prices)

elif feature == "Crop Health Tips":
    crop = st.text_input("Enter your crop name", placeholder="e.g. Paddy")
    if crop:
        tips = get_health_tips(crop)
        st.markdown("### Health Tips")
        for tip in tips:
            st.markdown(f"- {tip}")