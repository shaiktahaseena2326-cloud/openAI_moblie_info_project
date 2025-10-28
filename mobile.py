import streamlit as st
import pandas as pd
import random
from textblob import TextBlob

# -------------------------------
# Load mobile phone data from CSV
# -------------------------------
@st.cache_data
def load_mobile_data(csv_file="mobile_phones.csv"):
    return pd.read_csv(csv_file)

mobile_df = load_mobile_data()

# -------------------------------
# Function to get mobile info
# -------------------------------
def get_mobile_info(mobile_name):
    name_lower = mobile_name.strip().lower()
    filtered = mobile_df[mobile_df['Model'].str.lower() == name_lower]

    if not filtered.empty:
        phone = filtered.sample(1).iloc[0]  # Pick a random row if duplicates
        # Generate IMEI number and condition dynamically
        imei = str(random.randint(100000000000000, 999999999999999))
        condition = random.choice(["New", "Used", "Refurbished"])
        price = phone['Price']  # Use price from CSV
        launch_year = phone['Launch_Year']  # Use year from CSV

        return {
            "make": phone["Brand"],
            "series": phone["Series"],
            "model": phone["Model"],
            "launch_year": launch_year,
            "condition": condition,
            "price": price,
            "imei_number": imei
        }
    else:
        return None

# -------------------------------
# Sentiment analysis
# -------------------------------
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive 😊"
    elif polarity < -0.1:
        return "Negative 😞"
    else:
        return "Neutral 😐"

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title=" Mobile Info Chatbot", page_icon="🤖")
st.title(" Mobile Info Chatbot")
st.write("Type any mobile model to see full details:")

user_input = st.text_input("Enter Mobile Model (e.g., iPhone 15)")
user_review = st.text_area("Write your comment about the phone (optional)")

if st.button("Get Mobile Info"):
    if user_input.strip():
        data = get_mobile_info(user_input)
        if data:
            st.success("Here are the details:")
            st.write(f"**Make:** {data['make']}")
            st.write(f"**Series:** {data['series']}")
            st.write(f"**Model:** {data['model']}")
            st.write(f"**Launch Year:** {data['launch_year']}")
            st.write(f"**Condition:** {data['condition']}")
            st.write(f"**Price:** {data['price']}")
            st.write(f"**IMEI Number:** {data['imei_number']}")
            
            if user_review.strip():
                sentiment = analyze_sentiment(user_review)
                st.info(f"**Sentiment Analysis of your comment:** {sentiment}")
        else:
            st.error("❌ Sorry, no data found for this mobile.")
    else:
        st.warning("Please enter a mobile model.")  
#import pandas as pd
# import random

# brands_series = {
#     "Apple": ["iPhone"],
#     "Samsung": ["Galaxy S", "Galaxy Note"],
#     "OnePlus": ["OnePlus"],
#     "Xiaomi": ["Redmi Note", "Mi"],
#     "Realme": ["Realme"],
#     "Vivo": ["V"],
#     "Oppo": ["Oppo"],
#     "Motorola": ["Moto"],
#     "Poco": ["Poco"],
#     "Nothing": ["Nothing"]
# }

# data = []

# for brand, series_list in brands_series.items():
#     for series in series_list:
#         for i in range(1, 21):  # 20 models per series
#             model_number = f"{series} {i}"
#             launch_year = random.randint(2018, 2025)
#             price = f"₹{random.randint(8000, 100000)}"
#             data.append({
#                 "Brand": brand,
#                 "Series": series,
#                 "Model": model_number,
#                 "Launch_Year": launch_year,
#                 "Price": price
#             })

# df = pd.DataFrame(data)
# df.to_csv("mobile_phones.csv", index=False)
# print("CSV file 'mobile_phones.csv' generated successfully!")
