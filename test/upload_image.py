import requests
import os
import cv2
import datetime


URL = "http://140.238.28.123/fileUpload"
TIME_FORMAT = "%Y-%m-%d_%H:%M:%S"


def check_dir():
    """
    이미지 파일 다루기 전, images 폴더가 있는지 확인. 없으면 images 폴더 생성
    """
    cwd = os.getcwd()
    ls = os.listdir(cwd)

    if "images" not in ls:
        os.makedirs(f"{cwd}/images")

    return None


def save_image():
    """
    웹캠 화면을 저장하는 코드.
    return: 저장된 이미지 파일 이름(현재 시간), 저장된 이미지 파일 경로
    """

    now_time = datetime.datetime.now().strftime(TIME_FORMAT)

    check_dir()
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()

    img_name = f"images/image_{now_time}.jpg"
    cv2.imwrite(img_name, frame)

    cam.release()
    cv2.destroyAllWindows()

    file_name = f"image_{now_time}.jpg"
    file_path = f"images/{file_name}"

    return file_name, file_path


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

    file_name, file_path = save_image()
    upload_image(file_name, file_path)
