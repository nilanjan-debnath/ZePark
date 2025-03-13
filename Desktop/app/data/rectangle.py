from .parking_slot import create_slot_data
import json

rect_data = "app/data/resource/json/rectangles.json"


def get_rect_data():
    try:
        with open(rect_data, "r") as file:
            all_rectangle_data = json.load(file)
            # print(all_rectangle_data)
        return all_rectangle_data
    except FileNotFoundError:
        return {}


def save_rect_data(data):
    data = arrange_data(data=data)
    with open(rect_data, "w") as file:
        json.dump(data, file, indent=4)
    create_slot_data(data)


def arrange_data(data: dict):
    # print("data arrange")
    keys = list(data.keys())
    keys.sort()
    data = {i: data[i] for i in keys}
    count = 1
    for key in keys:
        for value in data[key]:
            value["index"] = count
            count += 1
    return data
