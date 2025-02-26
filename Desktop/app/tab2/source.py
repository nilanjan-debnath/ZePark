import json

# Constants for background videos
videos = [
    "video/video69crop-1.mp4",
    "video/video69crop-2.mp4",
    "video/video69crop-3.mp4",
    "video/video69crop-4.mp4",
    # "video/video69.mp4",
    # "video/video6.mp4",
    # " ",
]
rect_data = "data/rectangles.json"
slot_data = "data/slots.json"


def video(index):
    if index < count():
        return videos[index]
    else:
        print("Video isn't available")
        return " "


def count():
    return len(videos)


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
