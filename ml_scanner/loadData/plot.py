import matplotlib.pyplot as plt
import webbrowser
import itertools
import os

marker = itertools.cycle(('o','x','+','*', '.', '^','>','<' ))

def plot_price_km(tree, dates = 'last' , USD = 'get', fileSave = False, printLinks = False):
    '''Grafica precio vs km de las fechas indicadas.

    Uso: 

    studyLabel = 'FKD'
    fileSave = studyLabel + '.svg'
    dates = ['25-05-2020', '31-05-2020', '03-06-2020']
    FKD = load.tree(studyLabel = studyLabel)

    plot_price_km(tree, dates = dates , fileSave = fileSave)

    '''

    marker = itertools.cycle(('o','x','+','*', '.', '^','>','<' ))

    studyLabel = os.path.split(tree.path)[-2]
    if not fileSave:
        fileSave = studyLabel + '.svg'

    if USD == 'get':
        # obtener de alguna web
        #https://www.cotizacion-dolar.com.ar/dolar-blue.php
        USD = 120.0
    
    tree.load()
    
    f = plt.figure()

    if dates == 'last':
        date, results  = tree.dates.popitem()
        y1 = results.prices()
        x1 = results.kms()
        
        s = plt.scatter(x1, y1,  label = date, marker = next(marker))

        if printLinks:
            urls = results.urls()
            s.set_urls(urls)

    else:    
        for date in dates:  
            y1 = tree.dates[date].prices(USD)
            x1 = tree.dates[date].kms()
            
            s = plt.scatter(x1, y1,  label = date, marker = next(marker))

            if printLinks:
                urls = tree.dates[date].urls()
                s.set_urls(urls)

    plt.legend()
    plt.title(tree.path)
    plt.xlabel('km')
    plt.ylabel('Precio [ARS]')

    if fileSave or printLinks:
        f.savefig(fileSave)
    if printLinks:
        webbrowser.open(fileSave)
    plt.show()

def plot_price_km_byItem(tree, fileSave = False, USD = 'get', printLinks = False, lastLinks = False, onlyChangesLinks = False):
    '''Grafica la evolucion temporal de cada publicacion en un grafico km vs precio

    '''
    
    marker = itertools.cycle(('o','x','+','*', '.', '^','>','<' ))

    studyLabel = os.path.split(tree.path)[-2]
    if not fileSave:
        fileSave = studyLabel + '.svg'

    if USD == 'get':
        # obtener de alguna web
        #https://www.cotizacion-dolar.com.ar/dolar-blue.php
        USD = 120.0

    tree.load()
    tree.items_by_date()

    if lastLinks:
        dates = [date for date in tree.dates]

    f = plt.figure()
    
    for itemName in tree.unique:
        x = []
        y = []
        #urls = []
        for date, idx in tree.unique[itemName]['date']:
                
            item = tree.dates[date].loadItem(idx)

            # chequear categoria auto para continuar

            price, currency = tree.dates[date].price(item)
            price = price if currency == 'ARS' else price*USD
            y.append(price)
            
            km = tree.dates[date].km(item)
            x.append(km)
        
        plotFlag = True
        if onlyChangesLinks:
            y_mean, y_max, y_min = sum(y)/len(y), max(y), min(y)
            noChange = y_mean == y_max and y_mean == y_min
            plotFlag = False if noChange else True

        if plotFlag:
            plt.plot(x, y,linewidth=1)
            plt.plot(
                x[0], y[0],
                label = itemName, marker = 's', color = 'k', 
                markersize=2,
                )
            plt.scatter(x, y,
                label = itemName, marker = next(marker),
                #s = 5,
                )

            if printLinks and lastLinks:
                if date == dates[-1]:
                    url = tree.dates[date].url(item)
                    plt.annotate("'", xy=(x[-1],y[-1]),
                                    url=url, color = 'r',
                                    #size=4,
                                    )
            elif printLinks:
                url = tree.dates[date].url(item)
                plt.annotate("'", xy=(x[-1],y[-1]),
                                url=url, color = 'r',
                                #size=4,
                                )
    
    plt.title(tree.path)
    plt.xlabel('km')
    plt.ylabel('Precio [ARS]')

    if fileSave or printLinks:
        f.savefig(fileSave)
    if printLinks:
        webbrowser.open(fileSave)
        
    plt.show()

def plot_price_by_date(tree, fileSave = False, USD = 'get', printLinks = False, onlyChangesLinks = False):
    '''Crea un grafico con la evolucion temporal del precio de las publicaciones.

    '''

    studyLabel = os.path.split(tree.path)[-2]
    if not fileSave:
        fileSave = studyLabel + '.svg'

    tree.items_by_date()

    dates = [date for date in tree.dates]
    N = len(dates)
    xTicks = [i for i in range(N)]

    if USD == 'get':
        # obtener de alguna web
        #https://www.cotizacion-dolar.com.ar/dolar-blue.php
        USD = 120.0

    f, ax = plt.subplots()
    for itemName in tree.unique:
        x = []
        y = []

        for date, idx in tree.unique[itemName]['date']:
            item = tree.dates[date].loadItem(idx)

            x.append(dates.index(date))

            price, currency = tree.dates[date].price(item)
            price = price if currency == 'ARS' else price*USD
            y.append(price)

        plotFlag = True
        if onlyChangesLinks:
            y_mean, y_max, y_min = sum(y)/len(y), max(y), min(y)
            noChange = y_mean == y_max and y_mean == y_min
            plotFlag = False if noChange else True

        if plotFlag:
            plt.plot(x, y)
            ax.scatter(x, y, marker = next(marker))
            if printLinks:
                url = tree.dates[date].url(item)
                plt.annotate("'", xy=(x[-1],y[-1]),
                                url=url, color = 'r',
                                #size=4,
                                )

    xLabels = dates
    ax.xaxis.set_ticks(xTicks)
    ax.xaxis.set_ticklabels(xLabels, rotation=20)
    
    plt.title(tree.path)
    plt.xlabel('Fechas')
    plt.ylabel('Precio [ARS]')
    
    if fileSave or printLinks:
        f.savefig(fileSave)
    if printLinks:
        webbrowser.open(fileSave)
    plt.show()