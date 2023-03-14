"""
@author: lataf 
@file: Helper.py 
@time: 08.11.2022 11:34
Модуль отвечает за предупреждения и ошибки при составлении расписания
UML схемы: Scheduler_classes.puml, Scheduler_usecase.puml
Сценарий работы модуля:Scheduler_scenario.docx
Тест модуля находится в папке tests.

"""
from dataclasses import dataclass

global_student_id = 0  # Глобальная для всего модуля переменная - код студента


class Expert:
    """Эксперт по расписанию - создает расписания"""

    def __init__(self):
        self.schedules_number = 1  # Число вариантов расписания
        self.lessons_number = 3  # Номеров занятий в расписании ( Лекция и семинар могут иметь один номер)
        self.schedules = []  # Набор расписаний

    def __repr__(self):
        return f'Расписание {self.schedules_number}'

    def load_schedules(self, schedules_number=1):
        """Сбор данных"""
        self.schedules_number = schedules_number  # Количество вариантов расписания
        for schedule_id in range(self.schedules_number):  # Для каждого последующего номера
            sch = Schedule(schedule_id + 1, lessons_number=self.lessons_number)  # создаем расписание
            sch.load()  # и загружаем в него данные
            self.schedules.append(sch)  # Добавляем расписание в список расписаний

    def handling(self):
        """"Обработка"""
        pass

    def save(self):
        """Сохранение"""
        pass

    def publish(self):
        """Публикация"""
        pass


class Schedule:
    """Расписание - загрузка объектов в расписание"""

    def __init__(self, id=1, lessons_number=1):
        self.alert = None  # Предупреждение
        self.id = id  # Номер расписания
        self.lessons_number = lessons_number  # Число занятий
        self.lessons = []  # Набор занятий
        self.alerts = []  # Список предупреждений
        self.year = 0  # Год расписания
        self.term = 0  # Семестр расписания


def create_objects(self):
    """Создает набор объектов Trader"""
    self.alert = Alert()  # Создаем дочерний объект Предупреждение
    self.alert.schedule = self  # Ссылаемся в нем на родителя Расписание


def __repr__(self):
    """Переопределение вывода на печать"""
    return f'    Расписание {self.id} Занятий {len(self.lessons)}'


def load(self, ):
    """Загружает набор объектов - смотри Scheduler_classes.puml"""
    for n in range(self.lessons_number):  # Для каждого номера занятия
        n += 1
        self.lessons.append(Lesson(Lesson.seminar, n, Discipline(n), 1, 1, Teacher(n), Group(n), Building(n),
                                   Auditorium(n), Pair(n)))  # добавляем семинар, а затем
        self.lessons.append(Lesson(Lesson.lecture, n, Discipline(n), 1, 1, Teacher(n), Group(n), Building(n),
                                   Auditorium(n), Pair(n + 1)))  # добавляем лекцию


def alerts_handling(self):
    """"Обработка предупреждений"""
    self.alert.seminar_befor_lecture()  # Семинар проводится до лекции
    self.alert.many_lectures_in_one_day_1()  # Много лекций (больше двух) подряд - пока не создана


class Lesson:
    """Занятие - связывает свои объекты"""
    lecture = "Лекция"
    seminar = "Семинар"

    def __init__(self, types, number, discipline, week, day, teacher, group, building, auditorium, pair):  #
        # self.id = id  # Код занятия
        self.number = number  # Порядковый номер занятия в дисциплине
        self.type = types  # Тип занятия: лекция или практическое занятие
        self.discipline = discipline  # Дисциплина
        self.week = week  # Неделя
        self.day = day  # День недели
        self.pair = pair  # Пара
        self.teacher = teacher  # Преподаватель
        self.group = group  # Группа
        self.building = building  # Корпус
        self.auditorium = auditorium  # Аудитория
        self.face_to_face: bool = True  # Занятие очное

    def __repr__(self):
        """Переопределение вывода на печать"""
        return f'{self.type} {self.number} {self.discipline} {self.teacher} {self.group} ' \
               f'{self.building},{self.auditorium} Неделя {self.week} День {self.day} {self.pair} '


class Alert:
    """Предупреждение - проверка расписания на предупреждения"""

    def __init__(self):
        self.schedule = None  # Ссылка на родителя
        self.last_seminar_number = 0  # Номер семинара
        self.lecturepair = None


def seminar_befor_lecture(self):
    """"Семинар проводится до лекции"""
    for les in self.schedule.lessons:  # Для всех занятий в одном расписании
        if les.type == Lesson.seminar:  # если занятие семинар,
            self.last_seminar_number = les.number  # то запоминаем его номер
        elif les.type == Lesson.lecture and self.last_seminar_number >= les.number:  # м если номер лекции больше
            # или равен номеру семинара
            print(f"Лекция {les.number} позже Семинара {self.last_seminar_number} ")  # то пишем предупреждение


def many_lectures_in_one_day(self):
    """"Много лекций (больше двух) подряд"""
    for les in self.schedule.lessons:
        if les.type == Lesson.lecture:
            self.lecturepair = les.pair
        elif les.type == Lesson.lecture and self.lecturepair != les.pair:
            self.fulllecturestatus = True  # Статус отображает максимальное количество лекций в день
        elif les.type == Lesson.lecture and self.fulllecturestatus == True:
            print("В этот день много лекций (больше двух")


@dataclass
class Error:
    """Ошибка"""
    name = ''
    output = ''


class Teacher:
    """Преподаватель"""

    def __init__(self, id):  # Код преподавателя
        self.id = id
        self.e_mail: str = f'teacher_{id}@mail.com'  # Генерация почты

    def __repr__(self):
        """Переопределение вывода на печать"""
        return f'Преподаватель {self.id}'


class Discipline:
    """Дисциплина"""

    def __init__(self, id: int = 1):  # Код дисциплины
        self.id = id

    def __repr__(self):
        return f'Дисциплина {self.id}'


class Pair:
    """Пара"""

    def __init__(self, id: int = 1):  # Код пары
        self.id = id

    def __repr__(self):
        return f'Пара {self.id}'


class Student:
    """Студент"""

    def __init__(self, id):
        self.id: int = id
        self.e_mail_id: int = id

    def __repr__(self):
        return f'Студент {self.id}, student_{self.e_mail_id}@mail.com '


class Group:
    """Группа"""

    def __init__(self, id: int):
        self.id: int = id
        self.students = []

    def __repr__(self):
        return f'Группа {self.id}'

    def create_students(self, st_number):  # Число студентов в группе
        global global_student_id  # Глобальная для всего модуля переменная - код студента
        for student_id in range(st_number):
            global_student_id += 1
            student = Student(global_student_id)
            self.students.append(student)


class Building:
    """Корпус"""

    def __init__(self, id: int):
        self.id: int = id

    def __repr__(self):
        return f'Корпус {self.id}'


class Auditorium:
    """Аудитория"""

    def __init__(self, id: int):
        self.id: int = id

    def __repr__(self):
        return f'Аудитория {self.id}'


class Transfer:
    """Трансфер"""
    route = ''
    time = ''


if __name__ == '__main__':
    expert = Expert()  # Создаем эксперта по расписанию и одно расписание
    expert.load_schedules(1)  # Эксперт загружает один вариант расписания
    for schedule in expert.schedules:  # Для каждого расписания выводим
        schedule.create_objects()  # Создаем связанные с родителем дочерние объекты
        print(schedule)  # его номер и число занятий
        for lesson in schedule.lessons:  # Для каждого занятия выводим
            print(lesson)  # Объекты занятия (см. переопределение печати)
    for schedule in expert.schedules:  # Для каждого расписания выводим
        print(f'    Предупреждения по расписанию {schedule.id}')
        schedule.alerts_handling()  # Проверяем расписание на предупреждения
# print(teacher_2)
# print(group_1)
# print(group_1.students)
# print(group_6)
# print(group_6.students)

# SyntaxError: multiple
# statements
# found
# while compiling a single statement
