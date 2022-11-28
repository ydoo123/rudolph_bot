import requests
import os
import json


URL = "http://140.238.28.123/fileUpload"


def check_dir():
    """
    이미지 파일 다루기 전, images 폴더가 있는지 확인. 없으면 images 폴더 생성
    """
    cwd = os.getcwd()
    ls = os.listdir(cwd)

    if "images" not in ls:
        os.makedirs(f"{cwd}/images")

    return None


def upload_image(file_name, file_path):
    """
    URL로 이미지파일을 업로드하는 함수
    """
    filename = file_name
    filepath = file_path

    image_file = {
        "file": (filename, open(filepath, "rb")),
        "Content-Type": "image/jpg",
        # "Content-Length": l,
    }
    requests.post(URL, files=image_file)

    return None


if __name__ == "__main__":

    # filename = "jpeg420exif.jpg"
    # filepath = f"/home/ubuntu/test_server/rudolph_bot/test/image/{filename}"

    # result = upload_image(filename, filepath)

    # check_dir()
    print("test")
