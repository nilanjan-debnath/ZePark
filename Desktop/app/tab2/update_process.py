import queue
import time
import datetime

from tab1 import ui_updates
from data import get_slot_data, save_slot_data

update_queue = queue.Queue()


def update_worker():
    while True:
        if update_queue.not_empty:
            slot_no, confidence, count = update_queue.get()

            if confidence > 50:
                update_parking(slot_no, confidence, count)
            else:
                clear_parking(slot_no, confidence, count)

            update_queue.task_done()

        time.sleep(0.01)


def update_parking(index, confidence, pixel_count):
    slots = get_slot_data()
    slots[index - 1]["confidence"] = f"{confidence}"
    slots[index - 1]["pixel_count"] = pixel_count
    if slots[index - 1]["status"] != 2:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slots[index - 1]["status"] = 2
        slots[index - 1]["parking_time"] = time
        slots[index - 1]["emptied_time"] = " "

        ui_updates.put((index, 2))

        save_slot_data(data=slots)


def clear_parking(index, confidence, pixel_count):
    slots = get_slot_data()
    slots[index - 1]["confidence"] = f"{confidence}"
    slots[index - 1]["pixel_count"] = pixel_count
    if slots[index - 1]["status"] != 0:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slots[index - 1]["status"] = 0
        slots[index - 1]["booking_time"] = " "
        slots[index - 1]["parking_time"] = " "
        slots[index - 1]["emptied_time"] = time

        ui_updates.put((index, 0))

        save_slot_data(data=slots)
