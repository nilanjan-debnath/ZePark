from PySide6.QtWidgets import QHBoxLayout, QGroupBox, QVBoxLayout, QLabel
from data import get_provider_details


class ProviderDetails(QGroupBox):
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
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        name_box = QHBoxLayout()
        self.park_name_label = QLabel(f"Park Name: {self.park_name}")
        self.provider_name_label = QLabel(f"Park Name: {self.provider_name}")
        name_box.addWidget(self.park_name_label)
        name_box.addWidget(self.provider_name_label)

        self.address_label = QLabel(f"Address: {self.address}")

        layout.addLayout(name_box)
        layout.addWidget(self.address_label)

        self.setLayout(layout)
        self.setObjectName("providerDetails")
