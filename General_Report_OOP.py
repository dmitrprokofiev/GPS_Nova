import pandas as pd

class Murmansk:

    path = {'report' : '/home/dmitry/Загрузки/',
       'bigdata' : '/home/dmitry/Рабочий стол/code/pandas/BD.csv'}

    def __init__(self, path_klad_1, path_klad_2, pivot_table, day):
        self.path_klad_1=path_klad_1
        self.path_klad_2=path_klad_2
        self.pivot_table=pivot_table
        self.day=day

    """Метод обратботки сводного отчета"""
    def pivot_processing(self):
        df = pd.read_excel(self.path['report']+self.pivot_table, )
        df = df.drop([0, 1, 2, 3, 4, 5, 6])
        df.columns = ['name', 'date', 'val']
        df1 = df[0:len(df):3]
        df0 = df[df.date == 'Итого:']
        df1.index = df0.index
        result_report = pd.concat([df1[['name', 'date']], df0.val], axis='columns')
        result_report = result_report[(result_report.val != 0) & (result_report.val != '-')]
        return result_report

    """""Объединяем таблицы кладовщика 29уч и 40уч"""
    def gsm_table(self):
        uchastok29 = pd.read_excel(self.path['report']+self.path_klad_2)
        uchastok40 = pd.read_excel(self.path['report']+self.path_klad_2)
        df = pd.concat([uchastok29, uchastok40])
        return df

    """Метод извдечения и переименоывания нужных нам столбцов из таблицы кладовщика"""
    def klad(self):
        z = self.day
        c = 'Unnamed: 4'
        if z == 1:
            c = 'Unnamed: 4'
        else:
            c = list(c)
            c[-1] = str(int(c[-1]) + (z - 1))
            c = ''.join(c)
        x = self.gsm_table() # открываем таблицу кладовщика
        x = x[['Unnamed: 0', c]]
        x.columns = ['id', 'V']
        return x

    """Обработка сводной таблицы кладовщика"""
    def klad_table(self):
        uchastok29 = self.klad()
        uchastok29 = uchastok29.dropna()  # удаляем все значения nan
        uchastok29.id = uchastok29.id.astype(int)  # преобразуем str(id) = int(id)
        uchastok29.set_index('id', inplace=True)  # индексируем столбец id
        return uchastok29

    def pivot_id(self):
        data_bd = pd.read_csv(self.path['bigdata'])
        df1 = pd.merge(self.klad_table(), data_bd, left_index=True, right_index=True)
        result = pd.merge(df1, self.pivot_processing(), left_on='Omnicomm', right_on='name')

        result = result[['name', 'date', 'val', 'V']]
        spisok = []

        spisok.append(result)

        result = pd.concat([i for i in spisok])

        # result.insert(2, 'date2', 'date')
        # result['date2'] = result['date']
        return result

x = Murmansk('uchastok29.xlsx', 'uchastok40.xlsx', 'pivot_table.xlsx', 1)
# print(x.pivot_processing())
# print(x.klad())
# print(len(
print(x.pivot_id())
