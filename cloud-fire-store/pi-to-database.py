# get firebase_admin by `sudo pip install firebase_admin`
import firebase_admin
import datetime
import threading
from orientation import read_orientation
from flexsensor import read_flex
from firebase_admin import credentials
from firebase_admin import firestore
from quaternion import quaternion_to_euler

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
            if session != u'posture-data':
                print('meh')
            session = u'posture-data'
    callback_done.set()

doc_ref = db.collection(u'variables').document(u'start')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

# for naming documents
i=1

# default document
session = u'posture-data'
num_session = 0

# Total value for each parameter to calculate average
total_back = 0
total_orientation = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

while True:
    # flex sensor
    back_curviture = read_flex()
    if session != u'posture-data':
        total_back += back_curviture
    print(back_curviture)
    
    # imu sensor
    imu_sensors = read_orientation()
    orientation_0 = quaternion_to_euler(imu_sensors[0][0], imu_sensors[0][1], imu_sensors[0][2], imu_sensors[0][3])
    orientation_1 = quaternion_to_euler(imu_sensors[1][0], imu_sensors[1][1], imu_sensors[1][2], imu_sensors[1][3])
    orientation_2 = quaternion_to_euler(imu_sensors[2][0], imu_sensors[2][1], imu_sensors[2][2], imu_sensors[2][3])
    orientation_3 = quaternion_to_euler(imu_sensors[3][0], imu_sensors[3][1], imu_sensors[3][2], imu_sensors[3][3])
    orientation_matrix = [orientation_0, orientation_1, orientation_2, orientation_3]
    
    # session total for imu_sensor
    if session != u'posture-data':
        for i in range(4):
           # iterate through columns
           for j in range(4):
               total_orientation[i][j] = total_orientation[i][j] + orientation_matrix[i][j]
    
    
    # Warning from back sensor
    if back_curviture < 18:
        data = {
            u'message': "your leaning too far back",
        }
        db.collection(u'notification').document(u'notification').set(data)
    elif back_curviture > 26:
        data = {
            u'message': "your leaning too far in buddy",
        }
        db.collection(u'notification').document(u'notification').set(data)
    else:
        data = {
            u'message': "",
        }
        db.collection(u'notification').document(u'notification').set(data)
    
    data = {
        u'time': datetime.datetime.now(),
        u'back-curviture': back_curviture,
        u'neck': {
            u'orientation': imu_sensors[0]
        },
        u'rShoulder': {
            u'orientation': imu_sensors[1]
        },
        u'lShoulder': {
            u'orientation': imu_sensors[2]
        },
        u'back': {
            u'orientation': imu_sensors[3]
        },
    }
    
    # increment the number of data points in the session
    num_session += 1
    
    db.collection(u'test').document(str(datetime.datetime.now())).set(data)
