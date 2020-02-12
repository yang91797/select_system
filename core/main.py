import time
from libs import common
from conf import settings


class RootMetaclass(type):
    """
    元类，在Root类中加入
    __create__和__view__两个参数，
    分别表示添加和查看功能
    """
    def __new__(cls, name, bases, attrs):
        attrs['__create__'] = []
        attrs['__view__'] = []
        for k, v in attrs.items():
            if 'add_' in k:
                attrs['__create__'].append(k)
            elif 'view_' in k:
                attrs['__view__'].append(k)

        return type.__new__(cls, name, bases, attrs)


class Create:  # 创建讲师，学生角色的父类
    information = {}

    def sign(self):
        School.tell_info()
        location = input('请输入所在校区：').strip()
        name = input('请输入姓名：').strip()
        sex = input('请输入性别：').strip()
        age = input('请输入年龄：').strip()
        print("注册成功!!!")
        self.information['所在校区'] = location
        self.information['姓名'] = name
        self.information['性别'] = sex
        self.information['年龄'] = age
        for key in self.information:
            if not self.information[key]:
                print('请完善所有信息')
                return

        return self.information


class School:  # 学校类
    def __init__(self, location=None):
        self.location = location

    def add(self):  # 新增校区
        self.location = input("请输入新建校区名称：")
        location_list = common.information(settings.school_path, 'rb')
        location_list.append(self.location)
        common.information(settings.school_path, 'wb', location_list)

    @classmethod
    def tell_info(cls):  # 查询校区
        print('校区'.center(50, '-'))
        information = common.information(settings.school_path, 'rb')
        for content in information:
            print(content)


class Course(School):  # 课程类
    dic_list = []

    def __init__(self, location, course_name, course_price, course_period):
        super().__init__(location)
        self.course_name = course_name
        self.course_price = course_price
        self.course_period = course_period

    @classmethod
    def tell_info(cls, screen=None):  # 查询课程信息
        course_list = common.information(settings.course_path, m='rb')
        print('''
            —————已开课程—————
        ''')
        for dic in course_list:
            if not screen:
                print('''
                校区：%s  课程名称：%s  课程价钱：%s  课程周期：%s
                ''' % (dic['开课校区'], dic['课程名称'], dic['课程价钱'], dic['课程周期'])
                      )
            if screen == dic['课程名称']:  # 条件筛选

                cls.dic_list.append(dic)
                return cls.dic_list
        return course_list

    @classmethod
    def create(cls, arg):
        """
        创建课程
        :param arg:
        :return:
        """
        School.tell_info()  # 显示校区
        course_dic = {}
        course_school = input('请输入开课校区：').strip()
        course_name = input('请输入课程名称：').strip()
        course_price = input('请输入课程价钱：').strip()
        course_period = input('请输入课程周期：').strip()
        course_dic['开课校区'] = course_school
        course_dic['课程名称'] = course_name
        course_dic['课程价钱'] = course_price
        course_dic['课程周期'] = course_period
        for key in course_dic:
            if not course_dic[key]:
                print('请完善所有信息')
                return
        arg.append(course_dic)
        common.information(settings.course_path, 'wb', arg)
        print('已添加课程')


class Student_class(School):  # 班级类
    def __init__(self, location, class_name):
        super().__init__(location)
        self.class_name = class_name

    @classmethod
    def tell_info(cls, screen=None):
        flag = True
        information = common.information(settings.class_path, 'rb')

        for dic in information:
            if not screen:  # 条件筛选
                show = '校区：%s    班级名称：%s    讲师：%s' % (dic['校区'], dic['班级名称'], dic['讲师'])
                flag = False
                yield show
            elif screen == dic['校区']:
                show = '校区：%s  班级名称：%s  讲师：%s ' % (dic['校区'], dic['班级名称'], dic['讲师'])
                flag = False
                yield show
            elif screen == dic['班级名称']:
                flag = False
                yield dic
            elif screen == dic['讲师']:
                flag = False
                yield dic
        if flag:
            print('无此内容,重新选择')
            return
        return information

    @classmethod
    def add_class(cls):  # 创建班级
        class_location = input('请输入校区:').strip()
        class_name = input('请输入班级名称:').strip()
        class_dict = {}
        course_name = None
        info = Tell_info(settings.teacher_path).message()  # 查询讲师信息
        teacher = input('请选择讲师:').strip()
        for dic in info:
            if dic['所在校区'] == class_location and dic['姓名'] == teacher:
                course_name = dic['所教课程名']
        class_dict['校区'] = class_location
        class_dict['班级名称'] = class_name
        class_dict['讲师'] = teacher
        class_dict['课程'] = course_name
        try:
            class_list = common.information(settings.class_path, 'rb')
        except Exception:
            class_list = []
        for key in class_dict:
            if not class_dict[key]:
                print('请完善所有信息')
                return
        class_list.append(class_dict)
        common.information(settings.class_path, 'wb', class_list)
        print('已新增班级')


class Teacher(Create):  # 老师类

    def tell_info(self, name=None, t_name=None):  # 查看
        flag = False
        if not name:
            t_name = input('请输入讲师名：').strip()

        info = common.information(settings.teacher_path, 'rb')
        for dic in info:
            if dic['姓名'] == t_name:
                flag = True
                break
        else:
            yield info
        if flag:
            class_info = Student_class.tell_info(t_name)
            yield class_info

    @classmethod
    def add(cls):  # 创建讲师信息
        # information_list = []
        information_list = common.information(settings.teacher_path, 'rb')
        information = super().sign(cls)
        course_name = input('请输入所教课程名称：').strip()
        information['所教课程名'] = course_name
        information_list.append(information)
        common.information(settings.teacher_path, 'wb', information_list)

    @classmethod
    def go_class(cls):  # 上课
        class_list = []
        info = Teacher().tell_info()  # 生成器
        for i in info:
            for dic in i:
                print('班级:', dic['班级名称'])
                class_list.append(dic['班级名称'])
        choice = input('请选择上课班级：').strip()
        if choice in class_list:
            print('已开始上课...')
            time.sleep(3)

    @classmethod
    def look_student(cls):  # 查看所教学员
        flag = True
        info = Teacher().tell_info()
        for i in info:
            for dic in i:
                print(dic['班级名称'])
                s_info = Student.tell_info(dic['班级名称'])
                for arg in s_info:
                    print('班级：%s  姓名：%s  分数：%s  学费：%s' % (arg['所在班级'], arg['姓名'], arg['分数'], arg['支付']))
                    flag = False
        if flag:
            print('暂无学员')

    @classmethod
    def c_grade(cls):  # 修改成绩
        info = Teacher().tell_info()
        s_info = []
        for i in info:
            for dic in i:
                s_info = Student.tell_info(dic['班级名称'])
        for arg in s_info:
            print('班级：%s  姓名：%s  分数：%s' % (arg['所在班级'], arg['姓名'], arg['分数']))
        s_name = input('输入学生姓名：').strip()
        s_info = common.information(settings.student_path, 'rb')
        for item in s_info:
            if item['姓名'] == s_name:
                grade = input('输入分数：').strip()
                item['分数'] = int(grade)
        common.information(settings.student_path, 'wb', s_info)
        print('已修改成绩')


class Student(Create):  # 学生类
    student_list = []

    def __init__(self, s_name, sex, age):
        self.s_name = s_name
        self.sex = sex
        self.age = age

    @classmethod
    def tell_info(cls, screen=None):
        student_info = common.information(settings.student_path, 'rb')
        for dic in student_info:
            if not screen:
                return student_info
            if screen == dic['所在班级']:
                cls.student_list.append(dic)
                return cls.student_list

    @classmethod
    def create(cls):  # 增加学生信息  注册
        student_list = common.information(settings.student_path, 'rb')
        information = super().sign(cls)  # 执行父类sign方法
        if Student_class.tell_info(information['所在校区']):
            information['所在班级'] = None
            information['支付'] = 0
            information['分数'] = 0
            student_list.append(information)
            common.information(settings.student_path, 'wb', student_list)

    @classmethod
    def pay(cls):  # 支付学费
        name = input('请输入姓名：').strip()
        location = input('请输入所在校区：').strip()
        student_list = common.information(settings.student_path, 'rb')
        for dic in student_list:
            if name == dic['姓名'] and location == dic['所在校区']:
                if int(dic['支付']) >= 0:
                    print('暂无可交费用')
                else:
                    print('姓名：%s  班级：%s  学费：%s' % (name, dic['所在班级'], dic['支付']))
                    money = input('支付费用：').strip()
                    dic['支付'] = str(int(dic['支付']) + int(money))
                    print('已支付学费%s元' % money)
                    common.information(settings.student_path, 'wb', student_list)

    @classmethod
    def clas(cls):  # 选择班级
        name = input('请输入你的姓名：').strip()
        School.tell_info()  # 显示已有校区
        school_name = input('请输入所在校区：').strip()
        foo = Student_class.tell_info(school_name)  # 显示校区的班级
        for i in foo:
            print(i)
        class_name = input('请选择班级：').strip()
        try:
            class_info = Student_class.tell_info(class_name)  # 查询班级，拿到课程信息
            course = None
            price = 0
            for i in class_info:
                course = i['课程']
            course_info = Course.tell_info(course)  # 查询课程，拿到价格
            for dic in course_info:
                price = dic['课程价钱']
            student_list = common.information(settings.student_path, 'rb')
            for dic in student_list:
                if name == dic['姓名'] and school_name == dic['所在校区']:
                    dic['所在班级'] = class_name  # 添加班级信息
                    dic['支付'] = str(int(dic['支付']) - int(price))  # 添加支付信息
                    common.information(settings.student_path, 'wb', student_list)
        except Exception:
            pass


class Root(object, metaclass=RootMetaclass):  # 管理员
    def get_func(self, callback):
        eval("self.{}()".format(callback))

    def add_teacher(self):  # 创建讲师
        Teacher.add()

    def add_course(self):  # 添加课程
        try:
            information = Course.tell_info()
            for i in information:
                information = i
        except Exception as e:
            information = []
        Course.create(information)

    def add_class(self):  # 创建班级
        foo = Student_class.tell_info()  # 显示已有班级
        for i in foo:
            print(i)
        School.tell_info()  # 显示校区
        Student_class.add_class()

    def add_school(self):
        School().add()

    def view_teacher(self):
        """
        查看老师
        :return:
        """

        teach_info = Teacher().tell_info(name='All')
        for item in teach_info:
            for i in item:
                print("所在校区：%s  姓名：%s  性别：%s  年龄：%s 所教课程：%s" % (i.get("所在校区"), i.get("姓名"),
                                                                i.get("性别"), i.get("年龄"), i.get("所教课程名")))

    def view_course(self):
        """
        查看课程
        :return:
        """
        Course.tell_info()

    def view_class(self):
        """
        查看班级
        :return:
        """
        info = Student_class.tell_info()
        for item in info:
            print(item)

    def view_school(self):
        """
        查看校区
        :return:
        """
        School.tell_info()  # 显示校区


class Tell_info:  # 查看文件信息

    def __init__(self, path):
        self.path = path

    def message(self):
        information = common.information(self.path, 'rb')
        for dic in information:
            print(''.center(50, '-'))
            for key in dic:
                print(key, dic[key], sep=':')

        return information
