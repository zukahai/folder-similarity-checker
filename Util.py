class Util:
    def __init__(self):
        pass
    def write_json_utf8(self, path, json):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(json)

json = {
    "a": 1
}

u = Util()
u.write_json_utf8('test.json', json)