def format_phone_number(phone_number):
    """
    전화번호에서 '-'를 제거하는 함수
    """
    num_list = phone_number.split("-")
    result = "".join(num_list)
    return result


def check_dest(dest, dest_list):
    """
    dest 판별하는 함수
    """
    if dest not in dest_list:
        return "주소가 지도상에 존재하지 않습니다."

    if len(dest) != 3:
        return "주소가 3자리가 아닙니다."

    return True


def check_phone_number(phone_number):
    """
    phone_number 판별하는 함수
    """
    if len(phone_number) != 11:
        return "전화번호가 11자리가 아닙니다."

    if phone_number[0] != "0":
        return "전화번호가 0으로 시작하지 않습니다."

    return True
