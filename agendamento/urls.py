from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:cliente_id>/", views.detail, name="detail"),
    path("<int:cliente_id>/results", views.results, name="results"),
    path("<int:cliente_id>/vote", views.vote, name="vote"),
]
