import os
import pickle
import sys


class tree():
    '''Carga la estructura de archivos almacenados por saveData.

    Uso:
    --------------------------------
    import ml_scanner

    cwd = os.path.join('C:','Users','name','Programacion')
    scannFolder = 'mls_RUN'
    studyLabel = 'FKD'
    
    # creo una instancia de la clase tree:
    ##a) absolut path to studyLabel
    pathToData = os.path.join(cwd, scannFolder, studyLabel)
    label = ml_scanner.tree(pathToData) # absolut path to data

    ##b) scannFolder/studyLabel1, scannFolder/studyLabel2, etc
    label = ml_scanner.tree(scannFolder, studyLabel) # path to one label relative to the scan folder with multiple studyLabels

    ##c) studyLabel1, studyLabel2, etc
    label = ml_scanner.tree(studyLabel) # relative path to the label


    label.load() #
    dates = label.dates.keys() #devuelve las fechas con busquedas
    label.dates[key] # es una clase results()

    label.dates[key].count() # devuelve la cantidad de resultados en esa fecha
    label.dates[key].pathToItem(idx) # retorna el path completo hasta el item de indice idx en fecha.items[idx]
    label.dates[key].item(idx) # retorna el item de indice idx en fecha.items[idx]
    label.dates[key].items # retorna la lista de  items de esa fecha

    # variacion de un precio segun la fecha 
    date = '25-05-2020'
    idx = 3
    prices = [label.dates[date].loadItem(idx)['price'] for date in label.dates]

    '''
    
    def __init__(self, pathToData = '', scannFolder = '', studyLabel = ''):
        self.path = os.path.join(pathToData,scannFolder,studyLabel)
        self.dates = {}
        
    def load(self):
        # como verifico que pathToData es el inicio del walk? config.mls?
        dates = os.listdir(self.path)

        for date in dates:
            self.dates[date] = results() # creo una instancia de la clase results()
            result = self.dates[date]
            newPath = os.path.join(self.path,date)
            result.items = os.listdir(newPath)
            result.path = newPath
    
class results():
    '''Almacena los resultados de busqueda realizado para cada fecha.

    Uso:

    # Carga de datos
    -----------------------------------------------------
    fecha = results()
    fecha.items = [] # lista de items a almacenar
    fecha.path = path/to/data/and/date
    -----------------------------------------------------

    # Metodos de results()
    -----------------------------------------------------
    fecha.count() # devuelve la cantidad de resultados encontrados
    fecha.pathToItem(idx) # retorna el path completo hasta el item de indice idx en fecha.items[idx]
    fecha.item(idx) # retorna el PRODUCT_ID del item de indice idx en fecha.items[idx]
    fecha.loadItem(idx) # # retorna el item de indice idx en fecha.items[idx]

    prices = fecha.prices() ## retorna un vector con los precios 
    
    keys = ['attributes', 10, 'value_name'] # year
    keys = ['attributes', 6, 'value_struct', 'number'] # km
    load_n_keys(keys)

    km = fecha.km()
    year = fecha.year()

    # devuelve cada item a partir de un generador
    items = fecha.itemGen()
    for item in items:
        print(item)

    '''
    
    def __init__(self):
        self.items = []
        self.path = ''
        #self.N = 0

    def count(self):
        N = len(self.items)
        return N

    def pathToItem(self,idx = 0):
        path = os.path.join(self.path,self.items[idx])
        return path

    def item(self,idx = 0):
        item = self.items[idx]
        return item

    def itemGen(self):
        for itemName in self.items:
            yield itemName

    def prices(self):
        '''Retorna un array del valor del key:'price' y otro array del key:'currency_id'.

        currency_id = 0: ARS, 1: USD

        prices, currency_id = self.prices()

        '''

        prices = []
        currency_id = [] # 0: ARS, 1: USD
        for itemName in self.itemGen():
            path = os.path.join(self.path,itemName)
            with open(path, "rb") as file:
                item = pickle.load(file)
                prices.append(item['price'])
                currency = 0 if item['currency_id'] == 'ARS' else 1
                currency_id.append(currency)
        return prices, currency_id

    def km(self):
        '''Retorna un array del valor del item km

        km = self.km()

        '''
        keys = ['attributes', 6, 'value_struct', 'number']
        km = self.load_n_keys(keys)
        return km

    def year(self):
        '''Retorna un array del valor del item km

        km = self.km()

        '''
        keys = ['attributes', 10, 'value_name']
        km = self.load_n_keys(keys)
        return km

    def load_n_keys(self, keys, *keys2):
        '''Retorna un array con el valor de los keys anidados.

        values = self.load_n_keys([key1, key2, ... ,keyn])
        # equivale a items[key1][key2]...[keyn]

        '''

        values = []
        keys.reverse()
        for itemName in self.itemGen():
            path = os.path.join(self.path,itemName)
            key = keys.copy()
            with open(path, "rb") as file:
                item = pickle.load(file)
                while len(key) > 1:
                    item = item[key[-1]]
                    key.pop()
                values.append(item[key[-1]])
        return values
            
    def loadItem(self, idx):
        with open(self.pathToItem(idx), "rb") as file:
            item = pickle.load(file)
            return item
        
