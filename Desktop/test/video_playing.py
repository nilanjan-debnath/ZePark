import sys
import cv2
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer


class VideoPlayer(QWidget):
    def __init__(self, video_path):
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player with Tabs")
        self.setGeometry(200, 200, 800, 600)

        # Create a QTabWidget
        self.tab_widget = QTabWidget()

        # Create two tabs
        self.tab1 = VideoPlayer("sample_video.mp4")  # Replace with your video file path
        self.tab2 = QWidget()

        # Set up tab2 content
        tab2_layout = QVBoxLayout()
        tab2_label = QLabel("This is Tab 2")
        tab2_layout.addWidget(tab2_label)
        self.tab2.setLayout(tab2_layout)

        # Add tabs to the QTabWidget
        self.tab_widget.addTab(self.tab1, "Video Player")
        self.tab_widget.addTab(self.tab2, "Tab 2")

        # Set the central widget
        self.setCentralWidget(self.tab_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
