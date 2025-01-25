# Constants for background images
images = [
    "img/Screenshot (331).png",
    "img/Screenshot (301).png",
    "img/Screenshot (304).png",
    "img/Screenshot (312).png",
]


class Background:
    @staticmethod
    def image(index):
        if index < len(images):
            return images[index]
        else:
            print("Image isn't available")
            return ""

    @staticmethod
    def count():
        return len(images)
