"""
@author: lataf 
@file: Helper_7.py
@time: 06.01.2023 17:59
Модуль отвечает за предупреждения и ошибки при составлении расписания
8. Построчная обработка расписания из формы в Excel
UML схемы: Scheduler_classes_2.puml, Scheduler_usecase.puml
Сценарий работы модуля:Scheduler_scenario_2.docx
Тест модуля находится в папке tests.

"""
from dataclasses import dataclass
import pandas as pd

global_student_id = 0  # Глобальная для всего модуля переменная - код студента
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)


def save_in_excel(df_restructured, table_name, sheet_name):
    """Сохраняем данные датафрейма в таблице excel"""
    df_restructured.to_excel(table_name, sheet_name=sheet_name)  # Сохраняем данные датафрейма в таблице excel


def load_from_excel(table_name: str, sheet_name: str):
    """Загружаем данные из таблицы excel в датафрейм"""
    return pd.read_excel(table_name, sheet_name, index_col=0)  # Загружаем данные из таблицы excel в датафрейм


class Expert:
    """Эксперт по расписанию - создает расписания"""

    def __init__(self):
        self.schedules_number = 1  # Число вариантов расписания
        self.lessons_number = 3  # Номеров занятий в расписании ( Лекция и семинар могут иметь один номер)
        self.schedules = []  # Набор расписаний
        self.pair_df = pd.DataFrame

    def __repr__(self):
        return f'Расписание {self.schedules_number}'

    def load_pair(self):
        """Загружаем значения пар"""
        self.pair_df = load_from_excel(f'input/Пары.xlsx', 'Лист1')
        print(self.pair_df)

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


def data_frame_to_schedule_object(data_frame: pd.DataFrame):
    """Конвертация из DataFrame в класс  Scheduler"""
    return data_frame


class Schedule:
    """Расписание - загрузка объектов в расписание"""

    def __init__(self, id=1, lessons_number=1):
        self.file_path = ''
        self.df = None
        self.schedule = {}
        self.groups = []
        self.weeks = []
        self.days = []
        self.pairs = []
        self.lessons_types = []
        self.lessons = []
        self.disciplines = []
        self.teachers = []
        self.buildings = []
        self.audiences = []
        self.schedule_df = pd.DataFrame(columns=['group', 'week', 'day', 'pair', 'lesson', 'discipline',
                                                 'teacher', 'building', 'auditory'])
        self.alert = None  # Предупреждение
        self.id = id  # Номер расписания
        self.name = 'без ошибок'
        self.lessons_number = lessons_number  # Число занятий
        self.lessons_numbers = []  # Набор номеров занятий
        self.alerts = []  # Список предупреждений
        self.year = 0  # Год расписания
        self.term = 0  # Семестр расписания

    def __repr__(self):
        """Переопределение вывода на печать"""
        return f'    Расписание №{self.id} Занятий {len(self.lessons)}'

    def create_objects(self):
        """Создает набор объектов Trader"""
        self.alert = Alert()  # Создаем дочерний объект Предупреждение
        self.alert.schedule = self  # Ссылаемся в нем на родителя Расписание

    def load(self):
        """Загружает набор объектов - смотри Scheduler_classes.puml"""
        for n in range(self.lessons_number):  # Для каждого номера занятия
            n += 1
            self.lessons.append(Lesson(Lesson.lecture, n, Discipline(n), 1, n, Teacher(n), Group(n), Building(n),
                                       Auditorium(1), Pair(n)))  # добавляем лекцию, а затем
            self.lessons.append(Lesson(Lesson.seminar, n, Discipline(n), 1, n + 1, Teacher(n), Group(n), Building(n),
                                       Auditorium(2), Pair(n + 1)))  # добавляем семинар
    #
    # def create_df(self):
    #     """Извлекаем данные из занятий датафрейм и сохраняем в Excel таблицу """
    #     self.file_path = f' output/Расписание №{self.id} {self.name}.xlsx'
    #     for les in self.lessons:
    #         self.groups.append(les.group)
    #         self.weeks.append(les.week)
    #         self.days.append(les.day)
    #         self.pairs.append(les.pair)
    #         self.lessons_types.append(les.type)
    #         self.lessons_numbers.append(les.number)
    #         self.disciplines.append(les.discipline)
    #         self.teachers.append(les.teacher)
    #         self.buildings.append(les.building)
    #         self.audiences.append(les.auditorium)
    #     self.schedule = {'group': self.groups,
    #                      'week': self.weeks, 'day': self.days, 'pair': self.pairs,
    #                      'lesson': self.lessons_numbers, 'type': self.lessons_types,
    #                      'discipline': self.disciplines, "teacher": self.teachers,
    #                      'building': self.buildings, 'auditory': self.audiences,
    #                      }  # Создаем словарь расписания
    #     self.schedule_df = pd.DataFrame(self.schedule)  # Словарь конвертируем в датафрейм расписания
    #     print(self.schedule_df)  # Показываем датафрейм расписания
    #     save_in_excel(self.schedule_df, self.file_path, 'sheet_1')  # Экспортируем датафрейм в scheduler.xlsx

    def load_df(self):
        """Извлекаем данные Excel таблицы из и сохраняем в датафрейм"""
        table_name = 'Расписание №3 с ошибкой'
        self.file_path = f'input/{table_name}.xlsx'
        schedule_df = load_from_excel(self.file_path, 'sheet_1')
        print(table_name)
        print(schedule_df)
        return schedule_df

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
        self.last_seminar_number = 0  # Номер последнего семинара
        self.lecture_pair = 0  # Начальное число лекций (для счетчика)
        self.max_lecture_pair = 2  # Максимальное число пар лекций в один день
        self.week = 0  # Номер недели
        self.day = 0  # Номер дня недели (1 - Пн, 2 - Вт и т.д.)

    def seminar_befor_lecture(self):
        """"Семинар проводится до лекции"""
        for les in self.schedule.lessons:  # Для всех занятий в одном расписании
            if les.type == Lesson.seminar:  # если занятие семинар,
                self.last_seminar_number = les.number  # то запоминаем его номер
            elif les.type == Lesson.lecture and self.last_seminar_number >= les.number:  # и если номер лекции больше
                # или равен номеру семинара, то
                print(f"Лекция №{les.number} позже Семинара №{self.last_seminar_number}"  # выводим предупреждение,
                      f" в день {les.day} недели {les.week}")  # день и неделю

    def many_lectures_in_one_day_1(self):
        """"Много лекций (больше двух) в один день"""
        for les in self.schedule.lessons:  # Для всех занятий в одном расписании
            if les.type == Lesson.lecture and self.day == les.day and self.week == les.week:  # если занятие лекция и
                # у него совпадает предыдущие день и номер недели при сравнении, то
                self.lecture_pair += 1  # увеличиваем счетчик числа лекций на 1
            self.week = les.week  # Запоминаем номер недели для последующего сравнения
            self.day = les.day  # Запоминаем номер дня недели для последующего сравнения
        if self.lecture_pair > self.max_lecture_pair:  # Если число лекций в день больше установленного, то
            print(f"Лекций {self.lecture_pair} (больше, чем {self.max_lecture_pair}) "  # выводим предупреждение, 
                  f"в день {self.day} недели {self.week}")  # день и неделю
            self.lecture_pair = 0  # Восстанавливаем начальное число счетчика лекций


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


class Auditorium:
    """Аудитория"""

    def __init__(self, id: int):
        self.id: int = id

    def __repr__(self):
        return f'Аудитория {self.id}'


class Building:
    """Корпус"""

    def __init__(self, id: int):
        self.id: int = id

    def __repr__(self):
        return f'Корпус {self.id}'
#
#
# class Transfer:
#     """Трансфер"""
#     route = ''
#     time = ''


# class Resource:
#     """Ресурсы"""
#
#     def __init__(self):
#         self.lessons = []  # Набор занятий
#         self.teachers = pd.DataFrame(columns=['name', 'e_mail'])
#         self.groups = pd.DataFrame(columns=['name'])
#         self.students = pd.DataFrame(columns=['group', 'name', 'e_mail'])
#         self.buildings = pd.DataFrame(columns=['name'])
#         self.auditoriums = pd.DataFrame(columns=['building', 'name'])
#
#     def create_data_frames(self):
#         """Создает набор объектов Resurce"""
#         for teacher_id in range(1, 7):
#             teacher: pd.Series = pd.Series({'name': f'Преподаватель {teacher_id}',
#                                             'e_mail': f' teacher_{teacher_id}@university.com'})
#             self.teachers = pd.concat([self.teachers, teacher.to_frame().T], ignore_index=True)
#         print(self.teachers)
#         for group_id in range(1, 7):
#             group = pd.Series({'name': f'Группа {group_id}'})
#             self.groups = pd.concat([self.groups, group.to_frame().T], ignore_index=True)
#         print(self.groups)
#         for group_id in range(len(self.groups)):  # В каждой группе
#             for student_id_in_group in range(1, 11):  # создаем 10 студентов
#                 student_id = int(str(group_id) + str(student_id_in_group - 1)) + 1  # Создаем id студента
#                 student = pd.Series({'group': self.groups['name'][group_id],  # Создаем строку данных студента
#                                      'name': f'Студент {student_id}',
#                                      'e_mail': f' student_{student_id}@university.com'})
#                 self.students = pd.concat([self.students, student.to_frame().T], ignore_index=True)  # Сохраняем
#         print(self.students)  # Выводим на экран
#         for building_id in range(1, 4):
#             building = pd.Series({'name': f'Корпус {building_id}'})
#             self.buildings = pd.concat([self.buildings, building.to_frame().T], ignore_index=True)
#         print(self.buildings)
#         for building_id in range(len(self.buildings)):
#             for auditorium_id in range(1, 7):
#                 # auditorium = int(str(building) + str(auditoriums_in_building - 1)) + 1
#                 auditorium = pd.Series({'building': self.buildings['name'][building_id],
#                                         'name': f'Аудитория {auditorium_id}'})
#                 self.auditoriums = pd.concat([self.auditoriums, auditorium.to_frame().T], ignore_index=True)
#         print(self.auditoriums)


if __name__ == '__main__':
    expert = Expert()  # Создаем эксперта по расписанию и одно расписание
    expert.load_pair()
    expert.load_schedules(1)  # Эксперт загружает один вариант расписания
    for schedule in expert.schedules:  # Для каждого расписания выводим
        schedule.create_objects()  # Создаем связанные с родителем дочерние объекты
        # print(schedule)  # его номер и число занятий
        # for lesson in schedule.lessons:  # Для каждого занятия выводим
        #     print(lesson)  # Объекты занятия (см. переопределение печати)
    # for schedule in expert.schedules:  # Для каждого расписания выводим
    #     print(f'    Предупреждения по расписанию №{schedule.id}')
    #     schedule.alerts_handling()  # Проверяем расписание на предупреждения
    for schedule in expert.schedules:
        # schedule.create_df()
        schedule.load_df()
