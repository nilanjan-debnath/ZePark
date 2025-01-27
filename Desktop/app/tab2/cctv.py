from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QImage
import cv2


class CCVTPlayer(QWidget):
    def __init__(self, video_path):
        super().__init__()

        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)  # Open the video file

        # Check if the video was opened successfully
        if not self.cap.isOpened():
            print("Error: Could not open video.")
            return

        self.timer = QTimer(self)  # Timer for video playback

        # Create a QLabel to display the video
        self.video_label = QLabel("Loading video...")
        self.video_label.setScaledContents(True)

        # Layout for the video player
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        self.setLayout(layout)

        # Connect the timer to the update_frame function
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # Update frames every 33 ms (30 FPS)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert frame from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            aspect_ratio = 16 / 9  # Fixed 16:9 aspect ratio

            # Calculate new dimensions based on the 16:9 ratio
            new_w = w
            new_h = int(new_w / aspect_ratio)

            # If the height exceeds the available space, scale based on height
            if new_h > h:
                new_h = h
                new_w = int(new_h * aspect_ratio)

            # Resize the frame to maintain the 16:9 aspect ratio
            resized_frame = cv2.resize(rgb_frame, (new_w, new_h))

            bytes_per_line = 3 * new_w
            qimage = QImage(
                resized_frame.data, new_w, new_h, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qimage)
            self.video_label.setPixmap(pixmap)
        else:
            # Restart the video when it reaches the end
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()  # Release the video capture on close
        super().closeEvent(event)
