import PySimpleGUI as sg
layout = [
    [sg.Text('Регистрация водителей'), sg.InputText(), sg.FileBrowse()],
    [sg.Text('Сводный отчет'), sg.InputText(), sg.FileBrowse()],
    [sg.Output(size=(88, 20))],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Auto_Report', layout)
while True:                             # The Event Loop
    event, values = window.read()
    print(values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break