from .provider import get_provider_details
from .video_source import source_count, get_video
from .rectangle import get_rect_data, save_rect_data
from .parking_slot import get_slot_data, save_slot_data

__all__ = [
    "get_provider_details",
    "source_count",
    "get_video",
    "get_rect_data",
    "save_rect_data",
    "get_slot_data",
    "save_slot_data",
]
