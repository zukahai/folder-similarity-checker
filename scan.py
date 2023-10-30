import os
from main import HaiZuka
from util import Util

haizuka = HaiZuka()

path = 'C:\\Users\\HAIZUKA\\Downloads\\ex\\ex'

def check_folder(path):
    haizuka = HaiZuka()
    list_folder = haizuka.read_folder(path)

    json_result = {}

    list_folder = [x for x in list_folder if os.path.isdir(os.path.join(path, x))]
    print(list_folder)

    for i in range(0, len(list_folder) - 1):
        for j in range(i + 1, len(list_folder)):
            path_1 = os.path.join(path, list_folder[i])
            path_2 = os.path.join(path, list_folder[j])
            haizuka.__init__()
            similarities = haizuka.similarities_folder(path_1, path_2)
            json_result[list_folder[i] + '@' + list_folder[j]] = similarities

    #sắp xếp theo mean_rate
    json_result = sorted(json_result.items(), key=lambda x: x[1]['mean_rate'], reverse=True)

    return json_result
if __name__ == '__main__':
    check_folder(path)