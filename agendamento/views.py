from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import render, get_object_or_404

from datetime import datetime


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Cliente, Agendamento
from .serializers import AgendamentoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

# Utilitarios do arquivo utils
from .utils import converter_data, intervalo_mes, data_ja_ocorreu


@csrf_exempt
def agendamento_lista(request):
    if request.method == "GET":
        data = datetime.now()
        agendamentos = Agendamento.objects.filter(data=data)
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        dados = JSONParser().parse(request)
        serializer = AgendamentoSerializer(dados)
        if serializer.is_valid():
            return JsonResponse(serializer.data, status=201)
    return HttpResponse(status=405)


class AgendamentosListOrAdd(APIView):
    """
    Ver todos agendamento para o Dia ou Criar um novo agendamento
    """

    def get(self, request):
        agendamentos = Agendamento.objects.filter(data=datetime.today().date())
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AgendamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class AgendamentoInfo(APIView):

    def get(self, request, agendamento_id):
        agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
        serializer = AgendamentoSerializer(agendamento)
        return Response(serializer.data)

    def patch(self, request, agendamento_id):
        agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
        serializer = AgendamentoSerializer(agendamento, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, agendamento_id):
        agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
        nome_cliente = agendamento.cliente.nome if agendamento.cliente else None
        agendamento.delete()

        if nome_cliente:
            mensagem = f"O agendamento com id: {agendamento_id} do cliente {nome_cliente} foi removido com sucesso."
        else:
            mensagem = (
                f"O agendamento com id: {agendamento_id} foi removido com sucesso."
            )

        return Response(
            {"mensagem": mensagem},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET"])
def api_docs(request):
    endpoints = {
        "raiz": "/agendamento/api/raiz",
        "moderno": "/agendamento/api/moderno",
        "faturamento": "/agendamento/api/faturamento_mensal",
        "dia": "/agendamento/api/agendamentos_dia",
    }
    return Response({"documentacao": endpoints}, status=status.HTTP_200_OK)


@api_view(["GET"])
def faturamento_mensal(request):

    filtros = request.query_params

    data_atual = datetime.today().date()
    mes_inicio, mes_fim = intervalo_mes(data_atual)

    if "data" in filtros:
        data_str = filtros.get("data")
        data = converter_data(data_str)
        if data_ja_ocorreu(data):
            mes_inicio, mes_fim = (
                intervalo_mes(data, todo_mes=True)
                if "mes_total" in filtros
                else intervalo_mes(data)
            )
        else:
            return Response(
                {
                    "erro": "Esta data ainda não ocorreu. por favor insira uma data válida para calculo do Faturamento."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    metricas = Agendamento.relatorios.obter_metricas_mensal(
        mes_inicio=mes_inicio, mes_fim=mes_fim
    )

    return Response(metricas, status=status.HTTP_200_OK)


def index(request):
    lista_clientes = Cliente.objects.order_by("-data_cadastro")
    list = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
    ]
    context = {"lista_clientes": lista_clientes, "lista": list}
    return render(request, "agendamento/index.html", context)


def cliente_pag(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    return render(request, "agendamento/pagina_unica.html", {"cliente": cliente})


def results(request, cliente_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % cliente_id)


def vote(request, cliente_id):
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
    except Cliente.DoesNotExist:
        return render(
            request,
            "agendamento/index.html",
            {
                "error_message": "You didn't select a choice.",
            },
        )
    message = f"O cliente {cliente.nome} votou na opção {request.POST["choice"]}"
    return HttpResponse(message)


def pag_agenda(request):
    agenda = Agendamento.objects.filter(data=datetime.now()).order_by("horario_inicio")
    return render(request, "agendamento/agenda.html", {"agenda": agenda})


def pag_disponibilidade(request):
    agenda = Agendamento.objects.filter(data=datetime.now()).order_by("horario_inicio")
    return render(request, "agendamento/agenda.html", {"agenda": agenda})


def pag_unica(request, agendamento_id):
    horario = get_object_or_404(Agendamento, pk=agendamento_id)
    return render(request, "agendamento/pagina_unica.html", {"reserva": horario})
