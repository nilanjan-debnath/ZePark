# Constants for background images
images = [
    "img/Screenshot (331).png",
    "img/Screenshot (301).png",
    "img/Screenshot (304).png",
    "img/Screenshot (312).png",
]


def image(index):
    if index < len(images):
        return images[index]
    else:
        print("Image isn't available")
        return ""


def count():
    return len(images)
