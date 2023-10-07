import codecs
from gitignore_parser import parse_gitignore
import os
from util import Util
import time

class HaiZuka:
    def __init__(self):
        self.json_result = {}
    def similarities_folder(self, folder1, folder2):
        self.try_similarities(folder1, folder2, '')
        #trung bình rate
        rate = []
        for file in self.json_result:
            rate.append(self.json_result[file]['rate'])

        mean_rate = 0 if len(rate) == 0 else sum(rate)/len(rate)
        self.json_result['mean_rate'] = mean_rate
        self.json_result['folder1'] = folder1.split('\\')[-1].split('/')[-1]
        self.json_result['folder2'] = folder2.split('\\')[-1].split('/')[-1]
        return self.json_result
        

    def try_similarities(self, folder1, folder2, prefix):
        list_files = HaiZuka.read_folder(folder1)
        print(list_files)
        for file in list_files:
            if HaiZuka.is_path_ignored(file):
                continue
            # kiểm tra file có phải 1 file hay không
            if os.path.isfile(folder1 + '/' + file) and os.path.isfile(folder2 + '/' + file):
                print("File: ", file)
                similaritie = HaiZuka.similarities_file(folder1 + '/' + file, folder2 + '/' + file)
                self.json_result[prefix + '/' + file] = similaritie
                print(similaritie)
            # kiểm tra file có phải 1 folder không
            elif os.path.isdir(folder1 + '/' + file) and os.path.isdir(folder2 + '/' + file):
                print("Folder: ", file)
                self.try_similarities(folder1 + '/' + file, folder2 + '/' + file, prefix + '/' + file)


    @staticmethod
    def read_folder(folder):
        s = os.listdir(folder)
        return s

    @staticmethod
    def similarities_file(file1, file2):
        s = HaiZuka.read_file(file1)
        p = HaiZuka.read_file(file2)
        similarities =  HaiZuka.similarities_string(s, p)
        return similarities

    # Hàm tìm chuỗi con chung dài nhất
    @staticmethod
    def similarities_string(string1, string2):
        string1 = "x" + string1
        string2 = "x" + string2
        a = [[0 for _ in range(len(string2))] for _ in range(len(string1))]
        for i in range(1, len(string1)):
            for j in range(1, len(string2)):
                if string1[i] == string2[j]:
                    a[i][j] = a[i - 1][j - 1] + 1
                else:
                    a[i][j] = max(a[i - 1][j], a[i][j - 1])
        max_str = a[len(string1) - 1][len(string2) - 1]
        json = {}
        json['similarity'] = max_str
        json['length1'] = len(string1)
        json['length2'] = len(string2)
        json['rate'] = 2 * max_str / (len(string1) + len(string2) - 2)
        return json

    @staticmethod
    def read_file(path):
        # Đọc file bằng mã hóa UTF-8
        with codecs.open(path, 'r', encoding='utf-8') as file:
            java_code = file.read()
        return java_code

    @staticmethod
    def is_path_ignored(path_to_check, gitignore_file='ignore.txt'):
        gitignore = parse_gitignore(gitignore_file)
        return gitignore(path_to_check)
    
    def write_json_utf8(self):
        #tạo tên file yyyy-mm-dd_hh_mm_ss.json
        file_name_time = 'results\\' + time.strftime("%Y-%m-%d_%H_%M_%S") + '.json'
        Util.write_json_utf8(file_name_time, self.json_result)

# haizuka = HaiZuka()
# rs = haizuka.similarities_folder('C:\\Users\HAIZUKA\\java\kkk', 'C:\\Users\HAIZUKA\\java\DHDN')
# print(rs)
# haizuka.write_json_utf8()


