from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Agendamento
from datetime import datetime
from django.urls import reverse
from rest_framework import status


class AgendamentoTests(APITestCase):
    def setUp(self):
        self.agendamento = Agendamento.objects.create(
            data=datetime.now().date(),
            horario_inicio="14:00",
            horario_fim="15:00",
            valor_pago=50.00,
        )
        self.urlName = "agendamento:detail"
        self.url = reverse(self.urlName, kwargs={"agendamento_id": self.agendamento.pk})

    def test_patch_mudar_valor_pago(self):
        data = {"valor_pago": 79.00}
        response = self.client.patch(path=self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.valor_pago, 79.00)

    def test_patch_com_nenhum_valor(self):
        data = {}
        response = self.client.patch(path=self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_id_invalida_(self):
        """
        Teste retornar NotFound se id for inexistente
        """
        id = 12331
        url = reverse(self.urlName, kwargs={"agendamento_id": id})
        response = self.client.patch(path=url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
