import pyrebase
import os

firebase_config = {
    "apiKey": os.environ.get("FIREBASE_API_KEY"),
    "authDomain": "financecontrolapp-cee78.firebaseapp.com",
    "projectId": "financecontrolapp-cee78",
    "storageBucket": "financecontrolapp-cee78.firebasestorage.app",
    "messagingSenderId": "795130918813",
    "appId": "1:795130918813:web:f82d9f452ff6b73dfae174",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
