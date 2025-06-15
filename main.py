import streamlit as st
from agent import HoroscopeAgent
from datetime import date
import random
import hashlib
from PIL import Image
from io import BytesIO
import base64
from auth_ui import login_signup_ui, show_logged_in_user

st.set_page_config(page_title="🔮 Gemini Horoscope Agent", layout="centered")
def load_css(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
load_css("styles.css")

def get_base64_of_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img_base64 = get_base64_of_image("images/plain.jpg") 

st.markdown(f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/jpg;base64,{bg_img_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🔮 Navigation")
page = st.sidebar.radio("Go to", ["Daily Horoscope", "Compatibility Checker", "Tarot Cards", "Login / Signup"])
show_logged_in_user()
if page == "Login / Signup":
    st.title("🔐 Welcome to Horoscope Portal")
    login_signup_ui()
if "last_page" not in st.session_state:
    st.session_state.last_page = page
if page != st.session_state.last_page:
    st.session_state.flipped = [False, False, False]
    st.session_state.last_page = page

agent = HoroscopeAgent("Anonymous", "2000-01-01")
tarot_themes = [
    "card1",
    "card2",
    "card3"
]

def get_daily_cards(n=3):
    seed = int(hashlib.sha256(str(date.today()).encode()).hexdigest(), 16)
    random.seed(seed)
    return random.sample(tarot_themes, n)

if page == "Daily Horoscope":
    st.title("🌟 Daily Horoscope")
    if "user" in st.session_state and st.session_state.user:
        name = st.session_state.user.get("displayName", "there")
        st.markdown(f"👋 Hey **{name.capitalize()}**, welcome!")

    name = st.text_input("Your Name")
    birthdate = st.date_input("Your Birthdate", min_value=date(1950, 1, 1), max_value=date.today())
    
    if st.button("Reveal My Horoscope"):
        if name and birthdate:
            with st.spinner("Consulting the cosmic forces... ✨"):
                agent = HoroscopeAgent(name, birthdate.strftime("%Y-%m-%d"))
                lucky = agent.get_dynamic_lucky_elements()
                st.markdown("### 🍀 Lucky Elements of the Day")
                st.info(lucky)
                message = agent.get_interpreted_horoscope()
                st.write(message)
        else:
            st.warning("Please fill in all fields.")

elif page == "Compatibility Checker":
    st.title("Compatibility Checker")
    name = st.text_input("Your Name")
    birthdate = st.date_input("Your Birthdate", min_value=date(1950, 1, 1), max_value=date.today())
    other_sign = st.selectbox("Select partner's Zodiac sign", [
    "♈ Aries", "♉ Taurus", "♊ Gemini", "♋ Cancer",
    "♌ Leo", "♍ Virgo", "♎ Libra", "♏ Scorpio",
    "♐ Sagittarius", "♑ Capricorn", "♒ Aquarius", "♓ Pisces"
    ])
    
    if st.button("Check Compatibility"):
        if name and birthdate and other_sign:
            with st.spinner("Consulting the stars of relationships... 💫"):
                agent = HoroscopeAgent(name, birthdate.strftime("%Y-%m-%d"))
                compatibility = agent.get_compatibility_report(other_sign)
                st.subheader(f"❤️ Compatibility with {other_sign}")
                st.write(compatibility)
        else:
            st.warning("Please complete all fields.")

elif page == "Tarot Cards":
    st.title("🔮 Daily Tarot Reading")
    st.markdown("Each day reveals new energy. Tap a card to uncover your destiny.")
    
    cols = st.columns(3)
    drawn_themes = get_daily_cards()
    flipped = [False] * 3
    
    def encode_image_base64(path):
        with open(path, "rb") as img_file:
             return base64.b64encode(img_file.read()).decode()

    cols = st.columns(3)
    if "flipped" not in st.session_state:
        st.session_state.flipped = [False, False, False]

    back_images = ["card1.jpg", "card2.jpg", "card3.jpg"]
    card_image_path = "images/back.jpg"

    for i, col in enumerate(cols):
        with col:
            back_img_path = f"images/{back_images[i]}"
            if st.button(f"🔲 Flip Card {i+1}", key=f"flip_{i}"):
                for j in range(3):
                    st.session_state.flipped[j] = False
                st.session_state.flipped[i] = True

            if st.session_state.flipped[i]:
                reading = agent.get_tarot_reading(f"Card {i+1}")
                short_reading = "\n".join(reading.strip().split("\n")[:4])
                encoded_card = encode_image_base64(card_image_path)

                st.markdown(f"""
            <div style='position: relative; width: 150px; text-align: center;'>
                <img src='data:image/jpg;base64,{encoded_card}' width='150px' style='border-radius: 8px;' />
                <div style='position: absolute; top: 10px; left: 5px; right: 5px; 
                            color: black; font-weight: bold;
                            text-shadow: 0 0 3px black;
                            font-size: 13px;'>
                    {short_reading.replace('\n', '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            else:
              encoded_back = encode_image_base64(back_img_path)
              st.markdown(f"<img src='data:image/jpg;base64,{encoded_back}' width='150px'>", unsafe_allow_html=True)
