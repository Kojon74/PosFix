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
cred = credentials.Certificate(
    "/home/pi/mu_code/makeuoft2021/posfix/posfix-efa73-firebase-adminsdk-6d6mq-ca65a76d9e.json"
)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f"Received document snapshot: {doc.id}")
        global session
        if doc.get("isStarted"):
            session = "session_1"
        else:
            if session != "posture-data":
                print("meh")
            session = "posture-data"
    callback_done.set()


doc_ref = db.collection("variables").document("start")

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

# for naming documents
i = 1

# default document
session = "posture-data"
num_session = 0

# Total value for each parameter to calculate average
total_back = 0
total_orientation = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

while True:
    # flex sensor
    back_curviture = read_flex()
    if session != "posture-data":
        total_back += back_curviture
    print(back_curviture)

    # imu sensor
    imu_sensors = read_orientation()
    orientation_0 = quaternion_to_euler(
        imu_sensors[0][0], imu_sensors[0][1], imu_sensors[0][2], imu_sensors[0][3]
    )
    orientation_1 = quaternion_to_euler(
        imu_sensors[1][0], imu_sensors[1][1], imu_sensors[1][2], imu_sensors[1][3]
    )
    orientation_2 = quaternion_to_euler(
        imu_sensors[2][0], imu_sensors[2][1], imu_sensors[2][2], imu_sensors[2][3]
    )
    orientation_3 = quaternion_to_euler(
        imu_sensors[3][0], imu_sensors[3][1], imu_sensors[3][2], imu_sensors[3][3]
    )
    orientation_matrix = [orientation_0, orientation_1, orientation_2, orientation_3]

    # session total for imu_sensor
    if session != "posture-data":
        for i in range(4):
            # iterate through columns
            for j in range(4):
                total_orientation[i][j] = (
                    total_orientation[i][j] + orientation_matrix[i][j]
                )

    # Warning from back sensor
    if back_curviture < 18:
        data = {
            "message": "your leaning too far back",
        }
        db.collection("notification").document("notification").set(data)
    elif back_curviture > 26:
        data = {
            "message": "your leaning too far in buddy",
        }
        db.collection("notification").document("notification").set(data)
    else:
        data = {
            "message": "Good posture: Keep it up!",
        }
        db.collection("notification").document("notification").set(data)

    data = {
        "time": datetime.datetime.now(),
        "back-curviture": back_curviture,
        "neck": {"orientation": imu_sensors[0]},
        "rShoulder": {"orientation": imu_sensors[1]},
        "lShoulder": {"orientation": imu_sensors[2]},
        "back": {"orientation": imu_sensors[3]},
    }

    # increment the number of data points in the session
    num_session += 1

    db.collection("test").document(str(datetime.datetime.now())).set(data)
