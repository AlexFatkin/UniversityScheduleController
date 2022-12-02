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

global_student_id = 0  # Глобальная для всего модуля переменная - код студента


def excel_export(df_restructured, table_name, sheet_name):
    """Экспортируем датафрейм в таблицу excel """
    df_restructured.to_excel(table_name, sheet_name=sheet_name)


def excel_import(table_name: str, sheet_name: str):
    """Импортируем таблицу в датафрейм"""
    return pd.read_excel(table_name, sheet_name)  # Импортируем исходную таблицу в датафрейм


class Expert:
    """Эксперт по расписанию"""

    def load(self):
        """Сбор"""
        pass

    def handling(self):
        """"Обработка"""
        pass

    def save(self):
        """Сохранение"""
        pass

    def publish(self):
        """Публикация"""
        pass


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
        print(self.groups)
        for group_id in range(len(self.groups)):  # В каждой группе
            for student_id_in_group in range(1, 11):  # создаем 10 студентов
                student_id = int(str(group_id) + str(student_id_in_group - 1)) + 1  # Создаем уникальный номер студента
                student = pd.Series({'group': self.groups['name'][group_id],  # Создаем строку данных студента
                                     'name': f'Студент {student_id}',
                                     'e_mail': f'student_{student_id}@university.com'})
                self.students = pd.concat([self.students, student.to_frame().T], ignore_index=True)  # Сохраняем
        print(self.students)  # Выводим на экран
        for building_id in range(1, 4):
            building = pd.Series({'name': f'Корпус {building_id}'})
            self.buildings = pd.concat([self.buildings, building.to_frame().T], ignore_index=True)
        print(self.buildings)
        for building_id in range(len(self.buildings)):
            for auditorium_id in range(1, 7):
                # auditorium = int(str(building) + str(auditoriums_in_building - 1)) + 1
                auditorium = pd.Series({'building': self.buildings['name'][building_id],
                                        'name': f'Аудитория {auditorium_id}'})
                self.auditoriums = pd.concat([self.auditoriums, auditorium.to_frame().T], ignore_index=True)
        print(self.auditoriums)


class Schedule:
    """Расписание"""

    def __init__(self):
        self.lessons = []  # Набор занятий
        self.year = ''
        self.term = ''

    def create_objects(self):
        """Создает набор объектов Resurce"""
        for n in range(1, 7):
            self.lessons.append(Lesson('Лекция', n))  # Добавляем лекцию
            self.lessons.append(Lesson('Семинар', n))  # Добавляем семинар

    def run(self):
        pass


@dataclass
class Error:
    """Ошибка"""
    name = ''
    output = ''


@dataclass
class Warnings:
    """Предупреждение"""
    name = ''
    output = ''


class Lesson:
    """Занятие"""

    def __init__(self, types, number: int):  # : Handler
        self.type = types
        self.number = number
        self.face_to_face: bool = True

    def message(self):
        pass


class Teacher:
    """Преподаватель"""

    def __init__(self, id):
        self.name: str = f'Преподаватель {id}'
        self.e_mail: str = f'teacher_{id}@mail.com'

    def __repr__(self):
        return f'{self.name}, {self.e_mail}'


class Discipline:
    """Дисциплина"""
    name = ''


class Pair:
    """Пара"""
    name = ''
    begin = ''
    end = ''


class Student:
    """Студент"""

    def __init__(self, id):
        self.id: int = id
        self.e_mail_id: int = id

    def __repr__(self):
        return f'Студент {self.id}, student_{self.e_mail_id}@mail.com '


class Group:
    """Группа"""

    def __init__(self, id: int, student_number: int):
        self.id: int = id
        self.students = []
        self.create_students(student_number)

    def __repr__(self):
        return f'Группа {self.id}'

    def create_students(self, st_number):
        global global_student_id  # Глобальная для всего модуля переменная - код студента
        for student_id in range(st_number):
            global_student_id += 1
            student = Student(global_student_id)
            self.students.append(student)


class Building:
    """Корпус"""
    name = ''


class Auditorium:
    """Аудитория"""
    name = ''


class Transfer:
    """Трансфер"""
    route = ''
    time = ''


if __name__ == '__main__':
    resource = Resource()
    resource.create_data_frames()

