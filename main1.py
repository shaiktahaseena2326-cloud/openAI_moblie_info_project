import streamlit as st
import random
import requests
from textblob import TextBlob

# ----------------------------------
# Mistral via Ollama
# ----------------------------------
def mistral_chat(messages):
    """Send conversation history to Mistral through Ollama"""
    try:
        url = "http://localhost:11434/api/chat"
        payload = {"model": "mistral", "messages": messages}
        response = requests.post(url, json=payload)
        data = response.json()
        if "message" in data:
            return data["message"]["content"]
        else:
            return "⚠️ Mistral returned an invalid response. Please ensure it's running."
    except Exception as e:
        return f"⚠️ Mistral Error: {e}"

# ----------------------------------
# Mobile Info Generator
# ----------------------------------
series_to_brand = {
    "iPhone": "Apple",
    "Galaxy S": "Samsung",
    "Galaxy Note": "Samsung",
    "OnePlus": "OnePlus",
    "Redmi Note": "Xiaomi",
    "V": "Vivo",
    "Realme": "Realme",
    "Oppo": "Oppo",
    "Motorola": "Motorola",
    "Poco": "Poco",
    "Nothing": "Nothing"
}

def get_mobile_info(mobile_name):
    mobile_name = mobile_name.strip().lower()
    series_found = None
    for series in series_to_brand.keys():
        if series.lower() in mobile_name:
            series_found = series
            break
    if not series_found:
        series_found = random.choice(list(series_to_brand.keys()))

    make = series_to_brand[series_found]
    model = mobile_name.title().replace(series_found, "").strip() or "Standard"
    launch_year = random.randint(2018, 2025)
    purchased_year = random.randint(launch_year, 2025)
    condition = random.choice(["New", "Used", "Refurbished"])
    price = f"₹{random.randint(8000, 100000)}"
    imei = str(random.randint(100000000000000, 999999999999999))

    return {
        "make": make,
        "series": series_found,
        "model": model,
        "launch_year": launch_year,
        "purchased_year": purchased_year,
        "condition": condition,
        "price": price,
        "imei_number": imei
    }

# ----------------------------------
# Sentiment Analysis
# ----------------------------------
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive 😊"
    elif polarity < -0.1:
        return "Negative 😞"
    else:
        return "Neutral 😐"

# ----------------------------------
# Streamlit Chat UI
# ----------------------------------
st.set_page_config(page_title="📱 Smart Mistral Mobile Chatbot", page_icon="🤖")
st.title("📱 Smart Mobile Chatbot — Powered by Mistral 🤖")
st.write("Chat about mobile phones — now with realistic follow-up questions!")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": (
            "You are a friendly and intelligent mobile expert chatbot. "
            "When a user mentions a mobile model, respond naturally and give useful information. "
            "After providing info, ask a logical follow-up question — like showing IMEI, comparing models, "
            "discussing resale value, or asking if the user wants pros and cons."
        )}
    ]
if "pending_action" not in st.session_state:
    st.session_state.pending_action = None
if "current_phone" not in st.session_state:
    st.session_state.current_phone = None

# Display chat history
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💻 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Mistral:** {msg['content']}")

# User input
user_input = st.chat_input("Ask about a mobile phone...") 

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # If answering a follow-up
    if st.session_state.pending_action:
        action = st.session_state.pending_action
        phone_info = st.session_state.current_phone

        if any(w in user_input.lower() for w in ["yes", "yeah", "sure", "ok", "of course"]):
            if action == "show_imei":
                ai_reply = f"The IMEI number for {phone_info['make']} {phone_info['series']} {phone_info['model']} is **{phone_info['imei_number']}**."
                next_question = random.choice([
                    "Would you like me to tell you its resale value?",
                    "Would you like to compare it with a similar model?",
                    "Do you want to know its top 3 pros and cons?"
                ])
                ai_reply += f"\n\n{next_question}"
                st.session_state.pending_action = "follow_up"
            elif action == "compare":
                compare_phone = random.choice(list(series_to_brand.keys()))
                ai_reply = f"This model is comparable to the **{compare_phone}** series in performance and pricing."
                st.session_state.pending_action = None
            elif action == "resale":
                resale = int(int(phone_info['price'].replace('₹','')) * random.uniform(0.3, 0.7))
                ai_reply = f"The estimated resale value is around ₹{resale}."
                st.session_state.pending_action = None
            elif action == "pros_cons":
                ai_reply = (
                    f"Pros:\n- Great performance\n- Good camera\n- Reliable brand\n\n"
                    f"Cons:\n- Slightly high price\n- Average battery life"
                )
                st.session_state.pending_action = None
            else:
                ai_reply = "Okay!"
        else:
            ai_reply = "Alright, skipping that step."
            st.session_state.pending_action = None

    else:
        # New phone mentioned
        phone_info = get_mobile_info(user_input)
        st.session_state.current_phone = phone_info

        # Generate info + Mistral review
        phone_details = (
            f"Make: {phone_info['make']}\n"
            f"Series: {phone_info['series']}\n"
            f"Model: {phone_info['model']}\n"
            f"Launch Year: {phone_info['launch_year']}\n"
            f"Condition: {phone_info['condition']}\n"
            f"Price: {phone_info['price']}\n"
        )

        ai_prompt = f"{user_input}\n\nHere are the phone details:\n{phone_details}\nGive a friendly review and ask one realistic follow-up question."
        with st.spinner("🤖 Thinking..."):
            ai_reply = mistral_chat(st.session_state.chat_history + [{"role": "user", "content": ai_prompt}])

        # Choose a logical follow-up question dynamically
        next_action = random.choice(["show_imei", "compare", "resale", "pros_cons"])
        followup_text = {
            "show_imei": "Would you like me to show its IMEI number?",
            "compare": "Would you like me to compare it with a similar model?",
            "resale": "Do you want to know its resale value?",
            "pros_cons": "Would you like me to tell you its top pros and cons?"
        }[next_action]

        ai_reply += f"\n\n{followup_text}"
        st.session_state.pending_action = next_action

    # Display response
    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
    st.markdown(f"🤖 **Mistral:** {ai_reply}")

    # Sentiment
    sentiment = analyze_sentiment(ai_reply)
    st.caption(f"📊 Sentiment of AI Response: {sentiment}")
