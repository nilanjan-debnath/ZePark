from tab2.source import get_slot_data
from tab1.parking_details import ParkingDetails
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

        main_layout.addLayout(self.create_provider_details())

        # Scrollable area setup
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.dashboard_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.dashboard_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        self.create_slot_layout()
        self.create_dashboard_layout()

    def create_provider_details(self):
        """Create a layout for showing provider details."""
        layout = QVBoxLayout()
        return layout

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

    def create_dashboard_layout(self):
        details_layout = QVBoxLayout()
        for slot in self.slots:
            details_layout.addWidget(slot)
        self.dashboard_layout.addLayout(details_layout)

    def load_stylesheet(self):
        """Load and apply the stylesheet."""
        try:
            with open("app/style/tab1.css", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Error: Stylesheet file not found.")
