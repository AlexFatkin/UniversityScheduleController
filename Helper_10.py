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
import pandas as pd
from abc import ABC, abstractmethod

global_student_id = 0  # Глобальная для всего модуля переменная - код студента
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)
pd.options.mode.chained_assignment = None  # Избегаем предупреждения


class UndesirableEffect(ABC):
    """Абстрактный класс Нежелательное явление"""
    def __init__(self, name: str, kind: str):
        self._name = name
        self._kind = kind  # Тип
        self._lessons = []  # Лист занятий
        self.schedule = None
        self.ue_count = 0  # Число НЯ в текущем расписании

    @abstractmethod
    def find(self):
        """Поиск НЯ"""
        pass


class SeminarBeforeLecture(UndesirableEffect):
    def __init__(self):
        super().__init__(name="Семинар до лекции", kind="Предупреждение")

    def find(self):
        print()
        print(f'{self._kind} : {self._name} ')
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
                self.ue_count += 1
        if self.ue_count == 0:
            print(f'Все в порядке. {self._kind} не выявлено')


class ManyLecturesInOneDay(UndesirableEffect):
    def __init__(self):
        super().__init__(name="Много лекций в один день", kind="Предупреждение")
        self.lecture_pair = 1  # Начальное число лекций (для счетчика)
        self.max_lecture_pair = 2  # Максимальное число пар лекций в один день
        self.week = 0  # Номер недели
        self.day = 0  # Номер дня недели (1 - Пн, 2 - Вт и т.д.)

    def find(self):
        print()
        print(f'{self._kind} : {self._name} ')
        self.many_lectures_in_one_day()

    def many_lectures_in_one_day(self):
        """"Много лекций (больше двух) в один день"""
        for les in self.schedule.lessons:  # Для всех занятий в одном расписании
            if les.kind == 'Лекция' and self.day == les.day and self.week == les.week:  # если занятие лекция и
                # у него совпадает предыдущие день и номер недели при сравнении, то
                self.lecture_pair += 1  # увеличиваем счетчик числа лекций на 1
            self.week = les.week  # Запоминаем номер недели для последующего сравнения
            self.day = les.day  # Запоминаем номер дня недели для последующего сравнения
            if self.lecture_pair > self.max_lecture_pair:  # Если число лекций в день больше установленного, то
                print(f"Лекций {self.lecture_pair} (больше, чем {self.max_lecture_pair}) "  # выводим предупреждение, 
                      f"в день {self.day} недели {self.week}")  # день и неделю
                self.lecture_pair = 1  # Восстанавливаем начальное число счетчика лекций
                self.ue_count += 1
        if self.ue_count == 0:
            print(f'Все в порядке. {self._kind} не выявлено')


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

    def load(self, file_path, table_name):
        self.load_df_from_excel(file_path, table_name)
        # self.load_df_from_excel(file_path='input/', table_name='Расписание №2 Form')
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
            for w in str(s['week']).split(sep=','):
                s['week'] = w
                self.unpack_df = pd.concat([self.unpack_df, s.to_frame().T])
        # self.unpack_df = self.unpack_df.reindex(columns=['#'] + list(self.unpack_df.columns))  # Переносим # вперед
        self.unpack_df['#'] = self.unpack_df.index  # Записываем в # индекс pack (свернутой формы)
        self.unpack_df = self.unpack_df.sort_values(by=['week', 'day', 'pair'],
                                                    ascending=[True, True, True], na_position='first')
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
        self.schedule_df = pd.DataFrame(columns=['group', 'week', 'day', 'pair', 'lesson', 'discipline',
                                                 'teacher', 'building', 'auditory'])
        self.id = id  # Номер расписания
        self.name = 'без ошибок'
        self.year = 0  # Год расписания
        self.term = 0  # Семестр расписания

    def __repr__(self):
        """Переопределение вывода на печать"""
        title = f'Файл {self.name}  Год {self.year} Семестр {self.term}'
        return title

    def load_df_from_excel(self, file_path, table_name):
        """Извлекаем данные из Excel таблицы и сохраняем в датафрейм"""
        self.file_path = f'{file_path}{table_name}.xlsx'
        self.schedule_df = load_from_excel(self.file_path, 'form')
        print(table_name)
        print(self.schedule_df)
        return self.schedule_df

    def create_ue_objects(self):
        """Создает набор объектов нежелательных явлений"""
        self.undesirable_effect_list.append(SeminarBeforeLecture())
        self.undesirable_effect_list.append(ManyLecturesInOneDay())

    def unpack(self):
        """Распаковка свертки"""
        self.unpack_df = pd.DataFrame()
        for i in range(0, len(self.schedule_df)):  # Для каждой записи в ДатаФрейме (ДФ)
            s = self.schedule_df.iloc[i]  # берем строку
            for j in s['week'].split(sep=','):  # из поля "неделя" строки выделяем номера недель
                s['week'] = j  # вставляем их по отдельности в поле "неделя"
                self.unpack_df = pd.concat([self.unpack_df, s.to_frame().T])  # и вставляем полученную строку в ДФ
        self.unpack_df = self.unpack_df.reindex(columns=['#'] + list(self.unpack_df.columns))  # Создаем новую колонку
        self.unpack_df['#'] = self.unpack_df.index  # Записываем туда же индекс с повторениями из свернутой формы
        self.unpack_df.index = list(range(1, len(self.unpack_df) + 1))  # Создаем новый индекс занятий без повторений
        print()
        print('Развернутая свертка')
        print(self.unpack_df)
        return self.unpack_df

    def find_ue(self):
        """Ищем НЯ """
        for ue in self.undesirable_effect_list:
            ue.schedule = self
            ue.find()


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


class Teacher:
    """Преподаватель"""

    def __init__(self, name=''):  # Код преподавателя
        self.name = name
        self.e_mail: str = f'teacher_{id}@mail.com'  # Генерация почты

    def __repr__(self):
        """Переопределение вывода на печать"""
        return f'{self.name}'


class Discipline:
    """Дисциплина"""

    def __init__(self, name=''):  # Код дисциплины
        self.name = name

    def __repr__(self):
        return f'{self.name}'


class Auditorium:
    """Аудитория"""

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return f'{self.name}'


class Group:
    """Группа"""

    def __init__(self, name=''):
        self.name = name
        self.students = []

    def __repr__(self):
        return f'{self.name}'


if __name__ == '__main__':
    expert = Expert()  # Создаем Эксперта
    expert.load(file_path='input/', table_name='Расписание №1 Form')  # Эксперт загружает свернутую форму расписания
    expert.schedule.create_ue_objects()  # и список объектов НЯ
    expert.handling()  # Эксперт запускает обработку распакованного расписания объектами НЯ
