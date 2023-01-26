"""
@author: lataf
@file: Helper_7.py
@time: 24.01.2023 17:59
Модуль отвечает за предупреждения и ошибки при составлении расписания
9. Буду строить Фабричный метод для Undesirable Effect (UE)
UML схемы: Scheduler_classes_2.puml, Scheduler_usecase.puml
Сценарий работы модуля:Scheduler_scenario_2.docx
Тест модуля находится в папке tests.

"""
from dataclasses import dataclass
import pandas as pd
from abc import ABC, abstractmethod

global_student_id = 0  # Глобальная для всего модуля переменная - код студента
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)
pd.options.mode.chained_assignment = None  # Избегаем предупреждения


class UndesirableEffect(ABC):
    def __init__(self, name: str, kind: str):
        self._name = name
        self._kind = kind
        self._lessons = []
        self.schedule = None

    @abstractmethod
    def find(self): pass


class SeminarBeforeLecture(UndesirableEffect):
    def __init__(self):
        super().__init__(name="Семинар до лекции", kind="Предупреждение")

    def find(self):
        # print(self._name)
        self.seminar_befor_lecture()

    def seminar_befor_lecture(self):
        """"Семинар проводится до лекции"""
        last_seminar_number = 0
        for les in self.schedule.lessons:  # Для всех занятий в одном расписании
            if les.kind == Lesson.seminar:  # если занятие семинар,
                last_seminar_number = les.number  # то запоминаем его номер
            elif les.kind == Lesson.lecture and last_seminar_number >= les.number:  # и если номер лекции больше
                # или равен номеру семинара, то
                print(f"Лекция №{les.number} позже Семинара №{last_seminar_number}"  # выводим предупреждение,
                      f" в день {les.day} недели {les.week}")  # день и неделю


class ManyLecturesInOneDay(UndesirableEffect):
    def __init__(self):
        super().__init__(name="Много лекций в один день", kind="Предупреждение")

    def find(self):
        print(self._name)


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
        self.table_name = None
        self.file_path = None
        self.pack_df = None
        self.unpack_df = None
        self.schedule = None

    # def __repr__(self):
    #     return f'Расписание {self.schedules_number}'

    def load(self):
        self.load_df_from_excel(file_path='input/', table_name='Расписание №1 Form')
        self.unpack()
        self.create_schedule()

    def load_df_from_excel(self, file_path, table_name):
        """Извлекаем данные из Excel таблицы и сохраняем в датафрейм"""
        self.table_name = table_name
        self.file_path = f'{file_path}{self.table_name}.xlsx'
        self.pack_df = load_from_excel(self.file_path, 'form')
        print(self.table_name)
        print(self.pack_df)
        return self.pack_df

    def unpack(self):
        """Распаковка свертки"""
        self.unpack_df = pd.DataFrame()
        for i in range(0, len(self.pack_df)):
            s = self.pack_df.iloc[i]
            for w in s['week'].split(sep=','):
                s['week'] = w
                self.unpack_df = pd.concat([self.unpack_df, s.to_frame().T])
        # self.unpack_df = self.unpack_df.reindex(columns=['#'] + list(self.unpack_df.columns))  # Переносим # вперед
        self.unpack_df['#'] = self.unpack_df.index  # Записываем в # индекс pack (свернутой формы)
        self.unpack_df.index = list(range(1, len(self.unpack_df) + 1))  # Создаем новый индекс занятий без повторений
        print()
        print('Развернутая свертка')
        print(self.unpack_df)
        return self.unpack_df

    def create_schedule(self):
        self.schedule = Schedule(name=self.table_name, year=2022, term=1)
        for id in self.unpack_df.index:
            self.schedule.lessons.append(Lesson(id=id,
                                                week=self.unpack_df.at[id, 'week'],
                                                day=self.unpack_df.at[id, 'day'],
                                                pair=self.unpack_df.at[id, 'pair'],
                                                kind=self.unpack_df.at[id, 'kind'],
                                                number=self.unpack_df.at[id, 'number']))
        for les in self.schedule.lessons:
            les.discipline.name = self.unpack_df.at[les.id, 'discipline']
            les.teacher.name = self.unpack_df.at[les.id, 'teacher']
            les.auditorium.name = self.unpack_df.at[les.id, 'auditorium']
            for group in str(self.unpack_df.at[les.id, 'group']).split(sep=','):
                les.groups.append(Group(name=group))
            # print(les)
        # print(self.schedule)

    def load_pair(self):
        """Загружаем значения пар"""
        self.pair_df = load_from_excel(f'input/Пары.xlsx', 'Лист1')
        print(self.pair_df)

    # def load_schedules(self, schedules_number=1):
    #     """Сбор данных"""
    #     self.schedules_number = schedules_number  # Количество вариантов расписания
    #     for schedule_id in range(self.schedules_number):  # Для каждого последующего номера
    #         sch = Schedule(schedule_id + 1, lessons_number=self.lessons_number)  # создаем расписание
    #         # sch.load()  # и загружаем в него данные
    #         self.schedules.append(sch)  # Добавляем расписание в список расписаний

    def handling(self):
        """"Обработка"""
        self.schedule.find_ue()

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

    def __init__(self, name, year, term):
        self.undesirable_effect_list = []
        self.file_path = ''
        self.table_name = name
        self.year = year
        self.term = term
        self.df = None
        self.unpack_df = None
        self.lessons = []
        self.schedule = {}
        self.groups = []
        self.weeks = []
        self.days = []
        self.pairs = []
        self.lessons_types = []
        self.disciplines = []
        self.teachers = []
        self.buildings = []
        self.audiences = []
        self.schedule_df = pd.DataFrame(columns=['group', 'week', 'day', 'pair', 'lesson', 'discipline',
                                                 'teacher', 'building', 'auditory'])
        self.pair = None  # Объект Пары
        self.alert = None  # Предупреждение
        self.id = id  # Номер расписания
        self.name = 'без ошибок'
        self.lessons_number = 0  # Число занятий
        self.lessons_numbers = []  # Набор номеров занятий
        self.alerts = []  # Список предупреждений
        self.year = 0  # Год расписания
        self.term = 0  # Семестр расписания

    def __repr__(self):
        """Переопределение вывода на печать"""
        title = f'Файл {self.name}  Год {self.year} Семестр {self.term}'
        return title

    def load_df_from_excel(self, file_path, table_name):
        """Извлекаем данные из Excel таблицы и сохраняем в датафрейм"""
        # table_name = 'Расписание №1 Form'
        self.file_path = f'{file_path}{table_name}.xlsx'
        self.schedule_df = load_from_excel(self.file_path, 'form')
        print(table_name)
        print(self.schedule_df)
        return self.schedule_df

    def create_ue_objects(self):
        """Создает набор объектов нежелательных явлений"""
        self.undesirable_effect_list.append(SeminarBeforeLecture())
        self.undesirable_effect_list.append(ManyLecturesInOneDay())
        # self.alert = Alarm()  # Создаем дочерний объект Предупреждение
        # self.alert.schedule = self # Ссылаемся в нем на родителя - Расписание

    def unpack(self):
        """Распаковка свертки"""
        self.unpack_df = pd.DataFrame()
        for i in range(0, len(self.schedule_df)):
            s = self.schedule_df.iloc[i]
            for j in s['week'].split(sep=','):
                s['week'] = j
                self.unpack_df = pd.concat([self.unpack_df, s.to_frame().T])
        self.unpack_df = self.unpack_df.reindex(columns=['#'] + list(self.unpack_df.columns))  # Создаем новую колонку
        self.unpack_df['#'] = self.unpack_df.index  # Записываем туда индекс с повторениями из свернутой формы
        self.unpack_df.index = list(range(1, len(self.unpack_df) + 1))  # Создаем новый индекс занятий без повторений
        print()
        print('Развернутая свертка')
        print(self.unpack_df)
        return self.unpack_df

    # def load(self):
    #     """Загружает набор объектов - смотри Scheduler_classes.puml"""
    #     for n in range(self.lessons_number):  # Для каждого номера занятия
    #         n += 1
    #         self.lessons.append(Lesson(Lesson.lecture, n, Discipline(n), 1, n, Teacher(n), Group(n), Building(n),
    #                                    Auditorium(1), Pair(n)))  # добавляем лекцию, а затем
    #         self.lessons.append(Lesson(Lesson.seminar, n, Discipline(n), 1, n + 1, Teacher(n), Group(n), Building(n),
    #                                    Auditorium(2), Pair(n + 1)))  # добавляем семинар

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

    def df_to_schedule(self):
        at = self.unpack_df.at[4, 'group']
        print(at)

    def find_ue(self):
        for ue in self.undesirable_effect_list:
            ue.schedule = self
            ue.find()

    def alerts_handling(self):
        """"Обработка предупреждений"""
        self.alert.seminar_befor_lecture()  # Семинар проводится до лекции
        self.alert.many_lectures_in_one_day_1()  # Много лекций (больше двух) подряд - пока не создана


class Lesson:
    """Занятие - связывает свои объекты"""
    lecture = "Лекция"
    seminar = "Семинар"

    def __init__(self, id, week, day, pair, kind, number):  #
        self.id = id  # Код занятия
        self.week = week  # Неделя
        self.day = day  # День недели
        self.pair = pair  # Пара
        self.kind = kind  # Тип занятия: лекция или практическое занятие
        self.number = number  # Порядковый номер занятия в дисциплине
        self.discipline = Discipline()  # Дисциплина
        self.teacher = Teacher()  # Преподаватель
        self.auditorium = Auditorium()  # Аудитория
        self.group = Group()  # Группа
        self.groups = []  # Группы
        self.unpack_id = None  # Ссылка на id в не распакованном датафрейме
        self.face_to_face: bool = True  # Занятие очное

    def __repr__(self):
        """Переопределение вывода на печать"""
        self.group.name = ','.join([group.name for group in self.groups])  # Объединение названий групп через запятую
        return f'{self.id} {self.week} {self.day} {self.pair} {self.kind} {self.number} ' \
               f'{self.discipline.name},{self.teacher.name} {self.auditorium.name} {self.group.name}'


class Alarm:
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

    def __init__(self, name=''):  # Код преподавателя
        self.name = name
        self.e_mail: str = f'teacher_{id}@mail.com'  # Генерация почты

    def __repr__(self):
        """Переопределение вывода на печать"""
        return f'Преподаватель {self.name}'


class Discipline:
    """Дисциплина"""

    def __init__(self, name=''):  # Код дисциплины
        self.name = name

    def __repr__(self):
        return f'Дисциплина {self.name}'


class Auditorium:
    """Аудитория"""

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return f'Аудитория {self.name}'


class Pair:
    """Пара"""

    def __init__(self, id: int = 1):  # Код пары
        self.id = id
        self.pair_df = None

    def __repr__(self):
        return f'Пара {self.id}'

    def load_pair(self):
        """Загружаем значения пар"""
        self.pair_df = load_from_excel(f'input/Пары.xlsx', 'Лист1')
        print(self.pair_df)


class Student:
    """Студент"""

    def __init__(self, id):
        self.id: int = id
        self.e_mail_id: int = id

    def __repr__(self):
        return f'Студент {self.id}, student_{self.e_mail_id}@mail.com '


class Group:
    """Группа"""

    def __init__(self, name=''):
        self.name = name
        self.students = []

    def __repr__(self):
        return f'Группа {self.name}'

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


if __name__ == '__main__':
    expert = Expert()
    expert.load()
    expert.schedule.create_ue_objects()
    expert.handling()
    # schedule = Schedule()
    # schedule.load_df_from_excel(file_path='input/', table_name='Расписание №1 Form')
    # schedule.unpack()
    # schedule.df_to_schedule()
    # schedule.create_ue_objects()
    # schedule.find_ue()

    # expert = Expert()  # Создаем эксперта по расписанию и одно расписание
    # expert.load_schedules(1)  # Эксперт загружает один вариант расписания
    # for schedule in expert.schedules:  # Для каждого расписания выводим
    #     schedule.create_objects()  # Создаем связанные с родителем дочерние объекты
    # for schedule in expert.schedules:
    #     schedule_df = schedule.load_df()
    #     df = pd.DataFrame()
    #     for i in range(0, len(schedule_df)):
    #         s = schedule_df.iloc[i]
    #         for j in s['week'].split(sep=','):
    #             s['week'] = j
    #             df = pd.concat([df, s.to_frame().T])
    #     print()
    #     print('Развернутая свертка')
    #     print(df)

    # class A:
    #     pass
    #
    #
    # class B:
    #     pass
    #
    #
    # a = A()
    # b = B()
    # print(a == b)
    # b = a
    # print(a == b)
