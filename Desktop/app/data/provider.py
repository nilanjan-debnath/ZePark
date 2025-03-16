import json

provider_data = "app/data/resource/json/provider.json"


def get_provider_details():
    try:
        with open(provider_data, "r") as file:
            provider_details = json.load(file)
            # print(all_rectangle_data)
        return provider_details
    except FileNotFoundError:
        return {}
