from .provider import get_provider_details, update_count
from .video_source import source_count, get_video
from .rectangle import get_rect_data, save_rect_data
from .parking_slot import get_slot_data, save_slot_data
from . import model


__all__ = [
    "get_provider_details",
    "update_count",
    "source_count",
    "get_video",
    "get_rect_data",
    "save_rect_data",
    "get_slot_data",
    "save_slot_data",
    "model",
]
