import json

class Util:
    def __init__(self):
        pass

    @staticmethod
    def write_json_utf8(path, data):  # Sửa tên biến thành "data"
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

data = {
    "a": 1
}

