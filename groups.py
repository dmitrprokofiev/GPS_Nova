import pandas as pd

def file() -> object:
    # atz = input()

    with open('path.txt') as file:
        lines = file.read().splitlines()

    path = {}

    for line in lines:
        key, value = line.split(':')
        path.update({key:value})

    path["general"] = path["general"].replace("xxx", "1")
    return path


path = file()

def parent_process():
    parent_report = pd.read_excel(path['general'])
    parent_report_spisok = [i for i in parent_report[1]]
    data_auto = pd.read_excel(path["data_auto"])
    data_spisok_auto = [i for i in data_auto["Название ТС"]]
    data_um = pd.read_excel(path["data_um"])
    data_spisok_um = [i for i in data_um["Название ТС"]]
    general_column = []
    for i in parent_report_spisok:
        if i in data_spisok_auto:
            general_column.append("АБ")
        elif i in data_spisok_um:
            general_column.append("УМ")
        else:
            general_column.append(i)
    parent_report["Принаджежность"] = general_column

    return parent_report

print(parent_process())