# Constants for background videos
videos = [
    "video/video69crop-1.mp4",
    "video/video69crop-2.mp4",
    "video/video69crop-3.mp4",
    "video/video69crop-4.mp4",
    # "video/video69.mp4",
    # "video/video6.mp4",
    # " ",
]


def video(index):
    if index < count():
        return videos[index]
    else:
        print("Video isn't available")
        return " "


def count():
    return len(videos)
