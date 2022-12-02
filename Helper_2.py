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
import pandas as pd
from datetime import datetime

four_pm_time = datetime.strptime('16:00', '%H:%M').time()
five_pm_time = datetime.strptime('17:00', '%H:%M').time()

global_student_id = 0  # Глобальная для всего модуля переменная - код студента


def excel_export(df_restructured, table_name, sheet_name):
    """Экспортируем датафрейм в таблицу excel """
    df_restructured.to_excel(table_name, sheet_name=sheet_name)


def excel_import(table_name: str, sheet_name: str):
    """Импортируем таблицу в датафрейм"""
    return pd.read_excel(table_name, sheet_name)  # Импортируем исходную таблицу в датафрейм


class Expert:
    """Эксперт по расписанию"""

    def __init__(self):
        self.schedules_number = 1
        self.lessons_number = 3
        self.schedules = []  # Набор расписаний

    def __repr__(self):
        return f'Расписание {self.schedules_number}'

    def load_schedules(self, schedules_number=1):
        """Сбор"""
        self.schedules_number = schedules_number
        for schedule_id in range(self.schedules_number):
            sch = Schedule(schedule_id + 1, lessons_number=self.lessons_number)
            sch.load()
            self.schedules.append(sch)

    def handling(self):
        """"Обработка"""
        pass

    def save(self):
        """Сохранение"""
        pass

    def publish(self):
        """Публикация"""
        pass


class Alert:
    """Предупреждение"""

    def __init__(self, id=1):
        self.schedule = None  # Ссылка на родителя
        self.id = id  # Номер предупреждения
        self.description = ''  # Описание

    def seminar_befor_lecture(self):
        """"Семинар до лекции"""
        pass


class Schedule:
    """Расписание"""

    def __init__(self, id=1, lessons_number=1):
        self.alert = None  # Предупреждение
        self.id = id  # Номер расписания
        self.lessons_number = lessons_number  # Число занятий
        self.lessons = []  # Набор занятий
        self.alerts = []  # Список предупреждений
        self.year = ''
        self.term = ''

    def create_objects(self):
        """Создает набор объектов Trader"""
        self.alert = Alert()  # Создаем дочерний объект Предупреждение
        self.alert.schedule = self  # Ссылаемся в нем на родителя Расписание

    def __repr__(self):
        return f'Расписание {self.id} Занятий {len(self.lessons)}'

    def load(self, ):
        """Создает набор объектов """
        for n in range(self.lessons_number):
            n += 1
            self.lessons.append(Lesson(Lesson.lecture, n, Discipline(n), 1, n, Teacher(n), Group(n), Building(n),
                                       Auditorium(n), Pair(n)))  # Добавляем лекцию
            self.lessons.append(Lesson(Lesson.seminar, n, Discipline(n), 1, n, Teacher(n), Group(n), Building(n),
                                       Auditorium(n), Pair(n + 1)))  # семинар

    def alerts_handling(self):
        """"Обработка предупреждений"""
        for alert in self.alerts:
            alert.handling()


@dataclass
class Error:
    """Ошибка"""
    name = ''
    output = ''


class Lesson:
    """Занятие"""
    lecture = "Лекция"
    seminar = "Семинар"

    def __init__(self, types, number, discipline, week, day, teacher, group, building, auditorium, pair):  #
        # self.id = id  # Код занятия
        self.number = number  # Порядковый номер занятия в дисциплине
        self.type = types  # Тип занятия: лекция или практическое занятие
        self.discipline = discipline
        self.week = week
        self.day = day
        self.pair = pair
        self.teacher = teacher
        self.group = group
        self.building = building
        self.auditorium = auditorium
        self.face_to_face: bool = True

    def __repr__(self):
        return f'{self.type} {self.number} {self.discipline} {self.teacher} {self.group} ' \
               f'{self.building},{self.auditorium} Неделя {self.week} День {self.day} {self.pair} '


class Teacher:
    """Преподаватель"""

    def __init__(self, id):  # Код преподавателя
        self.id = id
        self.e_mail: str = f'teacher_{id}@mail.com'

    def __repr__(self):
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


class Resource:
    """Ресурсы"""

    def __init__(self):
        self.lessons = []  # Набор занятий
        self.teachers = pd.DataFrame(columns=['name', 'e_mail'])
        self.groups = pd.DataFrame(columns=['name'])
        self.students = pd.DataFrame(columns=['group', 'name', 'e_mail'])
        self.buildings = pd.DataFrame(columns=['name'])
        self.auditoriums = pd.DataFrame(columns=['building', 'name'])

    def create_data_frames(self):
        """Создает набор объектов Resurce"""
        for teacher_id in range(1, 7):
            teacher: pd.Series = pd.Series({'name': f'Преподаватель {teacher_id}',
                                            'e_mail': f'teacher_{teacher_id}@university.com'})
            self.teachers = pd.concat([self.teachers, teacher.to_frame().T], ignore_index=True)
        print(self.teachers)
        for group_id in range(1, 7):
            group = pd.Series({'name': f'Группа {group_id}'})
            self.groups = pd.concat([self.groups, group.to_frame().T], ignore_index=True)
        # print(self.groups)
        for group_id in range(len(self.groups)):  # В каждой группе
            for student_id_in_group in range(1, 11):  # создаем 10 студентов
                student_id = int(str(group_id) + str(student_id_in_group - 1)) + 1  # Создаем уникальный номер студента
                student = pd.Series({'group': self.groups['name'][group_id],  # Создаем строку данных студента
                                     'name': f'Студент {student_id}',
                                     'e_mail': f'student_{student_id}@university.com'})
                self.students = pd.concat([self.students, student.to_frame().T], ignore_index=True)  # Сохраняем
        # print(self.students)  # Выводим на экран
        for building_id in range(1, 4):
            building = pd.Series({'name': f'Корпус {building_id}'})
            self.buildings = pd.concat([self.buildings, building.to_frame().T], ignore_index=True)
        # print(self.buildings)
        for building_id in range(len(self.buildings)):
            for auditorium_id in range(1, 7):
                # auditorium = int(str(building) + str(auditoriums_in_building - 1)) + 1
                auditorium = pd.Series({'building': self.buildings['name'][building_id],
                                        'name': f'Аудитория {auditorium_id}'})
                self.auditoriums = pd.concat([self.auditoriums, auditorium.to_frame().T], ignore_index=True)
        # print(self.auditoriums)


if __name__ == '__main__':
    expert = Expert()  # Создаем эксперта по расписанию и одно расписание
    expert.load_schedules(1)  # Эксперт загружает два варианта расписания
    for schedule in expert.schedules:  # Для каждого расписания выводим
        schedule.create_objects()
        print(schedule)  # его номер и число занятий
        for lesson in schedule.lessons:  # Для каждого занятия выводим
            print(lesson)

    # print(teacher_2)
    # print(group_1)
    # print(group_1.students)
    # print(group_6)
    # print(group_6.students)
