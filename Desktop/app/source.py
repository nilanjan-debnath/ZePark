# Constants for background images
images = [
    "img/Screenshot (331).png",
    "img/Screenshot (301).png",
    "img/Screenshot (304).png",
    "img/Screenshot (312).png",
]
videos = [
    "video/video69crop-1.mp4",
    "video/video69crop-2.mp4",
    "video/video69crop-3.mp4",
    "video/video6.mp4",
]


def image(index):
    if index < len(images):
        return images[index]
    else:
        print("Image isn't available")
        return ""


def video(index):
    if index < count():
        return videos[index]
    else:
        print("Video isn't available")
        return ""


def count():
    return len(videos)
