from tab3.canvas import Canvas
from tab2 import source

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QShortcut, QKeySequence


class Tab3Content(QWidget):
    def __init__(self, tab1, tab2):
        super().__init__()
        self.tab1_instance = tab1
        self.tab2_instance = tab2
        self.canvas = Canvas(self.tab1_instance, self.tab2_instance)
        self.current_background_button = None

        self.load_stylesheet()
        self.setup_ui()
        self.add_shortcuts()

    def setup_ui(self):
        """Initialize and configure the main UI components"""
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.create_background_buttons())
        main_layout.addLayout(self.create_function_buttons())
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)
        self.adjust_canvas_size()

    def adjust_canvas_size(self):
        """Adjust canvas size based on current widget dimensions"""
        available_width = self.width() - 10  # Padding adjustment
        available_height = self.height() - 92  # Padding adjustment
        self.canvas.resize_canvas(available_width, available_height)
        self.canvas.load()

    def resizeEvent(self, event):
        """Update canvas size when window is resized"""
        super().resizeEvent(event)
        self.adjust_canvas_size()

    def create_background_buttons(self):
        """Create dynamic background selection buttons"""
        layout = QHBoxLayout()
        for i in range(source.count()):
            button = QPushButton(f"Background {i + 1}")
            button.setObjectName("backgroundButton")
            button.clicked.connect(
                lambda _, idx=i, btn=button: self.select_background(idx, btn)
            )
            layout.addWidget(button)
            if i == 0:
                self.update_current_background_button(button)
        return layout

    def select_background(self, index, button):
        """Switch active background and update UI"""
        self.canvas.update_background(index)
        self.canvas.load()
        self.update_current_background_button(button)

    def create_function_buttons(self):
        """Create and connect functional control buttons"""
        layout = QHBoxLayout()
        button_actions = {
            "undo_button": ("Undo", self.canvas.undo),
            "redo_button": ("Redo", self.canvas.redo),
            "remove_button": ("Remove", self.canvas.remove),
            "save_button": ("Save", self.canvas.save),
            "load_button": ("Load", self.canvas.load),
            "clear_button": ("Clear", self.canvas.clear),
            "reset_button": ("Reset Indexes", self.canvas.reset_indexes),
            "reset_view_button": ("Reset View", self.canvas.reset_view),
        }

        for attr, (text, func) in button_actions.items():
            button = QPushButton(text)
            button.setObjectName(attr)
            setattr(self, attr, button)
            layout.addWidget(button)
            button.clicked.connect(func)

        self.canvas.set_buttons(self.undo_button, self.redo_button, self.remove_button)
        return layout

    def add_shortcuts(self):
        """Register keyboard shortcuts for common actions"""
        shortcuts = [
            ("Ctrl+Z", self.canvas.undo),
            ("Ctrl+Y", self.canvas.redo),
            ("Del", self.canvas.remove),
            ("Ctrl+S", self.canvas.save),
            ("Ctrl+O", self.canvas.load),
            ("Ctrl+L", self.canvas.clear),
            ("Ctrl+R", self.canvas.reset_view),
        ]

        for key_sequence, func in shortcuts:
            QShortcut(QKeySequence(key_sequence), self, func)

    def update_current_background_button(self, button):
        """Manage visual state of active background button"""
        if self.current_background_button:
            self._toggle_button_state(self.current_background_button, False)
        self.current_background_button = button
        self._toggle_button_state(button, True)

    def _toggle_button_state(self, button, active):
        """Helper to update button styling based on state"""
        button.setProperty("active", active)
        button.style().unpolish(button)
        button.style().polish(button)

    def load_stylesheet(self):
        """Apply external stylesheet to the widget"""
        try:
            with open("app/style/tab3.css", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Error: Stylesheet file not found.")
