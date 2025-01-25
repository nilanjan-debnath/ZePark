from canvas import Canvas
from background import Background
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtGui import QShortcut, QKeySequence


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tab 3")
        self.setGeometry(100, 100, 1024, 640)
        self.canvas = Canvas()

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.create_background_buttons())
        main_layout.addLayout(self.create_function_buttons())
        main_layout.addWidget(self.canvas)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.resize_canvas()
        self.add_shortcuts()

    def create_background_buttons(self):
        layout = QHBoxLayout()
        for i in range(Background.count()):
            button = QPushButton(f"Background {i + 1}")
            button.clicked.connect(
                lambda _, index=i: self.canvas.update_background(
                    Background.image(index)
                )
            )
            layout.addWidget(button)
        return layout

    def create_function_buttons(self):
        layout = QHBoxLayout()
        self.undo_button = QPushButton("Undo")
        self.redo_button = QPushButton("Redo")
        self.remove_button = QPushButton("Remove")
        self.save_button = QPushButton("Save")
        self.load_button = QPushButton("Load")
        self.clear_button = QPushButton("Clear")
        self.reset_button = QPushButton("Reset Indexes")
        self.reset_view_button = QPushButton("Reset View")

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
        )  # maintaining button state

        layout.addWidget(self.undo_button)
        layout.addWidget(self.redo_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.reset_view_button)

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

    def resizeEvent(self, event):
        """Handle resizing of the main window."""
        super().resizeEvent(event)
        self.resize_canvas()

    def resize_canvas(self):
        """Resize the canvas based on the main window size."""
        available_width = self.width() - 20  # Subtract some padding
        available_height = self.height() - 80  # Subtract space for buttons and padding
        self.canvas.resize_canvas(available_width, available_height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
