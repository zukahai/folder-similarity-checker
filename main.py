import codecs
def similarities_file(file1, file2):
    s = read_file(file1)
    p = read_file(file2)
    print(s)
    print(p)

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
    # print(a[len(string1) - 1][len(string2) - 1])
    print(a)

def read_file(path):
    # Đọc file bằng mã hóa UTF-8
    with codecs.open(path, 'r', encoding='utf-8') as file:
        java_code = file.read()

    return java_code

similarities_string('cabah', 'cha')

# similarities_file('C:\\Users\HAIZUKA\\java\kkk\\src\model\\Student.java', 'C:\\Users\HAIZUKA\\java\kkk\\src\model\\People.java')