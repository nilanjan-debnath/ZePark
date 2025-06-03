import json

provider_data_file = "app/data/resource/json/provider.json"

provider_details = {}


def fetch_local_provider_details():
    try:
        global provider_details
        with open(provider_data_file, "r") as file:
            provider_details = json.load(file)
    except FileNotFoundError:
        provider_details = {}


fetch_local_provider_details()


def save_provider_details():
    global provider_details
    with open(provider_data_file, "w") as file:
        json.dump(provider_details, file, indent=4)


def get_provider_details():
    global provider_details
    return provider_details


def update_count(parked_count, booked_count, empty_count):
    provider_details.update({"parked slots": parked_count})
    provider_details.update({"booked slots": booked_count})
    provider_details.update({"empty slots": empty_count})
    provider_details.update({"total slots": parked_count + booked_count + empty_count})
    save_provider_details()
