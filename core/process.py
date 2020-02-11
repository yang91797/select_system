from conf import settings
from core.main import School
from core.main import Course
from core.main import Student_class
from core.main import Teacher
from core.main import Student
from core.main import Root


class Views:
    def __init__(self):
        self.s_func = [
            ('注册', Student.create),
            ('交学费', Student.pay),
            ('选择班级', Student.clas)
        ]
        self.t_func = [
            ('上课', Teacher.go_class),
            ('查看班级学员', Teacher.look_student),
            ('修改学员成绩', Teacher.c_grade)
        ]
        # self.r_func = [
        #     ('讲师', Root().add_teacher),
        #     ('课程', Root().add_course),
        #     ('创建班级', Root().add_class),
        #     ('创建校区', Root().add_school)
        # ]
        self.r_func = [
            ('讲师', [AddOrView, 'teacher']),
            ('课程', [AddOrView, 'course']),
            ('班级', [AddOrView, 'class']),
            ('校区', [AddOrView, 'school'])
        ]

    def student(self):
        index = 0
        for index, content in enumerate(self.s_func):
            print(index+1, content[0])
        choice = input('请选择:').strip()
        if choice.isdigit() and 0 < int(choice) <= index+1:
            choice = int(choice) - 1
            self.s_func[choice][1]()

    def teacher(self):

        func(self.t_func)

    def root(self):
        func(self.r_func)


class AddOrView:
    def __init__(self, arg):
        self.arg = arg
        self.func = [
            ('查看', [self.view, self.arg]),
            ('创建', [self.create, self.arg])
        ]

        func(self.func)

    def view(self, arg):

        Root().get_func("view_"+arg)

    def create(self, arg):
        Root().get_func("add_"+arg)


def func(args):             # 功能分发

    while True:
        print('按b返回上一层'.center(30, '-'))

        for index, content in enumerate(args):
            print(index+1, content[0])
        choice = input('请选择》》').strip()
        if choice.isdigit() and 0 < int(choice) <= len(args):
            choice = int(choice) - 1
            if isinstance(args[choice][1], list):
                args[choice][1][0](args[choice][1][1])
            else:
             args[choice][1]()

        elif choice == 'b':
            return
        else:
            print('请重新选择')




