import json
import logging

slot_data = "app/data/resource/json/slots.json"
slot_dict = {"data": []}


def local_save():
    global slot_dict
    with open(slot_data, "w") as file:
        json.dump(slot_dict, file, indent=4)


def fetch_local():
    global slot_dict
    try:
        with open(slot_data, "r") as file:
            slot_dict = json.load(file)
            # print(all_rectangle_data)
    except FileNotFoundError:
        return
    except Exception as e:
        logging.critical(f"Error in get_slot_data DETAILS: {e}")


fetch_local()


def save_slot_data(data):
    slot_dict.update({"data": data})


def get_slot_data():
    return slot_dict.get("data")


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
                "emptied_time": " ",
                "confidence": "0.0",
                "pixel_count": 0,
            }
            slot_data.append(tmp)
    save_slot_data(data=slot_data)
