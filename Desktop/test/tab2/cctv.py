from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QImage
import cv2


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.video_path = "video/video69crop-1.mp4"
        self.cap = cv2.VideoCapture(self.video_path)  # Open the video file
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
        self.timer.start(60)  # Update frames every 60 ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert frame from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qimage = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.video_label.setPixmap(pixmap)
        else:
            # Restart the video when it reaches the end
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def closeEvent(self, event):
        self.cap.release()  # Release the video capture on close
        super().closeEvent(event)
