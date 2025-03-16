from data import get_slot_data
from .parking_details import ParkingDetails
from .provider_details import ProviderDetails
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea


class Tab1Content(QWidget):
    def __init__(self):
        super().__init__()
        self.slots = []

        # Initialize the UI components
        self.load_stylesheet()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        main_layout.addWidget(ProviderDetails())

        # Scrollable area setup
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.dashboard_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.dashboard_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        self.create_dashboard_layout()

    def create_slot_layout(self):
        slot_data = get_slot_data()
        self.slots = [
            ParkingDetails(
                slot_no=slot["slot_no"],
                status=slot["status"],
                user_name=slot["user_name"],
                car_no=slot["car_no"],
                booking_time=slot["booking_time"],
                parking_time=slot["parking_time"],
            )
            for slot in slot_data
        ]

    def add_slot_widget(self):
        for slot in self.slots:
            self.details_layout.addWidget(slot)

    def clear_layout(self, layout):
        """Clear all widgets from a layout, but avoid deleting CCTV players directly."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def refresh_details(self):
        self.slots.clear()
        self.clear_layout(self.details_layout)
        self.create_slot_layout()
        self.add_slot_widget()

    def create_dashboard_layout(self):
        self.details_layout = QVBoxLayout()
        self.create_slot_layout()
        self.add_slot_widget()
        self.dashboard_layout.addLayout(self.details_layout)

    def load_stylesheet(self):
        """Load and apply the stylesheet."""
        try:
            with open("app/style/tab1.css", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Error: Stylesheet file not found.")
