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

## GUI

### Category Browser

Permite navegar por las categorias disponibles en ML y obtener el CATEGORY_ID.

Uso:

```python
python -m ml_scanner.GUI
```
