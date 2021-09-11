# f = open('path.txt', 'w')
# f.write("'report': '/home/dmitry/Загрузки/pivot_table.xlsx', 'uchastok29': '/home/dmitry/Загрузки/uchastok29.xlsx'")
# f.close()

with open('path.txt') as file:
    lines = file.read().splitlines()

dic_data = {}
for line in lines:
    key, value = line.split(':')
    dic_data.update({key:value})

print(dic_data['general'])