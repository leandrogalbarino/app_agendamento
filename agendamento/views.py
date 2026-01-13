from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Cliente
from django.urls import reverse

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
    # return HttpResponseRedirect(reverse("agendamento:resultados", args=(cliente.id,)))
