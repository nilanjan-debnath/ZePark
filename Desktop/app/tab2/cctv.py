from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap, QImage
import cv2


class CCVTPlayer(QWidget):
    def __init__(self, video_path):
        super().__init__()

        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)  # Open the video file

        # Check if the video was opened successfully
        if not self.cap.isOpened():
            print(f"Error: Could not open video: {video_path}")
            return

        self.timer = QTimer(self)  # Timer for video playback

        # Create a QLabel to display the video
        self.video_label = QLabel("Loading video...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setScaledContents(True)

        # Layout for the video player
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        self.setLayout(layout)

        # Connect the timer to the update_frame function
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # Update frames every ~33 ms (30 FPS)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            pixmap = self.convert_frame_to_pixmap(frame)
            self.video_label.setPixmap(pixmap)
        else:
            # Restart the video when it reaches the end
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def convert_frame_to_pixmap(self, frame):
        """Convert a BGR frame from OpenCV to QPixmap."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qimage = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def get_current_frame(self):
        """Capture the current frame from the video and return it as a QPixmap."""
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return self.convert_frame_to_pixmap(frame)
        return None

    def set_video_size(self, width, height):
        """Resize the video display area while maintaining the aspect ratio."""
        self.video_label.setMaximumSize(width, height)

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()  # Release the video capture on close
        super().closeEvent(event)
