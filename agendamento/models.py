from django.db import models


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


class Agendamento(models.Model):
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
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    bloqueado = models.BooleanField(default=False)
    descricao = models.CharField(max_length=100, blank=True)

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
        return (
            f"{self.data} | {self.horario_inicio}: {nome_cliente} - {nome_procedimento}"
        )


class Procedimento(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome
