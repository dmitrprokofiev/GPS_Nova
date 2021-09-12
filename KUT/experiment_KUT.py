import pandas as pd
import time

#TODO дописать код под шаблон
#TODO выкинуть код на репозиторий
#TODO сделать возможным обработку сразу нескольких АТЗ в файле
#TODO сводный отчет за один день вместо двух

# path = { "general" : "/home/dmitry/PycharmProjects/Murmansk_Report_Pandas/KUT/general_table.xlsx",
#          "dut" : "/home/dmitry/PycharmProjects/Murmansk_Report_Pandas/KUT/dut_table.xlsx",
#          "result" : "/home/dmitry/PycharmProjects/Murmansk_Report_Pandas/KUT/result.xlsx"}

def file() -> object: #открыть txt-файл, записать содержимое в словарь и заменить ххх на нужный АТЗ
    atz = input()

    with open('path.txt') as file:
        lines = file.read().splitlines()

    path = {}

    for line in lines:
        key, value = line.split(':')
        path.update({key:value})

    path["general"] = path["general"].replace("xxx", atz)
    return path

path = file()

def parent_process():
    parent_report = pd.read_excel(path['general'])
    parent_report = parent_report.drop([0, 1, 2, 3, 4, 5, 6, 7])  # 'Unnamed: 1'
    parent_report = parent_report.loc[parent_report['Unnamed: 2'] != "-"] # удалить итоговые значения
    parent_report = parent_report.groupby(["Unnamed: 0", "Unnamed: 1"])["Unnamed: 5"].sum().reset_index() #индексируем полученный результат
    parent_report["Unnamed: 1"] = [i.rstrip(" ") for i in parent_report["Unnamed: 1"]]
    return parent_report


def last_process():
    last_report = pd.read_excel(path["dut"])
    last_report = last_report.drop([0, 1, 2, 3, 4, 5, 6])  # Unnamed: 0
    last_report.columns = ['name', 'date', 'val']

    df1 = last_report[0:len(last_report):3]
    df0 = last_report[last_report.date == 'Итого:']
    df1.index = df0.index

    result_report = pd.concat([df1[['name', 'date']], df0.val], axis='columns')
    result_report = result_report[(result_report.val != 0) & (result_report.val != '-')]
    return result_report

def pivot():
    result = parent_process().merge(last_process(), left_on="Unnamed: 1", right_on="name", how='left')
    result.drop(["name"], axis=1, inplace=True)
    result.columns = ["Топливозаправщик", "Т/С", "Объем по КУТ, л", "Дата", "Объем по ДУТ, л"]
    result = result[["Топливозаправщик", "Т/С", "Дата", "Объем по КУТ, л", "Объем по ДУТ, л"]] #меняем столбцы местами
    result = result.fillna(0)
    result["Разница, л."] = result["Объем по КУТ, л"] - result["Объем по ДУТ, л"]
    result["Разница, %"] = (result["Разница, л."] * 100) / result["Объем по КУТ, л"]
    result = result.fillna(0)
    result["Разница, %"] = result["Разница, %"].astype(int)
    #ставим дату в ячейки с нулевым значением
    date = set(result["Дата"])
    date.discard(0)
    insert_date = date.pop()
    result.loc[(result["Дата"] == 0, "Дата")] = insert_date
    return result




pivot().to_excel('result.xlsx')
# print(pivot().to_excel('result.xlsx'))
# print(pivot().to_excel("itog.xlsx"))