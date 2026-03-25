import firebase_admin
from firebase_admin import credentials, firestore
import os

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            os.path.join(os.path.dirname(__file__), '..', 'serviceAccountKey.json')
        )
        firebase_admin.initialize_app(cred)

    return firestore.client()

db = init_firebase()