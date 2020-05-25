import pickle
import os
import json
from ml_scanner.getDataML import getDataML
from datetime import datetime

class config():
    '''Configuracion del scanner.

    Miembros:
    file:           Archivo desde donde se carga la configuracion
    q:              String con la busqueda a realizar
    CATEGORY_ID:    Codigo de la categoria sobre la cual buscar
    atrr:           Atributos que seran almacenados
    items:          Items a escanear

    Valores predefinidos:
    file:           'config.mls'
    atrr:           ['price','id']

    Uso:

    ----------------------------------------
    from saveData import save

    m = save.config() #intancia de la clase
    m.getConfig() # obtengo la configuracion desde el archivo config.mls
    #m.setPaths # creo las carpetas segun la configuracion
    m.saveData() # descargo las publicaciones y las almaceno en un archivo
    ----------------------------------------

    '''


    def __init__(self):
        self.file = 'config.mls'
        self.q = ''
        self.CATEGORY_ID = ''
        self.atrr = ['price','id']
        self.items = []

    def getConfig(self, fileName = ''):
        '''Lee el archivo de configuracion del scanner.

        Variables:
        fileName:   String con el nombre del archivo a cargar

        Si no se indica ningun archivo, se usa el predeterminado 'config.mls'

        '''
        # si existe el archivo indicado, lo uso. Sino aviso que uso el predeterminado
        if fileName and os.path.isfile(fileName):
            self.file = fileName
        elif fileName:
            print('El archivo ' + fileName + ' no existe.')
            print('Se carga el predeterminado ' + self.file)
                
        with open(self.file) as json_file:
            cfg = json.load(json_file)
        self.items = cfg["items"]
        #return cfg

    def setPaths(self):
        '''Crea las carpetas para los items del archivo de configuracion cargado.

        '''

        labels = [item["label"] for item in self.items]
        for label in labels:
            if not(os.path.isdir(label)):
                os.makedirs(os.getcwd() + '\\' + label)

    def saveData(self):
        '''Descarga los items segun el archivo de configuracion cargado.

        '''

        self.setPaths()
        date = datetime.today().strftime('%d-%m-%Y')
        for item in self.items:
            path = os.path.join(os.getcwd(), item['label'], date)
            if not os.path.isdir(path):
                os.makedirs(path)
            url = getDataML.mlURL()

            url.CATEGORY_ID = item.get('CATEGORY_ID', '')
            url.find = item.get('find', '')
            url.SELLER_ID = item.get('SELLER_ID', '')
            url.NICKNAME = item.get('NICKNAME', '')

            results = getDataML.getData(url)
            print('>>Descargando busqueda',item['label'])

            for result in results:
                saveItem(result, os.path.join(path, result['id']), mode = 'o')
            #print('Se guardaron ', str(url.totalItems), ' del item: ', item['label'])

def saveItem(item, fileName, mode = 'r'):
    '''Guarda en un archivo binario de nombre file la variable item.

    Por default hace un chequeo de existencia del archivo y solicita la confirmacion de sobreescritura.
    Si se desea sobreescribir directamenete, incluir una tercera variable con el caracter 'o'

    Requiere importar el paquete pickle

    Ejemplos:

    -------------------------------------------
    import pickle

    a = ['a','b', 'c']
    saveItem(a, 'aList.f')

    La variable -a- se puede recuperar con:
    file = open("aList.f", "rb")
    a = pickle.load(file)

    -------------------------------------------
    import pickle
    from getDataML import getData
    from getDataML import mlURL

    url = mlURL()
    url.CATEGORY_ID = 'MLA1743'
    url.find = 'Ford fiesta kinetic 2011'

    items = getData(url)

    item = next(items) # 1er item de la busqueda
    saveItem(item, 'item_0.dict')

    item = next(items) # 2do item de la busqueda
    saveItem(item, 'item_1.dict')

    item = next(items) # 3er item de la busqueda
    saveItem(item, 'item_2.dict')
    ...

    -------------------------------------------

    #Los items se pueden cargar con:
    file = open("item_0.dict", "rb")
    item = pickle.load(file)
    -------------------------------------------

    '''
    # modo de confirmacion para reemplazar archivos
    if mode == 'r':            
        nFile = fileName
        while os.path.isfile(nFile):
            print('File ' + nFile + ' already exist. Enter a new name or press Enter to replace.')
            nFile = input('')
            # En caso de que se quiera reemplazar otro archivo, guardo el nuevo nombre:
            if nFile: fileName = fileName
        if nFile: fileName = nFile
            
    a_file = open(fileName, "wb")
    pickle.dump(item, a_file)
    a_file.close()