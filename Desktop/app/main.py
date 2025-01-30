from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt
from tab2.tab2 import Tab2Content
from tab3.tab3 import Tab3Content


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stylish Tabs with External Stylesheet")
        self.setGeometry(100, 100, 1024, 640)
        self.setMinimumSize(1024, 640)

        # Create a QTabWidget
        self.tab_widget = QTabWidget()

        # Set tab position to the top
        self.tab_widget.setTabPosition(QTabWidget.North)

        # Create tabs
        self.tab1 = QWidget()
        # self.tab3 = QWidget()
        self.tab2 = Tab2Content()
        self.tab3 = Tab3Content(self.tab2)

        # Set up tab1 content
        tab1_layout = QVBoxLayout()
        tab1_label = QLabel("This is Tab 1")
        tab1_label.setAlignment(Qt.AlignCenter)
        tab1_layout.addWidget(tab1_label)
        self.tab1.setLayout(tab1_layout)

        # Set up tab2 content
        tab2_layout = QVBoxLayout()
        tab2_label = QLabel("This is Tab 2")
        tab2_label.setAlignment(Qt.AlignCenter)
        tab2_layout.addWidget(tab2_label)
        self.tab2.setLayout(tab2_layout)

        # Add tabs to the QTabWidget
        self.tab_widget.addTab(self.tab1, "Dashboard")
        self.tab_widget.addTab(self.tab2, "CCTV")
        self.tab_widget.addTab(self.tab3, "Area Selector")

        # Set Tab 3 as the default tab
        self.tab_widget.setCurrentIndex(1)

        # Set the central widget
        self.setCentralWidget(self.tab_widget)

        # Load and apply the external stylesheet
        self.apply_stylesheet()

    def apply_stylesheet(self):
        """Load and apply the stylesheet from an external QSS file."""
        try:
            with open("app/style/main.css", "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            print("Error: Stylesheet file not found.")

    def resizeEvent(self, event):
        """Dynamically adjust tab widths when the window is resized."""
        total_width = self.width()
        tab_count = self.tab_widget.count()
        tab_width = total_width // tab_count

        # Dynamically adjust tab width in the stylesheet
        self.tab_widget.setStyleSheet(f"""
            QTabBar::tab {{
                width: {tab_width - 55}px; /* Dynamically adjust tab width */
            }}
        """)

        # Call the parent class's resizeEvent
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
