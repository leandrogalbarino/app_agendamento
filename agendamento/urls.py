from django.urls import path
from . import views

app_name = "agendamento"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.agenda, name="index"),
    path("<int:agendamento_id>/", views.reserva, name="pagina_unica")
]
