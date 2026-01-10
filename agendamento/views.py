from django.http import JsonResponse, HttpResponse, Http404
from django.template import loader
from django.shortcuts import render
from .models import Cliente


# Create your views here.
# json
# def index(request):
#     lista_clientes = Cliente.objects.order_by("-data_cadastro")
#     saida = ", ".join(
#         [f"{cliente.nome} {cliente.sobrenome}" for cliente in lista_clientes]
#     )
#     saida_itens = []
#     for cliente in lista_clientes:
#         objecto = {
#             "nome": cliente.nome,
#             "sobrenome": cliente.sobrenome,
#             "email": cliente.email,
#             "cep": cliente.endereco.cep if cliente.endereco else None,
#             "cidade": cliente.endereco.cidade if cliente.endereco else None,
#         }
#         saida_itens.append(objecto)
#     return JsonResponse(saida_itens, safe=False)


def index(request):
    lista_clientes = Cliente.objects.order_by("-data_cadastro")

    context = {"lista_clientes": lista_clientes}
    return render(request, "agendamento/index.html", context)


def detail(request, cliente_id):
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
    except Cliente.DoesNotExist:
        raise Http404(f"Cliente com id: {cliente_id} não existe.")
    return render(request, "agendamento/pagina_unica.html", {"cliente": cliente})


def results(request, cliente_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % cliente_id)


def vote(request, cliente_id):
    return HttpResponse("You're voting on question %s." % cliente_id)
