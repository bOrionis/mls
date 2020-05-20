import PySimpleGUI as sg      

""" layout = [[sg.Text('My one-shot window.')],      
                 #[sg.InputText()],
                 [sg.InputText(key='-IN-')],
                 [sg.Button('Read'), sg.Exit()]] #Loop
#                 [sg.Submit(), sg.Cancel()]]  #Single    

window = sg.Window('Window Title', layout)    

'''
########################################## Single
event, values = window.read()    
window.close()

#text_input = values[0]    
text_input = values['-IN-']    
sg.popup('You entered', text_input)
##########################################


'''
########################################## Loop
while True:                             # The Event Loop
    event, values = window.read() 
    print(event, values)       
    if event in (None, 'Exit'):      
        break
##########################################


window.close() """

"""
    Allows you to "browse" through the Theme settings.  Click on one and you'll see a
    Popup window using the color scheme you chose.  It's a simple little program that also demonstrates
    how snappy a GUI can feel if you enable an element's events rather than waiting on a button click.
    In this program, as soon as a listbox entry is clicked, the read returns.
"""
from ..getDataML import getCategories

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

                catDict = getCategories(catListID[idx], key = 'child')
                
                catList = [cat['name'] for cat in catDict]
                catListID = [cat['id'] for cat in catDict]
                
                #sg.Listbox(values=catListNueva, size=(20, 12), key='-LIST-', enable_events=True)
                window['-LIST-'].update(catList)
                window['-ID-'].update(CATEGORY_ID)
                window['-NAME-'].update(CATEGORY_NAME)
                print(CATEGORY_ID)
            except:
                print('No hay mas subcategorias')
                
            '''layout = [[sg.Text('Theme Browser')],
                [sg.Text('Click a Theme color to see demo window')],
                [sg.Listbox(values=catListNueva, size=(20, 12), key='-LIST-', enable_events=True)],
                [sg.Button('Exit')]]'''
            #sg.theme(values['-LIST-'][0])
            #sg.popup_get_text('This is {}'.format(values['-LIST-'][0]))

    window.close()