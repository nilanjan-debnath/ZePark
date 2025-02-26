import firebase_admin
from firebase_admin import credentials, firestore, db

ID = "RThu5aFTHmxbqJ7zXf0r"  # 69 slots
# ID="Y5wbaFy5YnfFJE8ohgHZ"  #6 slots
DATABASE_URL = "https://par-king-car-default-rtdb.firebaseio.com/"
# DATABASE_URL="https://parkar-808f7-default-rtdb.firebaseio.com/" #shivam

cred = credentials.Certificate("par-king-car-firebase-adminsdk.json")
# cred = credentials.Certificate('parkar-firebase-adminsdk.json') # shivam
databaseURL = "https://par-king-car-default-rtdb.firebaseio.com/"
default_app = firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})
storedb = firestore.client()


def get_provider_details() -> dict:
    provider = storedb.collection("providers").document(ID).get().to_dict()
    return provider


def set_provider_details(data: dict):
    storedb.collection("providers").document(ID).set(data)


def get_grid_details() -> dict:
    grid = storedb.collection("grids").document(ID).get().to_dict()
    return grid


def set_grid_details(data: dict):
    storedb.collection("grids").document(ID).set(data)


def get_parking_details() -> list:
    data = db.reference(ID).get()
    return data


def set_parking_details(data: list):
    db.reference(ID).set(data)


def update_parking_details(index: int, data: dict):
    db.reference(f"{ID}/{str(index)}").update(data)


def update_spot_count(count: int):
    storedb.collection("providers").document(ID).update({"available_slots": count})
