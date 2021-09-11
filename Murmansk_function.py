import pandas as pd

#TODO добавить path

spisok = []

n = int(input()) #день

path = {'report': '/home/dmitry/Загрузки/pivot_table.xlsx',
        'uchastok29': '/home/dmitry/Загрузки/uchastok29.xlsx',
        'bigdata': '/home/dmitry/Рабочий стол/code/pandas/BD.csv',
        'uchastok40': '/home/dmitry/Загрузки/uchastok40.xlsx',
        'standart29': '/home/dmitry/Рабочий стол/code/pandas/standart29.xlsx'}

data_bd = pd.read_csv(path['bigdata'])


##функция обработки сводного отчета
def pivot_processing():
    df = pd.read_excel(path['report'])
    df = df.drop([0, 1, 2, 3, 4, 5, 6])
    df.columns = ['name', 'date', 'val']

    df1 = df[0:len(df):3]
    df0 = df[df.date == 'Итого:']
    df1.index = df0.index

    result_report = pd.concat([df1[['name', 'date']], df0.val], axis='columns')
    result_report = result_report[(result_report.val != 0) & (result_report.val != '-')]
    return result_report


##Объединяем таблицы кладовщика 29уч и 40уч
def gsm_table():
    uchastok29 = pd.read_excel(path['uchastok29'])
    uchastok40 = pd.read_excel(path['uchastok40'])
    df = pd.concat([uchastok29,  uchastok40])
    return df


##Метод извдечения и переименоывания нужных нам столбцов из таблицы кладовщика##
def klad():
    z = n
    c = 'Unnamed: 4'
    if z == 1:
        c = 'Unnamed: 4'
    else:
        c = list(c)
        c[-1] = str(int(c[-1]) + (z - 1))
        c = ''.join(c)
    x = gsm_table()  # pd.read_excel(y) # откываем таблицу кладовщика
    x = x[['Unnamed: 0', c]]
    x.columns = ['id', 'V']
    return x


##Обработка сводной таблицы кладовщика##
def klad_table():
    uchastok29 = klad()
    uchastok29 = uchastok29.dropna()  # удаляем все значения nan
    uchastok29.id = uchastok29.id.astype(int)  # преобразуем str(id) = int(id)
    uchastok29.set_index('id', inplace=True)  # индексируем столбец id
    return uchastok29


##Заключительная обаботка через слияние таблиц
def pivot_id():
    result_report = pivot_processing()
    uchastok29 = klad_table()
    df1 = pd.merge(uchastok29, data_bd, left_index=True, right_index=True)
    result = pd.merge(df1, result_report, left_on='Omnicomm', right_on='name')
    result = result[['name', 'date', 'val', 'V']]
    spisok.append(result)
    result = pd.concat([i for i in spisok])
    result.insert(2, 'date2', 'date')
    result.insert(3, 'event', 'Заправка')
    result['date2'] = result['date']

    result['-'] = result['V'] - result['val']  # формула расхождения литража
    return result


##вывести отчет в excel формат
def print_report():
    result = pivot_id()
    return result.to_excel('result.xlsx')


## функция выводит технику которая не попала ни в оодну из таблиц
##кладовщик не внесла заправку, заправка не попала в omnicomm
def table_error():
    result_report = pivot_processing()
    uchastok29 = klad_table()
    df1 = pd.merge(uchastok29, data_bd, left_index=True, right_index=True)
    table1 = [i for i in result_report['name']]
    table2 = [i for i in df1['Omnicomm']]
    return [i for i in table1 if i not in table2], [i for i in table2 if i not in table1]


# функция сохранения эталона для проверки таблиц кладовщика
def save_klad():
    data29 = pd.read_excel(path['uchastok29'])
    data29 = data29[['Unnamed: 0', 'Unnamed: 1']].dropna()
    data29.columns = ['id', 'name']
    data40 = pd.read_excel(path['uchastok40'])
    data40 = data40[['Unnamed: 0', 'Unnamed: 1']].dropna()
    data40.columns = ['id', 'name']
    return data29.to_excel('standart29.xlsx'), data40.to_excel('standart40.xlsx')  # эталон

##функция проверки таблицы кладовщика на изменения
def check():
    uchastok29 = pd.read_excel(path['uchastok29'])
    uchastok29 = uchastok29[['Unnamed: 0', 'Unnamed: 1']]
    uchastok29.columns = ['id', 'name']
    uchastok29 = uchastok29.dropna()  # удаляем все значения nan
    uchastok29.id = uchastok29.id.astype(int)  # преобразуем str(id) = int(id)
    uchastok29.set_index('id', inplace=True)  # индексируем столбец id

    standart29 = pd.read_excel(path['standart29'])
    standart29 = standart29[['id', 'name']]
    standart29 = standart29.dropna()  # удаляем все значения nan
    standart29.id = standart29.id.astype(int)  # преобразуем str(id) = int(id)
    standart29.set_index('id', inplace=True)  # индексируем столбец id
    return uchastok29 == standart29



a = print_report() #сформировать итоговый отчет
b = table_error() # показать расхождения

print(b)
