from data import get_slot_data, save_slot_data
from .classification import park_check
import threading
import queue
import datetime

ml_queue = queue.Queue()


def ml_worker():
    while True:
        slot_no, count, img = ml_queue.get()
        parked = False
        confidence = 0.0
        if count > 1500:
            confidence = park_check(img)
            if confidence > 0.5:
                parked = True

        if parked:
            update_parking(slot_no, count, confidence)
        else:
            clear_parking(slot_no, count, confidence)
        # logging.info(f"Slot No. {slot_no} | Confidence: {confidence} | Pixel count: {count}")
        ml_queue.task_done()


def threading_start():
    threading.Thread(target=ml_worker, daemon=True).start()


def update_parking(index, count, confidence):
    slots = get_slot_data()
    if slots[index - 1]["status"] == 0:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slots[index - 1]["status"] = 2
        slots[index - 1]["parking_time"] = time
        slots[index - 1]["emptied_time"] = " "
        slots[index - 1]["pixel_count"] = count
        slots[index - 1]["confidence"] = f"{confidence}"
        save_slot_data(data=slots)


def clear_parking(index, count, confidence):
    slots = get_slot_data()
    if slots[index - 1]["status"] != 0:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slots[index - 1]["status"] = 0
        slots[index - 1]["booking_time"] = " "
        slots[index - 1]["parking_time"] = " "
        slots[index - 1]["emptied_time"] = time
        slots[index - 1]["pixel_count"] = count
        slots[index - 1]["confidence"] = f"{confidence}"
        save_slot_data(data=slots)
