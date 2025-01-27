from tab2.cctv import CCVTPlayer
import source

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
import math


class Tab2Content(QWidget):
    def __init__(self):
        super().__init__()

        self.load_stylesheet()
        self.row_size = 0
        self.cctv_windows = []

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.create_cctv_window())

        self.setLayout(main_layout)

    def create_cctv_window(self):
        layout = QVBoxLayout()
        video_count = source.count()
        if video_count > 0:
            self.row_size = math.ceil(math.sqrt(video_count))
            c = 0
            for i in range(self.row_size):
                row = QHBoxLayout()
                for j in range(self.row_size):
                    if c == video_count:
                        break
                    cctv = CCVTPlayer(source.video(c))
                    c += 1
                    row.addWidget(cctv)
                    self.cctv_windows.append(cctv)
                layout.addLayout(row)
        return layout

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.row_size > 0:
            width = int(self.width() / self.row_size) - 30
            height = int(self.height() / self.row_size) - 30

            new_height = int(width / 16 * 9)

            if new_height > height:
                new_height = height
                new_width = int(height * 16 / 9)
            else:
                new_width = width
            for cctv in self.cctv_windows:
                cctv.set_video_size(new_width, new_height)

    def current_window_image(self, index):
        """Retrieve the current frame from a specific CCTV window."""
        if 0 <= index < len(self.cctv_windows):
            return self.cctv_windows[index].get_current_frame()
        print(f"Error: Invalid index {index}.")
        return None

    def load_stylesheet(self):
        """Load and apply a stylesheet from an external file."""
        try:
            with open("app/style/tab2.css", "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            print("Error: Stylesheet file not found.")
