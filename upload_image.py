import requests
import json


def upload_image(file_name, file_path):
    filename = file_name
    filepath = file_path

    url = "http://140.238.28.123/fileUpload"

    files = {
        "file": (filename, open(filepath, "rb")),
        "Content-Type": "image/jpg",
        # "Content-Length": l,
    }
    r = requests.post(url, files=files)
    return None


if __name__ == "__main__":
    
    filename = "jpeg420exif.jpg"
    filepath = f"/home/ubuntu/test_server/rudolph_bot/test/image/{filename}"
    
    result = upload_image(filename, filepath)
