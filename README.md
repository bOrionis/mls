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

## Archivo de configuracion de busqueda

En la carpeta donde se ejecuta, incluir un archivo de configuracion de la busqueda y descarga.

- Label: Etiqueta para la busqueda
- CATEGORY_ID: Codigo de la categoria donde se realiza la busqueda. (Ver Category Browser GUI)
- find: Texo a buscar

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
            "find": "ford fiesta kinetic 2011",
            "atrr" : ["price", "id", "km"]
            },
        {
            "label": "F_ESP",
            "CATEGORY_ID" : "MLA1743",
            "find": "ford ecosport xls 2004",
            "atrr" : ["price", "id", "km"]
            }
        ],
    "fecha": "23-05-2020"
}
```

## loadData

Carga la estructura de archivos almacenados por saveData y permite acceder a la información de las publicaciones.

Uso:

```python
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
```

## GUI

### Category Browser

Permite navegar por las categorias disponibles en ML y obtener el CATEGORY_ID.

Uso:

```python
python -m ml_scanner.GUI
```
