# ml_scanner

Scrapper de publicaciones de mercadolibre

## Installation

```python
pip install ml_scanner
```

## Usage

```python
python -m ml_scanner
```

Option -s for an automatic run. mls search a default file name 'config.mls'.

## Package required

- requests
- PySympleGUI
- matplotlib

## Archivo de configuracion de busqueda

En la carpeta donde se ejecuta, incluir un archivo de configuracion de la busqueda y descarga.

- Label: Etiqueta para la busqueda
- CATEGORY_ID: Codigo de la categoria donde se realiza la busqueda. (Ver Category Browser GUI)
- find: Texo a buscar
- f: Diccionario con los filtros de la busqueda

Minimo a incluir:

- label
- CATEGORY_ID o find.

Ejemplo 'config.mls'

```json
{
    "items":[
        {
            "label": "FKD",
            "CATEGORY_ID" : "MLA90998",
            "query": "ford fiesta kinetic 2011",
            "atrr" : ["price", "id", "km"]
            },
        {
            "label": "nescafe_piccolo_xs",
            "query": "nescafe dolce gusto piccolo xs",
			"f": {"ITEM_CONDITION": "2230284", "power_seller": "yes", "shipping_quarantine": "guaranteed_delivery", "category": "MLA438284", "price": "*-12500.0"},
            },
        {
            "label": "F_ESP",
            "CATEGORY_ID" : "MLA1743",
            "query": "ford ecosport xls 2004",
            "atrr" : ["price", "id", "km"]
            }
        ],
    "fecha": "23-05-2020"
}
```

## Filtros de busqueda

Para aplicar filtros a la busqueda, se debe ir inspeccionando los filtros disponibles y aplicandolos secuencialmente. Para ver los filtros disponibles de la busqueda general, se utiliza el metodo .print_a_filters. Luego se puede aplicar el filtro deseado con el metodo .setFilterIdx(i_Filtro,j_Value) donde i_Filtro corresponde número de filtro listado y j_Value el numero del seteo para el filtro.

Algunos filtros de rangos, pueden tener values predeterminados pero se pueden setear otros:

```txt
> Filtro 3 : Precio | ID: price
         - Value 0 : Hasta $ 10.000 | ID: *-10000.0 | Items: 13
         - Value 1 : 10000.0 | ID: 10000.0-10000.0 | Items: 2
         - Value 2 : Más de $10.000 | ID: 10000.0-* | Items: 29
```
Para hacer esto, se utiliza el metodo .setFilter(id, value, Forzar= True). Donde id es el id del filtro ('price') y value es el id del value con la configuracion personalizada (ej publicaciones hasta $12500 -> value = '*-12500.0').

Finalmente, una vez que la busqueda devuelve los items deseados se pude aplicar esta configuracion de filtros al archivo config.mls para la busqueda sistematica. Para ello, copiar (reemplazando ' por ") el contenido del miembro .f en el archivo config.mls bajo la key "f"


```python
from ml_scanner.getDataML import getDataML

url = getDataML.mlURL()
url.query = 'nescafe dolce gusto piccolo xs'
URL = url.getURL()

# inspeccion de filtros y aplicacion secuencial
url.print_a_filters()
url.setFilterIdx(14,0)
url.print_a_filters()
url.setFilterIdx(8,0)
url.print_a_filters()
url.setFilterIdx(11,0)
url.print_a_filters()
url.setFilterIdx(0,1)
url.print_a_filters()
url.setFilter('price','*-12500.0',Forzar= True)

url.f
```

## plots

Crea algunos graficos a partir de una clase tree().

Uso:

```python
import ml_scanner as mls

studyLabel = 'FKD'
dates = ['25-05-2020']

tree = mls.tree(studyLabel)

mls.plot_price_km(tree) # plotea el grafico de la utlima fecha disponible
mls.plot_price_km(tree, printLinks= True)

mls.plot_price_by_date(tree, USD = 120, printLinks = True)

plot_price_km_byItem(tree, printLinks = True, lastLinks = True, onlyChanges = True)
```

## loadData

Carga la estructura de archivos almacenados por saveData y permite acceder a la información de las publicaciones.

Uso:

```python
import ml_scanner as mls

cwd = os.path.join('C:','Users','name','Programacion')
scannFolder = 'mls_RUN'
studyLabel = 'FKD'

# creo una instancia de la clase tree:
##a) absolut path to studyLabel
pathToData = os.path.join(cwd, scannFolder, studyLabel)
label = mls.tree(pathToData) # absolut path to data

##b) scannFolder/studyLabel1, scannFolder/studyLabel2, etc
label = mls.tree(scannFolder, studyLabel) # path to one label relative to the scan folder with multiple studyLabels

##c) studyLabel1, studyLabel2, etc
label = mls.tree(studyLabel) # relative path to the label


label.load() #
dates = label.dates.keys() #devuelve las fechas con busquedas
label.dates[key] # es una clase results()

label.dates[key].count() # devuelve la cantidad de resultados en esa fecha
label.dates[key].pathToItem(idx) # retorna el path completo hasta el item de indice idx en fecha.items[idx]
label.dates[key].item(idx) # retorna el item de indice idx en fecha.items[idx]
label.dates[key].items # retorna la lista de  items de esa fecha
```

## GUI

### Category Browser

Permite navegar por las categorias disponibles en ML y obtener el CATEGORY_ID.

Uso:

```python
python -m ml_scanner.GUI
```
