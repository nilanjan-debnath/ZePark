from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from data.source import get_provider_details


class ProviderDetails(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.init_variables()
        self.init_ui()

    def init_variables(self):
        data = get_provider_details()
        self.park_name = data.get("area name")
        self.provider_name = data.get("provider name")
        self.address = data.get("address")
        self.empty_count = data.get("empty slots")
        self.booked_count = data.get("booked slots")
        self.parked_count = data.get("parked slots")

    def init_ui(self):
        name_box = QHBoxLayout()
        self.park_name_label = QLabel(f"Park Name: {self.park_name}")
        self.provider_name_label = QLabel(f"Park Name: {self.provider_name}")
        name_box.addWidget(self.park_name_label)
        name_box.addWidget(self.provider_name_label)

        self.address_label = QLabel(f"Address: {self.address}")

        count_box = QHBoxLayout()
        self.empty_label = QLabel(f"Empty: {self.empty_count}")
        self.booked_label = QLabel(f"Parked: {self.booked_count}")
        self.parked_label = QLabel(f"Parked: {self.parked_count}")
        count_box.addWidget(self.empty_label)
        count_box.addWidget(self.booked_label)
        count_box.addWidget(self.parked_label)

        self.addLayout(name_box)
        self.addWidget(self.address_label)
        self.addLayout(count_box)
