"""
@author: lataf 
@file: TimeWork.py 
@time: 17.11.2022 11:38
Модуль отвечает за 
UML схема модуля
Сценарий работы модуля:
Тест модуля находится в папке model/tests.
"""

from datetime import datetime

# start time
start_time = "9:20"
end_time = "10:00"

# convert time string to datetime
t1 = datetime.strptime(start_time, "%H:%M")
print('Начальная дата:', t1.time())
print(f'Начальная дата без секунд: {t1.hour}:{t1.minute}')
print(type(t1))
# print(dir(t1))

t2 = datetime.strptime(end_time, "%H:%M")
print('Конечная дата:', t2.time())

# time difference
delta_t2_t1 = t2 - t1
print(type(delta_t2_t1))

# time difference in minute
print(f"Разница = Конечная дата {t2.time()} - Начальная дата {t1.time()}  = "
      f"{int(delta_t2_t1.total_seconds() // 60)} минут")
d