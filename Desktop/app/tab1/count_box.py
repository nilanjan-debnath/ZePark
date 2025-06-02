from PySide6.QtWidgets import QHBoxLayout, QLabel, QGroupBox
from PySide6.QtCore import Qt
import logging


class CountBox(QGroupBox):
    def __init__(self, parked_count, booked_count, empty_count):
        super().__init__()
        self.parked_count = parked_count
        self.booked_count = booked_count
        self.empty_count = empty_count
        self.total_count = parked_count + empty_count + booked_count
        logging.debug(f"CountBox: {parked_count=} {booked_count=} {empty_count=}")

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.parked_label = QLabel(f"PARKED : {self.parked_count}")
        self.parked_label.setAlignment(Qt.AlignCenter)
        self.parked_label.setObjectName("parkedLabel")
        layout.addWidget(self.parked_label)

        self.booked_label = QLabel(f"BOOKED : {self.booked_count}")
        self.booked_label.setAlignment(Qt.AlignCenter)
        self.booked_label.setObjectName("bookedLabel")
        layout.addWidget(self.booked_label)

        self.empty_label = QLabel(f"EMPTY : {self.empty_count}")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setObjectName("emptyLabel")
        layout.addWidget(self.empty_label)

        self.total_label = QLabel(f"TOTAL : {self.total_count}")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setObjectName("totalLabel")
        layout.addWidget(self.total_label)

        self.setLayout(layout)
        self.setObjectName("countBox")

    def refresh_count(self, parked_count, booked_count, empty_count):
        self.parked_label.setText(f"PARKED : {parked_count}")
        self.booked_label.setText(f"BOOKED : {booked_count}")
        self.empty_label.setText(f"EMPTY : {empty_count}")
