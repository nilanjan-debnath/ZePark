import logging
import time
import cv2
import numpy as np
import threading

from data import model

images_dist = {}
acc_dist = {}
image_lock = threading.Lock()
acc_lock = threading.Lock()


def ml_worker():
    logging.info("MLProcess: Started")
    interpreter = model.get()
    while True:
        with image_lock:
            global images_dist
            slots_to_process = list(images_dist.keys())
            images_copy = {idx: images_dist[idx].copy() for idx in slots_to_process}

        for slot_no in slots_to_process:
            image = images_copy[slot_no]["image"]
            prev_time = images_copy[slot_no]["prev_time"]

            confidence = car_check(image, interpreter) * 100

            with acc_lock:
                acc_dist.update({slot_no: int(confidence)})
            # update_queue.put((slot_no, confidence, count))

            time_dif = time.time() - prev_time
            logging.info(f"MLProcess: {slot_no=} {time_dif=:.2f}s")

        time.sleep(0.01)


def car_check(area_image, interpreter) -> float:
    input_image_size = (256, 256)
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
    return probability
