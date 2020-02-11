import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)

from core import process


func_dic = [
    ('学员', process.Views().student),
    ('讲师', process.Views().teacher),
    ('管理员', process.Views().root)
]


if __name__ == '__main__':
    process.func(func_dic)
