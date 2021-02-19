# Write your code here :-)
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate("/home/pi/mu_code/makeuoft2021/posfix/PosFix/cloud-fire-store/posfix-efa73-firebase-adminsdk-6d6mq-dc145efbb0.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection('users').document('alovelace')
doc_ref.set({
    'first': 'Ada',
    'last': 'Lovelace',
    'born': 1815
})
