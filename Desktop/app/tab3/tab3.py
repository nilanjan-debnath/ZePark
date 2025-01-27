from tab3.canvas import Canvas
import source

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtGui import QShortcut, QKeySequence


class Tab3Content(QWidget):
    def __init__(self, tab2):
        super().__init__()
        self.tab2_instance = tab2
        self.canvas = Canvas(self.tab2_instance)
        self.current_background_button = None

        self.load_stylesheet()

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.create_background_buttons())
        main_layout.addLayout(self.create_function_buttons())
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

        self.resize_canvas()
        self.add_shortcuts()

    def create_background_buttons(self):
        layout = QHBoxLayout()
        background_count = source.count()
        if background_count > 0:
            for i in range(background_count):
                button = QPushButton(f"Background {i + 1}")
                button.setObjectName("backgroundButton")  # For styling in CSS
                button.clicked.connect(
                    lambda _, index=i, btn=button: self.select_background(index, btn)
                )
                layout.addWidget(button)
                if i == 0:
                    self.update_current_background_button(button)
        return layout

    def select_background(self, index, button):
        """Handle background selection and highlight the active button."""
        pixmap = self.tab2_instance.current_window_image(index)
        if pixmap:
            self.canvas.update_background(pixmap)
            self.update_current_background_button(button)
        else:
            print(f"Failed to retrieve image for index {index}.")

    def update_current_background_button(self, button):
        # Remove the 'current' class from the previously selected button
        if self.current_background_button:
            self.current_background_button.setProperty("active", False)
            self.current_background_button.style().unpolish(
                self.current_background_button
            )
            self.current_background_button.style().polish(
                self.current_background_button
            )

        # Add the 'current' class to the newly selected button
        self.current_background_button = button
        self.current_background_button.setProperty("active", True)
        self.current_background_button.style().unpolish(self.current_background_button)
        self.current_background_button.style().polish(self.current_background_button)

    def create_function_buttons(self):
        layout = QHBoxLayout()

        # Create and style buttons
        buttons = {
            "undo_button": "Undo",
            "redo_button": "Redo",
            "remove_button": "Remove",
            "save_button": "Save",
            "load_button": "Load",
            "clear_button": "Clear",
            "reset_button": "Reset Indexes",
            "reset_view_button": "Reset View",
        }

        for attr, text in buttons.items():
            button = QPushButton(text)
            button.setObjectName(attr)  # For styling in CSS
            setattr(self, attr, button)
            layout.addWidget(button)

        # Connect buttons to canvas methods
        self.undo_button.clicked.connect(self.canvas.undo)
        self.redo_button.clicked.connect(self.canvas.redo)
        self.remove_button.clicked.connect(self.canvas.remove)
        self.save_button.clicked.connect(self.canvas.save)
        self.load_button.clicked.connect(self.canvas.load)
        self.clear_button.clicked.connect(self.canvas.clear)
        self.reset_button.clicked.connect(self.canvas.reset_indexes)
        self.reset_view_button.clicked.connect(self.canvas.reset_view)

        self.canvas.set_buttons(
            self.undo_button, self.redo_button, self.remove_button
        )  # Maintain button state

        return layout

    def add_shortcuts(self):
        """Bind keyboard shortcuts to button actions."""
        QShortcut(QKeySequence("Ctrl+Z"), self, self.canvas.undo)
        QShortcut(QKeySequence("Ctrl+Y"), self, self.canvas.redo)
        QShortcut(QKeySequence("Del"), self, self.canvas.remove)
        QShortcut(QKeySequence("Ctrl+S"), self, self.canvas.save)
        QShortcut(QKeySequence("Ctrl+O"), self, self.canvas.load)
        QShortcut(QKeySequence("Ctrl+L"), self, self.canvas.clear)
        QShortcut(QKeySequence("Ctrl+R"), self, self.canvas.reset_view)

    def resize_canvas(self):
        """Resize the canvas based on the main window size."""
        available_width = self.width() - 10  # Subtract some padding
        available_height = self.height() - 92  # Subtract space for buttons and padding
        self.canvas.resize_canvas(available_width, available_height)

    def resizeEvent(self, event):
        """Handle resizing of the tab."""
        super().resizeEvent(event)
        self.resize_canvas()

    def load_stylesheet(self):
        """Load and apply a stylesheet from an external file."""
        try:
            with open("app/style/tab3.css", "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            print("Error: Stylesheet file not found.")
