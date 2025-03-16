import json

slot_data = "app/data/resource/json/slots.json"


def save_slot_data(data):
    with open(slot_data, "w") as file:
        json.dump(data, file, indent=4)


def get_slot_data():
    try:
        with open(slot_data, "r") as file:
            all_rectangle_data = json.load(file)
            # print(all_rectangle_data)
        return all_rectangle_data
    except FileNotFoundError:
        return {}


def create_slot_data(data: dict):
    slot_data = []
    keys = list(data.keys())
    for key in keys:
        for slot in data.get(key):
            tmp = {
                "cctv_cam": key,
                "slot_no": slot["index"],
                "status": 0,
                "user_name": " ",
                "car_no": " ",
                "booking_time": " ",
                "parking_time": " ",
            }
            slot_data.append(tmp)
    save_slot_data(data=slot_data)
