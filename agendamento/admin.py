from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Agendamento)
admin.site.register(models.Cliente)
admin.site.register(models.Procedimento)
admin.site.register(models.Endereco)
