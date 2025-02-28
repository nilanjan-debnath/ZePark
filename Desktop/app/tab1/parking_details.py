from PySide6.QtWidgets import QHBoxLayout, QLabel, QGroupBox


class ParkingDetails(QGroupBox):
    STATUS_MAP = {
        0: ("Empty", "#28a745", "#d4edda"),  # Green for Empty
        1: ("Booked", "#ffc107", "#fff3cd"),  # Yellow for Booked
        2: ("Parked", "#dc3545", "#f8d7da"),  # Red for Parked
    }

    def __init__(self, slot_no, status, user_name, car_no, booking_time, parking_time):
        super().__init__()

        self.slot_no = slot_no
        self.status = status
        self.user_name = user_name
        self.car_no = car_no
        self.booking_time = booking_time
        self.parking_time = parking_time

        # Layout for displaying details
        layout = QHBoxLayout()

        self.status_label = QLabel()
        self.slot_no_label = QLabel(f"Slot No: {self.slot_no}")
        self.user_label = QLabel(f"User: {self.user_name}")
        self.car_label = QLabel(f"Car No: {self.car_no}")
        self.booking_label = QLabel(f"Booking Time: {self.booking_time}")
        self.parking_label = QLabel(f"Parking Time: {self.parking_time}")

        layout.addWidget(self.slot_no_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.user_label)
        layout.addWidget(self.car_label)
        layout.addWidget(self.booking_label)
        layout.addWidget(self.parking_label)

        self.setLayout(layout)
        self.setObjectName("parkingDetails")  # For CSS Styling

        self.update_status(self.status)  # Apply initial status styles

    def update_status(self, new_status):
        """Update the status of the parking slot with color and text."""
        self.status = new_status
        status_text, text_color, bg_color = self.STATUS_MAP.get(
            new_status, ("Unknown", "#6c757d", "#e2e3e5")
        )

        self.status_label.setText(f"Status: {status_text}")
        self.status_label.setStyleSheet(
            f"color: {text_color}; background-color: {bg_color}; padding: 5px; border-radius: 5px;"
        )

    def add_booking_details(self, user_name, car_no, booking_time):
        """Set booking details and update status to 'Booked'."""
        self.update_status(1)
        self.user_name = user_name
        self.user_label.setText(f"User: {self.user_name}")
        self.car_no = car_no
        self.car_label.setText(f"Car No: {self.car_no}")
        self.booking_time = booking_time
        self.booking_label.setText(f"Booking Time: {self.booking_time}")

    def add_parking_details(self, parking_time):
        """Set parking time and update status to 'Parked'."""
        self.update_status(2)
        self.parking_time = parking_time
        self.parking_label.setText(f"Parking Time: {self.parking_time}")

    def clear_parking_details(self):
        """Clear all details and reset status to 'Empty'."""
        self.update_status(0)
        self.user_label.setText("User: ")
        self.car_label.setText("Car No: ")
        self.booking_label.setText("Booking Time: ")
        self.parking_label.setText("Parking Time: ")
