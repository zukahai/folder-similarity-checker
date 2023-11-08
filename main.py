from gitignore_parser import parse_gitignore
import os
from util import Util
import time
import re
import json

class HaiZuka:
    def __init__(self):
        self.json_result = {}
        self.json_result['files'] = {}
        self.json_result['files_other'] = {}
    def similarities_folder(self, folder1, folder2):
        self.folder_1_name = folder1.split('\\')[-1].split('/')[-1]
        self.folder_2_name = folder2.split('\\')[-1].split('/')[-1]
        self.json_result['files_other'][self.folder_1_name] = {}
        self.json_result['files_other'][self.folder_2_name] = {}

        self.try_similarities(folder1, folder2, '')
        #trung bình rate
        length_similary = 0
        length = 0
        for file in self.json_result['files']:
            leng12 = (self.json_result['files'][file]['length1'] + self.json_result['files'][file]['length2']) / 2
            length_similary += self.json_result['files'][file]['rate'] * leng12
            length += leng12

        similary_rate = length_similary / length
        self.json_result['similary_rate'] = similary_rate

        for file in self.json_result['files_other'][self.folder_1_name]:
            length += self.json_result['files_other'][self.folder_1_name][file]
        for file in self.json_result['files_other'][self.folder_2_name]:
            length += self.json_result['files_other'][self.folder_2_name][file]
        mean_rate = length_similary / length

        self.json_result['mean_rate'] = mean_rate
        self.json_result['folder1'] = self.folder_1_name
        self.json_result['folder2'] = self.folder_2_name
        
        print('\n================= Result ==================\n', json.dumps(self.json_result, indent=4))

        return self.json_result
        

    def try_similarities(self, folder1, folder2, prefix):
        print(folder1, folder2, prefix)
        list_files = HaiZuka.read_folder(folder1)
        self.read_other_file(folder1, folder2, list_files, HaiZuka.read_folder(folder2))
        print(list_files)
        for file in list_files:
            if HaiZuka.is_path_ignored(file):
                continue
            # kiểm tra file có phải 1 file hay không
            if os.path.isfile(folder1 + '/' + file) and os.path.isfile(folder2 + '/' + file):
                print("File: ", file)
                similaritie = HaiZuka.similarities_file(folder1 + '/' + file, folder2 + '/' + file)
                self.json_result['files'][prefix + '/' + file] = similaritie
                print(json.dumps(similaritie, indent=4))
            # kiểm tra file có phải 1 folder không
            elif os.path.isdir(folder1 + '/' + file) and os.path.isdir(folder2 + '/' + file):
                print("Folder: ", file)
                self.try_similarities(folder1 + '/' + file, folder2 + '/' + file, prefix + '/' + file)


    def read_other_file(self, folder1, folder2, list_files_1, list_files_2):
        for file in list_files_1:
            if file not in list_files_2 and os.path.isfile(folder1 + '/' + file):
                length = len(Util.read_file(folder1 + '/' + file))
                self.json_result['files_other'][self.folder_1_name][file] = length
        for file in list_files_2:
            if file not in list_files_1 and os.path.isfile(folder2 + '/' + file):
                length = len(Util.read_file(folder2 + '/' + file))
                self.json_result['files_other'][self.folder_2_name][file] = length
    @staticmethod
    def read_folder(folder):
        list_files = os.listdir(folder)
        return list_files

    @staticmethod
    def similarities_file(file1, file2):
        s = Util.read_file(file1)
        p = Util.read_file(file2)
        words_s = re.findall(r'\b\w+\b', s)
        words_p = re.findall(r'\b\w+\b', p)
        print(len(words_s), len(words_p))
        similarities =  HaiZuka.similarities_words(words_s, words_p)
        return similarities

    # Hàm tìm chuỗi con chung dài nhất
    @staticmethod
    def similarities_words(string1, string2):
        if string1 == string2:
            return {'similarity': 1, 'length1': len(string1), 'length2': len(string2), 'rate': 1}
        string1 = ['x'] + string1
        string2 = ['x'] + string2
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
    def is_path_ignored(path_to_check, gitignore_file='ignore.txt'):
        gitignore = parse_gitignore(gitignore_file)
        return gitignore(path_to_check)
    
    def write_json_utf8(self):
        #tạo tên file yyyy-mm-dd_hh_mm_ss.json
        file_name_time = 'results\\' + time.strftime("%Y-%m-%d_%H_%M_%S") + '.json'
        Util.write_json_utf8(file_name_time, self.json_result)
    
    @staticmethod
    def write_json_utf8_2(json_result):
        #tạo tên file yyyy-mm-dd_hh_mm_ss.json
        file_name_time = 'results\\' + time.strftime("%Y-%m-%d_%H_%M_%S") + '.json'
        Util.write_json_utf8(file_name_time, json_result)

# haizuka = HaiZuka()
# rs = haizuka.similarities_folder('C:\\Users\HAIZUKA\\java\kkk', 'C:\\Users\HAIZUKA\\java\DHDN')
# print(rs)
# haizuka.write_json_utf8()


