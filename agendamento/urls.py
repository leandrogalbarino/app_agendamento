from django.urls import path
from . import views

app_name = "agendamento"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:cliente_id>/", views.cliente_pag, name="cliente_pagina"),
    path("<int:cliente_id>/results", views.results, name="resultados"),
    path("<int:cliente_id>/vote", views.vote, name="vote"),
]
