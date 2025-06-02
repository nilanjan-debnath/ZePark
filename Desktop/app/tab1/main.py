import threading
from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QScrollArea

from data import get_slot_data
from .parking_details import ParkingDetails
from .provider_details import ProviderDetails
from .ui_process import ui_worker
from .count_box import CountBox


class Tab1Content(QGroupBox):
    def __init__(self):
        super().__init__()
        self.slots = []
        threading.Thread(target=ui_worker, args=(self,), daemon=True).start()

        self.load_stylesheet()
        self.setObjectName("tab1Main")

        self.init_variables()
        self.init_ui()

    def init_variables(self):
        self.empty_count = 0
        self.booked_count = 0
        self.parked_count = 0

    def init_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.main_layout.addWidget(ProviderDetails())
        self.create_count_box()

        # Scrollable area setup
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scrollArea")
        self.dashboard_layout = QVBoxLayout()
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("scrollWidget")
        self.scroll_widget.setLayout(self.dashboard_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        self.create_dashboard_layout()

    def create_slot_layout(self):
        slot_data = get_slot_data()
        self.slots = []
        for slot in slot_data:
            slot_widget = ParkingDetails(
                slot_no=slot["slot_no"],
                status=slot["status"],
                user_name=slot["user_name"],
                car_no=slot["car_no"],
                booking_time=slot["booking_time"],
                parking_time=slot["parking_time"],
                emptied_time=slot["emptied_time"],
            )
            self.slots.append(slot_widget)
            self.details_layout.addWidget(slot_widget)

            if slot["status"] == 0:
                self.empty_count += 1
            elif slot["status"] == 1:
                self.booked_count += 1
            else:
                self.parked_count += 1

    def clear_layout(self, layout):
        """Clear all widgets from a layout, but avoid deleting CCTV players directly."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def refresh_details(self):
        self.slots.clear()
        self.init_variables()
        self.clear_layout(self.details_layout)
        self.create_slot_layout()
        self.clear_layout(self.count_box)
        self.create_count_widget()

    def create_dashboard_layout(self):
        self.details_layout = QVBoxLayout()
        self.create_slot_layout()
        self.create_count_widget()
        self.dashboard_layout.addLayout(self.details_layout)

    def create_count_widget(self):
        self.count_box_widget = CountBox(
            self.parked_count, self.booked_count, self.empty_count
        )
        self.count_box.addWidget(self.count_box_widget)

    def create_count_box(self):
        self.count_box = QVBoxLayout()
        self.main_layout.addLayout(self.count_box)

    def load_stylesheet(self):
        """Load and apply the stylesheet."""
        try:
            with open("app/style/tab1.css", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Error: Stylesheet file not found.")
