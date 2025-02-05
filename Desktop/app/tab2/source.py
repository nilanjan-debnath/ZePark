import json

# Constants for background videos
videos = [
    "video/video69crop-1.mp4",
    "video/video69crop-2.mp4",
    "video/video69crop-3.mp4",
    # "video/video69crop-4.mp4",
    # "video/video69.mp4",
    "video/video6.mp4",
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
    with open(rect_data, "w") as file:
        json.dump(data, file, indent=4)


def arrange_data():
    print("data arrange")
    data = get_rect_data()
    keys = list(data.keys())
    keys.sort()
    data = {i: data[i] for i in keys}
    count = 1
    for key in keys:
        for value in data[key]:
            value["index"] = count
            count += 1
    # create_slot_data(count=count - 1)
    save_rect_data(data=data)


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


def create_slot_data(count):
    data = [
        {
            "slot_no": x,
            "status": 0,
            "user_name": " ",
            "car_no": " ",
            "booking_time": " ",
            "parking_time": " ",
        }
        for x in range(count)
    ]
    save_slot_data(data=data)


arrange_data()
