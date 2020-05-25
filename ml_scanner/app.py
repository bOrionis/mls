import ml_scanner
import sys

def run():
    print('Scanner de ML iniciado...')
    if not('-s' in sys.argv):
        print('Archivo de configuracion:')
        fileName = input('(Enter para default):')
    else:
        fileName = ''
    try:
        search = ml_scanner.config()
        search.getConfig(fileName)
        print('>Se encontraron', str(len(search.items)), 'items para escanear en:', search.file)
        
        if not('-s' in sys.argv):
            print('Buscar y guardar publicaciones?')
            val = input('(S/N) :')
        else:
            val = 's'

        if val in ['S', 's']:
            try:
                search.saveData()
                val = 'N'
            except Exception as e:
                print(e)
                print('Intentar nuevamente?')
                val = input('(S/N) :')
        return val
    except Exception as e:
        print(e)
        print('>> Error en el archivo de configuracion. Intentar nuevamente?')
        val = input('(S/N) :')
        return val
    
