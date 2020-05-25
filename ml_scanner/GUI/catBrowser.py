import PySimpleGUI as sg      
from ..getDataML import getCategories

'''
Permite navegar por las categorias disponibles en ML y obtener el ID.

Uso:

python -m mls.GUI

'''
def run():
        
    catList, catListID = [], []
    allCat = getCategories()
    
    catList = [cat['name'] for cat in allCat]
    catListID = [cat['id'] for cat in allCat]

    sg.theme('Dark Brown')


    layout = [[sg.Text('ML Category Browser')],
            [sg.Text('ID: '), sg.Text(size=(15,1),key='-ID-')],
            [sg.Text('Name: '), sg.Text(size=(20,1),key='-NAME-')],
            [sg.Listbox(values=catList, size=(40, 20), key='-LIST-', enable_events=True)],
            [sg.Button('Exit'),sg.Button('Restart')]]

    window = sg.Window('Category Browser', layout)

    while True:  # Event Loop
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event in (None, 'Restart'):
            catDict = getCategories()
            catList = [cat['name'] for cat in catDict]
            catListID = [cat['id'] for cat in catDict]
            window['-LIST-'].update(catList)
            event = False
        if event:    
            try:
                CATEGORY_NAME = values['-LIST-'][0]
                idx = catList.index(CATEGORY_NAME)
                CATEGORY_ID = catListID[idx]

                try:
                    catDict = getCategories(catListID[idx], key = 'child')
                except Exception as e:
                    print(e)
                
                catList = [cat['name'] for cat in catDict]
                catListID = [cat['id'] for cat in catDict]
                
                window['-LIST-'].update(catList)
                window['-ID-'].update(CATEGORY_ID)
                window['-NAME-'].update(CATEGORY_NAME)
                print(CATEGORY_ID)
            except:
                print('No hay mas subcategorias')

    window.close()