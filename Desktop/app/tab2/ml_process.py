from data import get_slot_data, save_slot_data
from data import model
from tab1 import ui_updates

import logging
import queue
import datetime
import cv2
import numpy as np


ml_queue = queue.Queue()


def car_check(area_image) -> bool:
    input_image_size = (256, 256)

    interpreter = model.get()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_shape = input_details[0]["shape"]
    input_index = input_details[0]["index"]

    output_index = output_details[0]["index"]

    rgb_image = cv2.cvtColor(area_image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(
        rgb_image, input_image_size, interpolation=cv2.INTER_AREA
    )
    img_array = resized_image.astype(np.float32) / 255.0
    input_tensor = np.expand_dims(img_array, axis=0)

    if not np.array_equal(input_tensor.shape, input_shape):
        print(
            f"Error: Input data shape {input_tensor.shape} does not match model input shape {input_shape}"
        )
        exit()

    interpreter.set_tensor(input_index, input_tensor)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_index)
    probability = output_data[0][0]
    return True if probability > 0.5 else False


def ml_worker():
    logging.info("MLProcess: Started")
    while True:
        if ml_queue.not_empty:
            slot_no, count, img = ml_queue.get()
            parked = False
            confidence = 0.0
            if count > 1500:
                parked = True
                # if car_check(img):
                #     parked = True
            if parked:
                update_parking(slot_no, confidence, count)
            else:
                clear_parking(slot_no, confidence, count)

            ml_queue.task_done()
            logging.info(f"MLProcess: {slot_no=} {count=}")


def update_parking(index, confidence, pixel_count):
    slots = get_slot_data()
    if slots[index - 1]["status"] != 2:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slots[index - 1]["status"] = 2
        slots[index - 1]["parking_time"] = time
        slots[index - 1]["emptied_time"] = " "
        slots[index - 1]["confidence"] = f"{confidence}"
        slots[index - 1]["pixel_count"] = pixel_count
        save_slot_data(data=slots)

        ui_updates.put((index, 2))


def clear_parking(index, confidence, pixel_count):
    slots = get_slot_data()
    if slots[index - 1]["status"] != 0:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slots[index - 1]["status"] = 0
        slots[index - 1]["booking_time"] = " "
        slots[index - 1]["parking_time"] = " "
        slots[index - 1]["emptied_time"] = time
        slots[index - 1]["confidence"] = f"{confidence}"
        slots[index - 1]["pixel_count"] = pixel_count
        save_slot_data(data=slots)

        ui_updates.put((index, 0))
