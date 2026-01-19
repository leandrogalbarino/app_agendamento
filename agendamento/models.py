from django.db import models
from datetime import datetime, date, time, timedelta
from django.core.exceptions import ValidationError
from django.db.models import Sum, Avg, Count, Value, DecimalField
from django.db.models.functions import Coalesce, Round


# Create your models here.
class Cliente(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    email = models.EmailField()
    telefone = models.CharField(max_length=14)
    endereco = models.ForeignKey(
        "Endereco", on_delete=models.SET_NULL, null=True, blank=True
    )
    data_cadastro = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"


class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    rua = models.CharField(max_length=30)
    numero = models.IntegerField()
    apartamento = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        eh_apartamento = self.apartamento if self.apartamento else ""
        if eh_apartamento:
            return f"Cep: {self.cep} | Num: {self.numero} | Apt: {self.apartamento} "
        return f"Cep: {self.cep} | Num: {self.numero} "


class AgendamentoManager(models.Manager):
    def obter_metricas_mensal(self, mes_inicio, mes_fim):
        metricas = self.filter(data__range=(mes_inicio, mes_fim)).aggregate(
            total_recebido=Round(
                Coalesce(Sum("valor_pago"), Value(0.00), output_field=DecimalField()), 2
            ),
            media_por_servico=Round(
                Coalesce(Avg("valor_pago"), Value(0.00), output_field=DecimalField()), 2
            ),
            total_atendimentos=Count("id"),
        )
        metricas["periodo"] = f"{mes_inicio} até {mes_fim}"
        return metricas


class Agendamento(models.Model):
    relatorios = AgendamentoManager()
    objects = models.Manager()

    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    cliente = models.ForeignKey(
        "Cliente", on_delete=models.SET_NULL, null=True, blank=True
    )
    procedimento = models.ForeignKey(
        "Procedimento", on_delete=models.SET_NULL, null=True, blank=True
    )
    valor_pago = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0.00
    )
    bloqueado = models.BooleanField(default=False)
    descricao = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["data"]

    def _verificar_conflitos_horarios(self):
        data = self.data
        margem = timedelta(minutes=15)

        novo_agendamento_inicio = datetime.combine(data, self.horario_inicio)
        novo_agendamento_fim = datetime.combine(data, self.horario_fim)
        conflitos = Agendamento.objects.filter(data=self.data).exclude(pk=self.pk)

        for item in conflitos:
            inicio_com_descanso = datetime.combine(data, item.horario_inicio) - margem
            fim_com_descanso = datetime.combine(data, item.horario_fim) + margem

            if (
                novo_agendamento_inicio < fim_com_descanso
                and novo_agendamento_fim > inicio_com_descanso
            ):
                raise ValidationError(
                    "Houve conflito de horários, por favor, verifique os horários disponiveis."
                )

    def _validar_intervalo_horario(self):
        self_inicio = datetime.combine(self.data, self.horario_inicio)
        self_fim = datetime.combine(self.data, self.horario_fim)
        if self_inicio >= self_fim:
            raise ValidationError(
                "O horário de fim precisa ser posteriormente ao de início."
            )

    def _inicializar_valor_pago(self):
        if self.valor_pago is None:
            if not self.bloqueado and self.procedimento:
                self.valor_pago = self.procedimento.valor
            else:
                self.valor_pago = 0.0

    def clean(self):
        super().clean()
        self._validar_intervalo_horario()
        self._verificar_conflitos_horarios()

    def save(self, *args, **kwargs):
        if not self.pk:
            self._inicializar_valor_pago()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.bloqueado:
            informacao_bloqueo = (
                self.descricao if self.descricao else "Sem Informações."
            )
            return f"{self.data} | {self.horario_inicio}-{self.horario_fim}: Sem agendamento - {informacao_bloqueo}"
        nome_cliente = self.cliente.nome if self.cliente else "Anônimo"
        nome_procedimento = (
            self.procedimento.nome if self.procedimento else "Não definido"
        )
        return f"{self.data} | {self.horario_inicio} - {self.horario_fim}: {nome_cliente} - {nome_procedimento}"


class Procedimento(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome
