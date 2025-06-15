import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = st.secrets["FIREBASE_WEB_API_KEY"]

FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
FIREBASE_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
FIREBASE_UPDATE_PROFILE_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={API_KEY}"
FIREBASE_LOOKUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={API_KEY}"

def get_zodiac_sign(birthdate_str):
    date = datetime.strptime(birthdate_str, "%Y-%m-%d")
    day, month = date.day, date.month
    if (month == 3 and day >= 21) or (month == 4 and day <= 19): return "aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20): return "taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20): return "gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22): return "cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22): return "leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22): return "virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22): return "libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21): return "scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21): return "sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19): return "capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18): return "aquarius"
    else: return "pisces"

def signup_user(name, email, password, birthdate):
    try:
        signup_payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        signup_response = requests.post(FIREBASE_SIGNUP_URL, json=signup_payload)

        if signup_response.status_code != 200:
            return {"success": False, "message": signup_response.json()["error"]["message"]}

        id_token = signup_response.json()["idToken"]

        update_payload = {
            "idToken": id_token,
            "displayName": name,
            "returnSecureToken": True
        }
        update_response = requests.post(FIREBASE_UPDATE_PROFILE_URL, json=update_payload)

        if update_response.status_code != 200:
            return {"success": False, "message": "Signup succeeded but failed to set name."}

        lookup_payload = {"idToken": id_token}
        lookup_response = requests.post(FIREBASE_LOOKUP_URL, json=lookup_payload)

        if lookup_response.status_code != 200:
            return {"success": False, "message": "Profile lookup failed."}

        user_info = lookup_response.json()["users"][0]  # ✅ FIXED
        user_info["idToken"] = id_token
        user_info["zodiac"] = get_zodiac_sign(birthdate)

        return {"success": True, "data": user_info}

    except Exception as e:
        return {"success": False, "message": str(e)}


def login_user(email, password):
    try:
        login_payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        login_response = requests.post(FIREBASE_SIGNIN_URL, json=login_payload)

        if login_response.status_code != 200:
            return {"success": False, "message": login_response.json()["error"]["message"]}

        id_token = login_response.json()["idToken"]

        lookup_payload = {"idToken": id_token}
        lookup_response = requests.post(FIREBASE_LOOKUP_URL, json=lookup_payload)

        if lookup_response.status_code != 200:
            return {"success": False, "message": "Login succeeded, but profile fetch failed."}

        user = lookup_response.json()["users"][0]

        user_info = {
            "email": user.get("email", "N/A"),
            "localId": user.get("localId", "N/A"),
            "displayName": user.get("displayName", "N/A"),
            "idToken": id_token
        }

        return {"success": True, "data": user_info}

    except Exception as e:
        return {"success": False, "message": str(e)}
