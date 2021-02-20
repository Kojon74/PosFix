# get firebase_admin by `sudo pip install firebase_admin`
import firebase_admin
import datetime
import threading
from flexsensor import read_flex
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate("/home/pi/mu_code/makeuoft2021/posfix/posfix-efa73-firebase-adminsdk-6d6mq-ca65a76d9e.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.id}')
        global session
        if doc.get('isStarted'):
            session = u'session_1'
        else:
            session = u'posture-data'
    callback_done.set()

doc_ref = db.collection(u'variables').document(u'start')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

i=1
session = u'posture-data'

while True:
    back_curviture = read_flex()
    print(back_curviture)
    
    # Warning from back sensor
    if back_curviture < 18:
        data = {
            u'message': "your leaning too far back",
        }
        db.collection(u'notification').document(u'notification_2').set(data)
    if back_curviture < 26:
        data = {
            u'message': "your leaning too far in buddy",
        }
        db.collection(u'notification').document(u'notification_2').set(data)
    
    data = {
        u'time': datetime.datetime.now(),
        u'back-curviture': back_curviture,
        u'neck': {
            u'position':[1, 1, 1],
            u'orientation': [1,1,1,1]
        },
        u'rShoulder': {
            u'position':[1, 1, 1],
            u'orientation': [1,1,1,1]
        },
        u'lShoulder': {
            u'position':[1, 1, 1],
            u'orientation': [1,1,1,1]        },
        u'back': {
            u'position':[1, 1, 1],
            u'orientation': [1,1,1,1]
        },
    }
    print(session)
    db.collection(session).document(str(datetime.datetime.now())).set(data)
