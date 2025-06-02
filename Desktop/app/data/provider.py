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


def update_count(category, count):
    provider_details.update({category: count})
    save_provider_details()
