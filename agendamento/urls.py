from django.urls import path
from . import views

app_name = "agendamento"

urlpatterns = [
    path("", views.pag_agenda, name="index"),
    path("api/raiz/", views.agendamento_lista),
    path("api/moderno/", views.AgendamentoListaApi.as_view()),
    path("disponiveis/", views.pag_disponibilidade, name="pagina_disponibilidade"),
    path("<int:agendamento_id>/", views.pag_unica, name="pagina_unica"),
]
