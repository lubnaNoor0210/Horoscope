import firebase_admin
from firebase_admin import credentials, auth

# Load credentials
cred = credentials.Certificate("firebase_key.json")

# Initialize the Firebase app
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
