# get firebase_admin by `sudo pip install firebase_admin`
import firebase_admin
import datetime
from flexsensor import read_flex
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate("/home/pi/mu_code/makeuoft2021/posfix/PosFix/cloud-fire-store/posfix-efa73-firebase-adminsdk-6d6mq-dc145efbb0.json")
firebase_admin.initialize_app(cred)

db = firestore.client()



for x in range(1,10000):
    back_curviture = read_flex()
    print(x)
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
    db.collection(u'posture-data').document(str(x)).set(data)
