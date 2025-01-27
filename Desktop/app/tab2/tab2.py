from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
import math
from tab2.cctv import CCVTPlayer

videos = [
    "video/video69crop-1.mp4",
    "video/video69crop-2.mp4",
    "video/video69crop-3.mp4",
    "video/video69crop-4.mp4",
]


class Tab2Content(QWidget):
    def __init__(self):
        super().__init__()

        self.load_stylesheet()

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.create_background_buttons())

        self.setLayout(main_layout)

    def create_background_buttons(self):
        layout = QVBoxLayout()
        video_count = len(videos)
        if video_count > 0:
            num = math.ceil(math.sqrt(video_count))
            c = 0
            for i in range(num):
                row = QHBoxLayout()
                for j in range(num):
                    if c == video_count:
                        break
                    cctv = CCVTPlayer(videos[c])
                    c += 1
                    row.addWidget(cctv)
                layout.addLayout(row)
        return layout

    def load_stylesheet(self):
        """Load and apply a stylesheet from an external file."""
        try:
            with open("app/style/tab2.css", "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            print("Error: Stylesheet file not found.")
