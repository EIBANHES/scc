import datetime
import calendar
import pytz
from datetime import datetime


def validar_data_aniversario(data):
    try:
        fuso_horario_brasileiro = pytz.timezone('America/Sao_Paulo')

        data_hora_atual = datetime.datetime.now(fuso_horario_brasileiro)

        ano, mes, dia = map(int, data.split('-'))

        ano_atual = data_hora_atual.year
        if ano < 1900 or ano > ano_atual:
            return False

        if mes < 1 or mes > 12:
            return False

        ultimo_dia_mes = calendar.monthrange(ano, mes)[1]
        print(ultimo_dia_mes)
        if dia < 1 or dia > ultimo_dia_mes:
            return False

        data_atual = data_hora_atual.date()
        data_aniversario = datetime.date(ano, mes, dia)
        if data_aniversario > data_atual:
            return False

        return True

    except (ValueError, AttributeError):
        return False


def formatar_data_brasil(data):
    # Formatando como str (dd:MM:YYYY)
    data_formatada = data.strftime('%d/%m/%Y %H:%M:%S')

    return data_formatada


def formatar_data(data_str):
    try:
        # Parse da data e hora original em formato UTC
        data_hora_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Definir o fuso horário para o Brasil (BRT ou BRST)
        tz_brasil = pytz.timezone('America/Sao_Paulo')
        data_hora_utc = pytz.utc.localize(data_hora_obj)
        data_hora_brasil = data_hora_utc.astimezone(tz_brasil)

        # Formatar a data e hora para o padrão brasileiro
        data_hora_formatada = data_hora_brasil.strftime('%d/%m/%Y %H:%M:%S')
        return data_hora_formatada
    except ValueError:
        return "Formato de data e hora inválido"
    
def formatar_apenas_data(data_str):
    try:
        # Parse da data original em formato UTC (formato: '%Y-%m-%d')
        data_obj = datetime.strptime(data_str, '%Y-%m-%d')

        # Definir o fuso horário para o Brasil (BRT ou BRST)
        tz_brasil = pytz.timezone('America/Sao_Paulo')
        data_brasil = tz_brasil.localize(data_obj)

        # Formatar a data para o padrão brasileiro
        data_formatada = data_brasil.strftime('%d/%m/%Y')
        return data_formatada
    except ValueError:
        return "Formato de data inválido"
