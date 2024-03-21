import re

def formatar_cpf(valor):
    valor_limpo = re.sub(r'\D', '', valor)
    return f'{valor_limpo[:3]}.{valor_limpo[3:6]}.{valor_limpo[6:9]}-{valor_limpo[9:]}'

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == '00000000000':
        return False
    
    # Cálculo dos dígitos de verificação
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    remainder = total % 11
    digit1 = 0 if remainder < 2 else 11 - remainder
    
    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    remainder = total % 11
    digit2 = 0 if remainder < 2 else 11 - remainder
    
    return cpf[-2:] == f"{digit1}{digit2}"