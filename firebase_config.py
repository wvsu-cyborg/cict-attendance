# firebase_config.py

import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("attendance-system-72efe-firebase-adminsdk-mv42z-e9582c40a7.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://attendance-system-72efe-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# Get a reference to the database
def get_db_reference():
    return db.reference()
