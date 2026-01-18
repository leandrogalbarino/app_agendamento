from rest_framework import serializers
from .models import Agendamento, Cliente, Endereco
from datetime import datetime, timedelta
from django.db.models import Q


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ["cep", "bairro", "rua", "numero", "apartamento"]

    extra_kwargs = {"apartamento": {"required": False, "allow_null": True}}


class ClienteSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()

    class Meta:
        model = Cliente
        fields = [
            "cpf",
            "nome",
            "sobrenome",
            "email",
            "telefone",
            "endereco",
        ]

    extra_kwargs = {"data_cadastro": {"required": False, "allow_null": True}}


class AgendamentoSerializer(serializers.ModelSerializer):
    cliente_info = ClienteSerializer(source="cliente", read_only=True)
    procedimento = serializers.ReadOnlyField(source="procedimento.nome")

    class Meta:
        model = Agendamento
        fields = [
            "id",
            "data",
            "horario_inicio",
            "horario_fim",
            "cliente",
            "cliente_info",
            "procedimento",
            "valor_pago",
            "bloqueado",
            "descricao",
        ]

    extra_kwargs = {
        "valor_pago": {"required": False, "allow_null": True},
        "descricao": {"required": False, "allow_blank": True},
    }

    def _intervalo_valido(self, dt_inicio: datetime, dt_fim: datetime):
        if dt_fim <= dt_inicio:
            raise serializers.ValidationError(
                {
                    "horario_fim": "O horário de término deve ser após o horário de início."
                }
            )

    def _checar_conflitos_datas(self, dt_inicio: datetime, dt_fim: datetime):

        tempo_intervalo = timedelta(minutes=15)
        limite_inferior = (dt_inicio - tempo_intervalo).time()
        limite_superior = (dt_fim + tempo_intervalo).time()

        queryset = Agendamento.objects.filter(data=dt_inicio.date())
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        conflito = queryset.filter(
            horario_fim__gt=limite_inferior, horario_inicio__lt=limite_superior
        ).exists()

        if conflito:
            raise serializers.ValidationError(
                "Já existe um agendamento para este horário, por favor verificar a agenda."
            )

    def validate(self, attrs):

        data = attrs.get("data")
        data_inicio = attrs.get("horario_inicio")
        data_fim = attrs.get("horario_fim")

        if data and data_inicio and data_fim:
            dt_inicio = datetime.combine(data, data_inicio)
            dt_fim = datetime.combine(data, data_fim)

            self._intervalo_valido(dt_inicio, dt_fim)
            self._checar_conflitos_datas(dt_inicio, dt_fim)

        return attrs
