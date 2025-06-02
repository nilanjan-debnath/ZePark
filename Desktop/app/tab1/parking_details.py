from PySide6.QtWidgets import QHBoxLayout, QLabel, QGroupBox
from PySide6.QtCore import Qt
import datetime


class ParkingDetails(QGroupBox):
    STATUS_MAP = {
        0: ("EMPTY", "#4CAF50", "#E0E0E0"),  # Green for Empty
        1: ("BOOKED", "#FF9800", "#1C1C1C"),  # Yellow for Booked
        2: ("PARKED", "#F44336", "#1C1C1C"),  # Red for Parked
    }

    def __init__(
        self,
        slot_no,
        status,
        user_name,
        car_no,
        booking_time,
        parking_time,
        emptied_time,
    ):
        super().__init__()
        self.slot_no = slot_no

        layout = QHBoxLayout()
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName("statusLabel")

        self.slot_no_label = QLabel(f"Slot No: {self.slot_no}")
        self.user_label = QLabel()
        self.car_label = QLabel()
        self.timing_label = QLabel()

        layout.addWidget(self.slot_no_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.user_label)
        layout.addWidget(self.car_label)
        layout.addWidget(self.timing_label)

        self.setLayout(layout)
        self.setObjectName("parkingDetails")  # For CSS Styling

        if status == 2:
            self.add_parking_details(parking_time)
        elif status == 1:
            self.add_booking_details(user_name, car_no, booking_time)
        else:
            self.clear_parking_details(emptied_time)

        self.update_status(self.status)  # Apply initial status styles

    def update_status(self, new_status):
        """Update the status of the parking slot with color and text."""
        self.status = new_status
        status_text, bg_color, text_color = self.STATUS_MAP.get(
            new_status, ("Unknown", "#6c757d", "#e2e3e5")
        )

        self.status_label.setText(f"{status_text}")
        self.status_label.setStyleSheet(
            f"""
            color: {text_color};
            background-color: {bg_color};
            """
        )

    def clear_parking_details(self, emptied_time):
        """Clear all details and reset status to 'Empty'."""
        self.update_status(0)
        self.user_label.setText(" ")
        self.car_label.setText(" ")
        if emptied_time == " ":
            emptied_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.emptied_time = emptied_time
        self.timing_label.setText(f"Emptied Time: {self.emptied_time}")

    def add_booking_details(self, user_name, car_no, booking_time):
        """Set booking details and update status to 'Booked'."""
        self.update_status(1)
        self.user_name = user_name
        self.user_label.setText(f"User: {self.user_name}")
        self.car_no = car_no
        self.car_label.setText(f"Car No: {self.car_no}")
        self.booking_time = booking_time
        self.timing_label.setText(f"Booking Time: {self.booking_time}")

    def add_parking_details(self, parking_time):
        """Set parking time and update status to 'Parked'."""
        self.update_status(2)
        self.parking_time = parking_time
        self.timing_label.setText(f"Parking Time: {self.parking_time}")

        self.user_name = "User Name"
        self.user_label.setText(f"User: {self.user_name}")

        self.car_no = "WB 26DQ 0333"
        self.car_label.setText(f"Car No: {self.car_no}")
