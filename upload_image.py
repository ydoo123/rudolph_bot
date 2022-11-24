import requests
import json


def get_url():
    filename = "jpeg420exif.jpg"
    filepath = f"/home/ubuntu/test_server/rudolph_bot/test/image/{filename}"

    url = "http://140.238.28.123/fileUpload"

    files = {
        "file": (filename, open(filepath, "rb")),
        "Content-Type": "image/jpg",
        # "Content-Length": l,
    }
    r = requests.post(url, files=files)
    return None


if __name__ == "__main__":
    result = get_url()
