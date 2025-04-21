from .frame_process import current_frames, processed_frames
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap, QImage

import cv2
import time


class CCVTPlayer(QWidget):
    def __init__(self, index: int, video_path: str):
        super().__init__()
        self.index = index
        self.debugging = False
        self.video_path = video_path
        self.init_ui()
        self.prev_time = time.time()

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
            self.video_label.setPixmap(
                self.convert_frame_to_pixmap(frame, processed=True)
            )
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video

    def convert_frame_to_pixmap(self, frame, processed=True):
        """Convert OpenCV frame to QPixmap with rectangles overlay."""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if processed:
            current_frames[self.index] = frame
            if self.index in processed_frames:
                frame = processed_frames[self.index]

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
                return self.convert_frame_to_pixmap(frame, processed=False)
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
