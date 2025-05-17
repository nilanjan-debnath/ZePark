import logging
import time
import cv2
import numpy as np
import threading

from .update_process import update_queue

# from .ml_process import images_dist, image_lock, acc_dist, acc_lock
from data import get_rect_data, get_slot_data

current_frames = {}
processed_frames = {}
frame_lock = threading.Lock()
processed_lock = threading.Lock()


def frame_worker():
    logging.info("FrameProcess: Started")
    while True:
        with frame_lock:
            indices_to_process = list(current_frames.keys())
            frames_copy = {
                idx: current_frames[idx].copy() for idx in indices_to_process
            }

        for index in indices_to_process:
            frame = frames_copy[index]  # Use the copied frame
            processed_frame = process_image(frame, cctv_index=index)
            with processed_lock:  # Acquire lock to update processed_frames
                processed_frames[index] = processed_frame
            # logging.info(f"FrameProcess: {index=}") # Consider reducing frequency

        time.sleep(0.01)


def get_local_data(cctv_index):
    all_rectangle_data = get_rect_data()
    rectangle_data = all_rectangle_data.get(str(cctv_index))
    return rectangle_data if rectangle_data else []


def process_image(frame, cctv_index, debugging=False):
    h, w, ch = frame.shape
    # imgOrg = frame
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16
    )
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    imgDilate = cv2.cvtColor(imgDilate, cv2.COLOR_GRAY2RGB)

    # take the imgDilate as the frame for checking the processed image
    if debugging:
        frame = imgDilate

    rectangles = get_local_data(cctv_index)
    slots = get_slot_data()
    for rect in rectangles:
        x = int(rect["x"] * w)
        y = int(rect["y"] * h)
        width = int(rect["width"] * w)
        height = int(rect["height"] * h)
        angle = rect["rotation"]

        rect_center = (
            x + width // 2,
            y + height // 2,
        )  # Define center of the rectangle
        rect_box = (
            (rect_center[0], rect_center[1]),
            (width, height),
            angle,
        )  # Create rotated bounding box
        box_pts = cv2.boxPoints(rect_box)  # Get corner points
        box_pts = np.array(box_pts, np.int32)  # Convert to integer

        # Rotate image and extract region
        rotation_matrix = cv2.getRotationMatrix2D(rect_center, angle, 1.0)
        img_rotated = cv2.warpAffine(imgDilate, rotation_matrix, (w, h))
        # imgOrg_rotated = cv2.warpAffine(imgOrg, rotation_matrix, (w, h))

        # Crop the rotated area
        x_min, y_min = np.min(box_pts, axis=0)
        x_max, y_max = np.max(box_pts, axis=0)

        # Ensure cropping remains within image boundaries
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(w, x_max)
        y_max = min(h, y_max)

        img_crop = img_rotated[y_min:y_max, x_min:x_max]
        # imgOrg_crop = imgOrg_rotated[y_min:y_max, x_min:x_max]

        if img_crop.size == 0:
            continue  # Skip if the cropped region is invalid

        # count = int(slots[rect["index"] - 1]['pixel_count'])
        count = cv2.countNonZero(
            cv2.cvtColor(img_crop, cv2.COLOR_RGB2GRAY)
        )  # Count non-zero pixels

        # with image_lock:
        #     images_dist[rect["index"]] = {
        #         "image": imgOrg_crop,
        #         "prev_time": time.time(),
        #     }
        # with acc_lock:
        #     confidence = acc_dist.get(rect["index"])

        confidence = 99
        if confidence is None:
            continue

        frame = add_text(frame, box_pts, rect, count, confidence, slots)
        update_queue.put((rect["index"], confidence, count))

    return frame


def add_text(frame, box_pts, rect, pixel_count, confidence, slots):
    h, w, ch = frame.shape
    x = int(rect["x"] * w)
    y = int(rect["y"] * h)
    width = int(rect["width"] * w)
    height = int(rect["height"] * h)
    index = rect["index"]

    if pixel_count > 1500:
        color = (255, 0, 0)
        # update_parking(index, confidence, pixel_count)
    elif slots[index - 1]["status"] == 1:
        color = (0, 0, 255)
    else:
        color = (0, 255, 0)
        # clear_parking(index, confidence, pixel_count)

    cv2.polylines(
        frame, [box_pts], isClosed=True, color=color, thickness=2
    )  # Draw rotated rectangle
    cv2.putText(
        frame,
        f"{confidence}",
        (x + width - 30, y + 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        2,
    )  # added pixel count
    cv2.putText(
        frame,
        f"{pixel_count}",
        (x + 5, y + height - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        2,
    )  # added pixel count
    cv2.putText(
        frame,
        f"{index}",
        (x + width // 2, y + height // 2),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        2,
    )  # added index
    return frame
