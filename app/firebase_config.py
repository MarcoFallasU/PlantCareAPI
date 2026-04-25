import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def init_firebase():
    if not firebase_admin._apps:
        firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
        if firebase_json:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
        else:
            cred = credentials.Certificate(
                os.path.join(os.path.dirname(__file__), '..', 'serviceAccountKey.json')
            )
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()