import streamlit as st
import os
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import date

load_dotenv()
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

class HoroscopeAgent:
    def __init__(self, name: str, birthdate: str):
        self.name = name
        self.birthdate = birthdate
        self.zodiac_sign = self.get_zodiac_sign()

    def get_zodiac_sign(self):
        date = datetime.strptime(self.birthdate, "%Y-%m-%d")
        day, month = date.day, date.month

        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "aquarius"
        else:
            return "pisces"

    def get_interpreted_horoscope(self, timeframe="Today"):
        today = datetime.today().strftime("%A, %B %d, %Y")
        prompt = f"""
You are a compassionate and insightful astrology expert.

Generate a {timeframe.lower()} horoscope in friendly and clear language for a person named {self.name}, who is a {self.zodiac_sign.capitalize()}.

Begin with this headline:
## 🔮 Horoscope for {self.zodiac_sign.capitalize()} – {timeframe} ({today})
Mention that today is {today.split(',')[0]} in the opening line.

Then write four detailed sections:

### ❤️ Love  
Give a 4–5 line paragraph. Describe current energies in their love life — is it a good time to open up, reflect, or resolve tension? Be honest and warm.

### 💼 Work  
Give a 4–5 line paragraph. Mention possible opportunities or mental blocks. Talk about productivity, creativity, or collaboration. Offer a grounded perspective.

### 💭 Emotions  
Write 4–5 lines on emotional patterns — what might they feel or struggle with today? Encourage self-awareness. Include validation or a simple reminder.

### 🔮 Advice  
End with a 2–3 line paragraph offering a practical tip or insight based on the overall tone of the day. Don't be vague — aim for usefulness.

Keep the tone empathetic, modern, and realistic. Don't use rhymes, clichés, or generic "good vibes". Avoid spiritual jargon — be human and thoughtful.
"""

        response = model.generate_content(prompt)
        return response.text
    
    def get_dynamic_lucky_elements(self):
        prompt = f"""
        Generate lucky elements for today ({datetime.now().strftime('%B %d, %Y')}) for the zodiac sign {self.zodiac_sign.capitalize()}. 
        Include:
        - Lucky color
        - Lucky number
        - Lucky stone or crystal
        Format it nicely and explain each in 1–2 lines.
        """
        response = model.generate_content(prompt)
        return response.text


    def get_compatibility_report(self, other_sign: str):
        today = datetime.today().strftime("%A, %B %d, %Y")
        prompt = f"""
You are a zodiac compatibility expert.
Generate a fun and practical compatibility report for:

- Person 1: {self.name}, born on {self.birthdate}, zodiac sign: {self.zodiac_sign.capitalize()}
- Person 2: Sign: {other_sign}

📅 Date: {today}

- The response must be exactly two paragraphs.
- Each paragraph should have 5 lines.
- Add percentage compatibility in last as a third paragraph.
- Do not include bullet points or lists.

Use clear, friendly language.
"""
        response = model.generate_content(prompt)
        return response.text
    
    def get_tarot_reading(self, theme: str):
      today = date.today().strftime("%B %d, %Y")
      prompt = f"""
You are a mystical tarot expert.

On {today}, the seeker has drawn the card: **{theme}**.

Write a short and simple tarot reading in plain english:
- keep it 4 lines only
- Each line should be short and easy to understand
- Based on the meaning of the card: {theme}

Do not include the user's name or birthdate. This reading is for all.

Avoid spiritual metaphors. Be clear, friendly, and encouraging.
"""
      response = model.generate_content(prompt)
      return response.text








