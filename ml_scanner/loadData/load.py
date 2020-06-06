import os
import pickle
import sys
from datetime import datetime


class tree():
    '''Clase que permite acceder a la estructura de archivos almacenados por saveData.

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
    label.items_by_date() # genera un diccionario con los items disponibles y su ubicacion en tree() y se almacena en el miembro .unique

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
        #self.unique = {}
        
    def load(self):
        # como verifico que pathToData es el inicio del walk? config.mls?
        dates = os.listdir(self.path)
        dates.sort(key=lambda date: datetime.strptime(date, "%d-%m-%Y"))

        for date in dates:
            self.dates[date] = results() # creo una instancia de la clase results()
            #result = self.dates[date]
            newPath = os.path.join(self.path,date)
            items = os.listdir(newPath)
            try:
                items.remove('available_filters')
            except:
                pass
            self.dates[date].items = items
            self.dates[date].path = newPath

    def items_by_date(self):
        '''Devuelve un diccionario con los nombres de los items almacenados y su ubicacion en tree() y se almacena en el miembro .unique

        '''
        self.unique = {}
        uniqueItems = []

        for date in self.dates:

            # para la primer fecha, almaceno todos los items como keys
            if not(uniqueItems):
                i = 0
                for item in self.dates[date].items:
                    self.unique[item] = {'date':[[date, i]], 'idx': [i]}
                    i += 1
                uniqueItems = list(set(self.dates[date].items + uniqueItems))
            else:
                # Si no es la primer fecha agrego los nuevos items y actualizo los existentes
                uniqueItems = list(set(self.dates[date].items + uniqueItems))
                for item in uniqueItems:
                    # si es nuevo, lo agrego
                    if item not in self.unique:
                        idx = self.dates[date].idx(item)
                        self.unique[item] = {'date':[[date, idx]]}
                    # si existe y esta en la fecha date, agrego los valores
                    elif item in self.dates[date].items:
                        idx = self.dates[date].idx(item)
                        self.unique[item]['date'].append([date, idx])
    
class results():
    '''Estructura de archivos con los resultados de busqueda realizado para cada fecha.
    
    ermite ademas acceder a los archivos e informacion con algunos metodos.

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

    kms = fecha.kms()
    years = fecha.years()

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
        '''Devuelve el numero de items.

        '''
        N = len(self.items)
        return N
    
    def idx(self, item):
        '''Devuelve el indice en items del nombre item.

        '''
        idx = self.items.index(item)
        return idx

    def pathToItem(self,idx):
        '''Devuelve el path al archivo del item asociado el indice idx de items.

        '''
        path = os.path.join(self.path,self.items[idx])
        return path

    def item(self,idx):
        '''Devuelve el nombre del item asociado al indice idx de items.

        '''
        item = self.items[idx]
        return item

    '''
    def itemGen(self):
        for itemName in self.items:
            yield itemName
    '''

    def prices(self, USD = 'get'):
        '''Retorna un array del valor del key:'price' y otro array del key:'currency_id'.

        prices = self.prices()

        '''
        if USD == 'get':
            # obtener de alguna web
            #https://www.cotizacion-dolar.com.ar/dolar-blue.php
            USD = 120.0
        prices = []
        for itemName in self.items:
            path = os.path.join(self.path,itemName)
            with open(path, "rb") as file:
                item = pickle.load(file)
                price = item['price'] if item['currency_id'] == 'ARS' else item['price']*USD
                prices.append(price)
                 
                
        return prices

    def price(self, item):
        #item = self.loadItem(idx)
        price = item['price']
        currency = item['currency_id']
        return price, currency

    def kms(self):
        '''Retorna un array del valor del item kms

        kms = self.kms()

        '''
        attr_id = 'KILOMETERS'
        N = self.count()
        kms = []
        for idx in range(N):
            item = self.loadItem(idx)
            attribute = self.find_attribute(item, attr_id)
            km = attribute['value_struct']['number']
            kms.append(km)
        return kms

    def km(self, item):
        '''Retorna un array del valor del item kms

        km = self.km(idx)

        '''
        attr_id = 'KILOMETERS'
        attribute = self.find_attribute(item, attr_id)
        if attribute:
            km = attribute['value_struct']['number']
            return km
        # es un attr mandatorio y deberia tener valor, pero igual dejo esto
        else:
            return -1000

    def years(self):
        '''Retorna un array del valor del item year

        years = self.years()

        '''
        keys = ['attributes', 10, 'value_name']
        years = self.load_n_keys(keys)
        return years

    def urls(self):
        '''Retorna un array del valor del item year

        urls = self.urls()

        '''
        keys = ['permalink']
        urls = self.load_n_keys(keys)
        return urls

    def url(self, item):
        '''Retorna un array del valor del item year

        url = self.urls(item)

        '''
        url = item['permalink']
        return url

    def load_n_keys(self, keys, *keys2):
        '''Retorna un array con el valor de los keys anidados.

        values = self.load_n_keys([key1, key2, ... ,keyn])
        # equivale a items[key1][key2]...[keyn]

        '''

        values = []
        keys.reverse()
        for itemName in self.items:
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
        '''Carga el archivo asociado al indice idx en items.

        '''
        with open(self.pathToItem(idx), "rb") as file:
            item = pickle.load(file)
            return item

    def find_attribute(self, item, attr_id):
        '''Devuelve el contenido del atributo 'attr_id' en el item del indice idx de items.

        '''

        #https://developers.mercadolibre.com.ar/en_us/categories-and-attributes
        
        # Atributos de cada categoria
        #https://api.mercadolibre.com/categories/CATEGORY_ID/attributes
        #item = self.loadItem(idx)
        attributes = item['attributes']
        for attribute in attributes:
            if attribute['id'] == attr_id:
                return attribute
        print(item['id'],'no contiene atributo', attr_id)
        return None