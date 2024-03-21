import locale

def formatacao_valor_numerico(num):
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')  
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    

    return locale.currency(num, grouping=True, symbol=None)