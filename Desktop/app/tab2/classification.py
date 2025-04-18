from data import model

import cv2
import numpy as np


def park_check(area_image):
    resized_image = cv2.resize(area_image, (128, 128), interpolation=cv2.INTER_AREA)
    normalized_image = resized_image.astype(np.float32) / 255.0
    rgb_image = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2RGB)
    input_tensor = np.expand_dims(rgb_image, axis=0)
    probabilities = model.predict(input_tensor, verbose=0)[0]

    max_prob = max(probabilities)
    return max_prob
