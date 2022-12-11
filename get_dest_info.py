"""
서버에 목적지 데이터 요청해, 데이터 받아오는 코드.
.json 파일 형태로 받아오기 때문에 한글은 인코딩 추가로 처리해야되서 패스~

dest = 목적지 주소 (e.g. dest: 112)
method = 수령 방법 (e.g. method: 0)
method == 0 이면 직접 수령, method == 1 이면 문 앞에 놓고 가기
"""


import requests
import json


def get_dest_dict() -> dict:
    URL = "http://140.238.28.123/get_dest"
    response = requests.get(URL)

    return_dict = json.loads(response.text)
    return return_dict


def get_dest() -> str:
    result_dict: dict = get_dest_dict()
    return result_dict["dest"]  # str


def get_method() -> str:
    result_dict: dict = get_dest_dict()
    return result_dict["method"]  # str


if __name__ == "__main__":
    result = get_dest_dict()
    print(result)
    print(type(result))
