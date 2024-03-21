import re

def formatar_cnpj(valor):
    valor_limpo = re.sub(r'\D', '', valor)
    return f'{valor_limpo[:2]}.{valor_limpo[2:5]}.{valor_limpo[5:8]}/{valor_limpo[8:12]}-{valor_limpo[12:]}'

def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj == '00000000000000':
        return False
    
    # Cálculo dos dígitos de verificação
    total = 0
    factors = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12):
        total += int(cnpj[i]) * factors[i]
    remainder = total % 11
    digit1 = 0 if remainder < 2 else 11 - remainder
    
    total = 0
    factors = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(13):
        total += int(cnpj[i]) * factors[i]
    remainder = total % 11
    digit2 = 0 if remainder < 2 else 11 - remainder
    
    return cnpj[-2:] == f"{digit1}{digit2}"