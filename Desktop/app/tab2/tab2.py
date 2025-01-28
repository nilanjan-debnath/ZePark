from tab2.cctv import CCVTPlayer
from tab2 import source
import math
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class Tab2Content(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_view = True
        self.selected_window = 0  # Default to the first CCTV window
        self.cctv_windows = []

        # Initialize the UI components
        self.load_stylesheet()
        self.create_cctv_windows()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.create_control_buttons())

        self.cctv_layout = QVBoxLayout()
        main_layout.addLayout(self.cctv_layout)

        self.setLayout(main_layout)
        self.update_cctv_view()

    def create_control_buttons(self):
        """Create control buttons for grid and single views."""
        layout = QHBoxLayout()

        switch_view_button = QPushButton("Switch View")
        switch_view_button.setObjectName("switch_view_button")
        switch_view_button.clicked.connect(self.toggle_view_mode)
        layout.addWidget(switch_view_button)

        for i in range(source.count()):
            button = QPushButton(f"CCTV {i + 1}")
            button.setObjectName(f"cctv_button_{i}")
            button.clicked.connect(lambda _, idx=i: self.select_cctv_window(idx))
            layout.addWidget(button)

        return layout

    def toggle_view_mode(self):
        """Switch between grid and single view modes."""
        self.grid_view = not self.grid_view
        self.update_cctv_view()

    def update_cctv_view(self):
        """Update the CCTV display based on the current mode."""
        self.clear_layout(self.cctv_layout)

        if self.grid_view:
            self.cctv_layout.addLayout(self.create_grid_layout())
        else:
            self.cctv_layout.addLayout(self.create_single_view_layout())

        self.resize_windows()

    def create_grid_layout(self):
        """Generate a grid layout for CCTV windows."""
        layout = QVBoxLayout()
        self.row_size = math.ceil(math.sqrt(len(self.cctv_windows)))
        index = 0

        for _ in range(self.row_size):
            row = QHBoxLayout()
            for _ in range(self.row_size):
                if index >= len(self.cctv_windows):
                    break
                row.addWidget(self.cctv_windows[index])
                index += 1
            layout.addLayout(row)

        return layout

    def create_single_view_layout(self):
        """Generate a layout for single-view mode."""
        layout = QHBoxLayout()

        # Add the selected window (takes 75% of the width)
        layout.addWidget(self.cctv_windows[self.selected_window], stretch=3)

        # Add the smaller previews (stacked vertically, takes 25% of the width)
        side_layout = QVBoxLayout()
        for i, cctv_window in enumerate(self.cctv_windows):
            if i != self.selected_window:
                side_layout.addWidget(cctv_window)
        side_layout.setAlignment(Qt.AlignTop)
        layout.addLayout(side_layout, stretch=1)

        return layout

    def create_cctv_windows(self):
        """Initialize CCTV windows from the source."""
        self.cctv_windows = [
            CCVTPlayer(index=i, video_path=source.video(i))
            for i in range(source.count())
        ]

    def select_cctv_window(self, index):
        """Set the selected CCTV window for single view."""
        if 0 <= index < len(self.cctv_windows):
            self.selected_window = index
            self.update_cctv_view()

    def clear_layout(self, layout):
        """Clear all widgets from a layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_stylesheet(self):
        """Load and apply the stylesheet."""
        try:
            with open("app/style/tab2.css", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Error: Stylesheet file not found.")

    def resizeEvent(self, event):
        """Handle resizing to adjust CCTV sizes."""
        super().resizeEvent(event)
        self.resize_windows()

    def resize_windows(self):
        width, height = self.width(), self.height()

        if self.grid_view:
            # Calculate grid cell size while maintaining a 16:9 ratio
            cell_width = width // self.row_size
            cell_height = cell_width * 9 // 16
            if (
                cell_height * self.row_size > height
            ):  # Adjust if height exceeds available space
                cell_height = height // self.row_size
                cell_width = cell_height * 16 // 9

            for cctv in self.cctv_windows:
                cctv.set_video_size(cell_width, cell_height)
        else:
            # Single window view
            main_width = int(width * 0.75)  # Selected window takes 75% width
            main_height = min(main_width * 9 // 16, height)  # Maintain 16:9 ratio

            self.cctv_windows[self.selected_window].set_video_size(
                main_width, main_height
            )

            # Set sizes for the other windows
            side_width = width - main_width  # Remaining 25% width
            side_height = side_width * 9 // 16
            for i, cctv in enumerate(self.cctv_windows):
                if i != self.selected_window:
                    cctv.set_video_size(side_width, side_height)

    def current_window_image(self, index):
        """Retrieve the current frame from a specific CCTV window."""
        if 0 <= index < len(self.cctv_windows):
            return self.cctv_windows[index].get_current_frame()
        print(f"Error: Invalid index {index}. Returning None.")
        return None
