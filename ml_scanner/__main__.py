# Funcionalidad gral. Es lo que se ejecuta cuando llamas al paquete. >> python -m mls
from ml_scanner import app

import time
import sys


if __name__ == '__main__':
    val = 'S'

    while val in ['S', 's']:
        try:
            val = app.run()
        except Exception as e:
            print(e)
            print('Intentar nuevamente?')
            val = input('(S/N) :')

        if val in ['N', 'n']:
            print('Finalizado. Continuar en mls?')
            val = input('(S/N) :')
    print('>> mls finalizado.')