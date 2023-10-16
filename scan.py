import os
from main import HaiZuka

haizuka = HaiZuka()

path = 'C:\\Users\HAIZUKA\\java'
list_folder = haizuka.read_folder(path)

list_folder = [x for x in list_folder if os.path.isdir(os.path.join(path, x))]

for i in range(0, len(list_folder) - 1):
    for j in range(i + 1, len(list_folder)):
        path_1 = os.path.join(path, list_folder[i])
        path_2 = os.path.join(path, list_folder[j])
        similarities = haizuka.similarities_folder(path_1, path_2)
        print(similarities)