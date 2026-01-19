from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError


def data_ja_ocorreu(data):
    return data <= datetime.today().date()


def eh_mes_atual(data):
    data_atual = datetime.today().date()
    if data.year == data_atual.year and data.month == data_atual.month:
        return True
    return False


def converter_data(data_str):
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        return data
    except TypeError:
        raise ValidationError(
            {"erro": "Formato de data inválido. Use AAAA-MM-DD."},
        )
    except ValueError:
        raise ValidationError(
            {"erro": "Data inválida. Por favor insira um data válida."},
        )


def intervalo_mes(data, todo_mes=False):

    data_inicio = data.replace(day=1)
    data_fim = data

    if todo_mes:
        if eh_mes_atual(data):
            data_fim = datetime.today().date()

        else:
            if data.month == 12:
                primeiro_dia_proximo_mes = data.replace(
                    day=1, month=1, year=(data.year + 1)
                )
                data_fim = primeiro_dia_proximo_mes - timedelta(days=1)
            else:
                primeiro_dia_proximo_mes = data.replace(month=(data.month + 1), day=1)
                data_fim = primeiro_dia_proximo_mes - timedelta(days=1)

    return data_inicio, data_fim
