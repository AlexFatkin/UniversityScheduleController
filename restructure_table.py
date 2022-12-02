# Транслитерация столбцов в строки

import pandas as pd


def excel_import(table_name, sheet_name):
    """Импортируем исходную таблицу"""
    return pd.read_excel(table_name, sheet_name)  # Импортируем исходную таблицу в датафрейм


def excel_export(df_restructured, table_name, sheet_name):
    """Экспортируем датафрейм в таблицу"""
    df_restructured.to_excel(table_name, sheet_name=sheet_name)  # Экспортируем датафрейм в таблицу


def restructure_date_2(df_data):
    """Транслитерация столбцов в строки"""
    col_number = len(df.columns)  # Считаем количество столбцов
    restructured_df = pd.DataFrame(columns=['student', 'problem'])  # Создаем новый датафрейм
    for row in df_data.index:  # Для каждой стоки в датафрейме
        for col in range(1, col_number):  # для каждого столбца в датафрейме
            new_row = pd.Series({'student': row, 'problem': df_data.iloc[row, col]})  # создаем строку
            if str(new_row['problem']) != 'nan':  # м если строка имеет значение
                restructured_df = pd.concat([restructured_df, new_row.to_frame().T], ignore_index=True)  # заносим её
    print(restructured_df)
    return restructured_df


if __name__ == '__main__':
    df = (excel_import('Schedule_Python_2.xlsx', 'Sheet1'))
    restruct_df = restructure_date_2(df)
    excel_export(restruct_df, "restructured_2.xlsx", 'Sheet1')
