from data import get_slot_data, save_slot_data
from tab1 import ui_updates
import logging
import queue
import datetime
# import cv2
# import numpy as np
# from data import model

ml_queue = queue.Queue()


# def park_check(area_image):
#     resized_image = cv2.resize(area_image, (128, 128), interpolation=cv2.INTER_AREA)
#     normalized_image = resized_image.astype(np.float32) / 255.0
#     rgb_image = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2RGB)
#     input_tensor = np.expand_dims(rgb_image, axis=0)
#     bi_model = model.get()
#     probabilities = bi_model.predict(input_tensor, verbose=0)[0]

#     max_prob = max(probabilities)
#     return max_prob


def ml_worker():
    logging.info("MLProcess: Started")
    while True:
        if ml_queue.not_empty:
            slot_no, count, img = ml_queue.get()
            parked = False
            confidence = 0.0
            if count > 1500:
                parked = True
                # confidence = park_check(img)
                # if confidence > 0.5:
                #     parked = True

            if parked:
                update_parking(slot_no, confidence)
            else:
                clear_parking(slot_no, confidence)

            ml_queue.task_done()
            logging.info(f"MLProcess: {slot_no=} {count=}")


def update_parking(index, confidence):
    slots = get_slot_data()
    if slots[index - 1]["status"] != 2:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slots[index - 1]["status"] = 2
        slots[index - 1]["parking_time"] = time
        slots[index - 1]["emptied_time"] = " "
        slots[index - 1]["confidence"] = f"{confidence}"
        save_slot_data(data=slots)

        ui_updates.put((index, 2))


def clear_parking(index, confidence):
    slots = get_slot_data()
    if slots[index - 1]["status"] != 0:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slots[index - 1]["status"] = 0
        slots[index - 1]["booking_time"] = " "
        slots[index - 1]["parking_time"] = " "
        slots[index - 1]["emptied_time"] = time
        slots[index - 1]["confidence"] = f"{confidence}"
        save_slot_data(data=slots)

        ui_updates.put((index, 0))
