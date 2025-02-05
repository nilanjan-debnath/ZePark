from tab2.source import get_rect_data

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap, QImage
import cv2
import numpy as np


class CCVTPlayer(QWidget):
    def __init__(self, index, video_path):
        super().__init__()
        self.index = index
        self.debugging = False
        self.video_path = video_path
        self.init_ui()

        self.cap = cv2.VideoCapture(self.video_path)
        if self.cap.isOpened():
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(33)  # Approx. 30 FPS
        else:
            self.video_label.setText(f"Error: Could not open {self.video_path}")

    def init_ui(self):
        """Initialize the UI for the video player."""
        self.video_label = QLabel("Loading...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setScaledContents(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing
        layout.addWidget(self.video_label)
        self.setLayout(layout)

    def update_frame(self):
        """Update the video frame."""
        ret, frame = self.cap.read()
        if ret:
            self.video_label.setPixmap(self.convert_frame_to_pixmap(frame))
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video

    def get_local_data(self):
        all_rectangle_data = get_rect_data()
        rectangle_data = all_rectangle_data.get(str(self.index))
        return rectangle_data if rectangle_data else []

    def process_image(self, frame):
        h, w, ch = frame.shape
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
        if self.debugging:
            frame = imgDilate

        rectangles = self.get_local_data()  # Get rectangle data
        for rect in rectangles:
            x = int(rect["x"] * w)
            y = int(rect["y"] * h)
            width = int(rect["width"] * w)
            height = int(rect["height"] * h)
            angle = rect["rotation"]  # Rotation angle

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

            # Crop the rotated area
            x_min, y_min = np.min(box_pts, axis=0)
            x_max, y_max = np.max(box_pts, axis=0)
            img_crop = img_rotated[y_min:y_max, x_min:x_max]

            count = cv2.countNonZero(
                cv2.cvtColor(img_crop, cv2.COLOR_RGB2GRAY)
            )  # Count non-zero pixels
            color = (
                (255, 0, 0) if count > 900 else (0, 255, 0)
            )  # Determine parking status, Blue for occupied, Green for free

            cv2.polylines(
                frame, [box_pts], isClosed=True, color=color, thickness=2
            )  # Draw rotated rectangle
            cv2.putText(
                frame,
                f"{count}",
                (x + 5, y + height - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2,
            )  # added pixel count
            cv2.putText(
                frame,
                f"{rect['index']}",
                (x + width // 2, y + height // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2,
            )  # added index

        return frame

    def convert_frame_to_pixmap(self, frame, no_process=False):
        """Convert OpenCV frame to QPixmap with rectangles overlay."""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if not no_process:
            frame = self.process_image(frame)

        # Convert to QPixmap
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(image)

    def get_current_frame(self):
        """Capture the current frame from the video and return it as a QPixmap."""
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return self.convert_frame_to_pixmap(frame, no_process=True)
        return None

    def set_video_size(self, width, height):
        """Resize the video display area while maintaining a 16:9 aspect ratio."""
        aspect_height = width * 9 // 16
        if aspect_height > height:  # Adjust if height exceeds the allowed limit
            aspect_height = height
            width = aspect_height * 16 // 9
        self.video_label.setFixedSize(width, aspect_height)

    def closeEvent(self, event):
        """Release resources on close."""
        if self.cap.isOpened():
            self.cap.release()
        super().closeEvent(event)
