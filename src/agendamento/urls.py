from django.urls import path
from . import views

app_name = "agendamento"

urlpatterns = [
    path("", views.pag_agenda, name="index"),
    path("api/", views.api_docs),
    path("api/raiz/", views.agendamento_lista),
    path("api/moderno/", views.AgendamentosListOrAdd.as_view()),
    path(
        "api/moderno/<int:agendamento_id>/",
        views.AgendamentoInfo.as_view(),
        name="detail",
    ),
    path("api/faturamento_mensal/", views.faturamento_mensal),
    path("disponiveis/", views.pag_disponibilidade, name="pagina_disponibilidade"),
    path("<int:agendamento_id>/", views.pag_unica, name="pagina_unica"),
]
