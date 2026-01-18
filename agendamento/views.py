from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.template import loader
from django.shortcuts import render, get_object_or_404

from datetime import datetime


from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Cliente, Agendamento
from .serializers import AgendamentoSerializer


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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AgendamentoListaApi(APIView):
    """
    Controle total: Listagem e Criação.
    """

    def get(self, request):
        agendamentos = Agendamento.objects.filter(data=datetime.now())
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
