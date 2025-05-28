import pyrebase

firebase_config = {
    "apiKey": "AIzaSyDynKQZw26yAqD1xx6zS9ho_9IWPE1sa68",
    "authDomain": "financecontrolapp-cee78.firebaseapp.com",
    "projectId": "financecontrolapp-cee78",
    "storageBucket": "financecontrolapp-cee78.firebasestorage.app",
    "messagingSenderId": "795130918813",
    "appId": "1:795130918813:web:f82d9f452ff6b73dfae174",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
