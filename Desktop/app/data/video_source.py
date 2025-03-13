videos = [
    "app/data/resource/video/video69crop-1.mp4",
    "app/data/resource/video/video69crop-2.mp4",
    "app/data/resource/video/video69crop-3.mp4",
    "app/data/resource/video/video69crop-4.mp4",
    # "app/data/resource/video/video69.mp4",
    # "app/data/resource/video/video6.mp4",
    # " ",
]


def get_video(index):
    if index < source_count():
        return videos[index]
    else:
        print("Video isn't available")
        return " "


def source_count():
    return len(videos)
