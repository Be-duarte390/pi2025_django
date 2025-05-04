from django.db import models
from django.contrib.auth.models import User


class Guiche(models.Model):
    numero = models.PositiveSmallIntegerField(unique=True)
    tipos_atendimento = models.ManyToManyField('principal.TipoAtendimento', related_name='guiches', blank=True)
    # Outros campos...

    def __str__(self):
        return f'Guichê {self.numero}'

class Chamada(models.Model):
    senha = models.ForeignKey('principal.SenhaPaciente', on_delete=models.CASCADE, related_name='chamadas')
    guiche = models.ForeignKey(Guiche, on_delete=models.SET_NULL, null=True)
    paciente = models.ForeignKey('principal.Paciente', on_delete=models.SET_NULL, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.senha} - {self.guiche}"

class SenhaChamada(models.Model):
    senha = models.CharField(max_length=10)
    data_hora_chamada = models.DateTimeField(auto_now_add=True)
    atendente = models.ForeignKey('Atendente', on_delete=models.CASCADE)
    guiche = models.CharField(max_length=10)
    atendido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.senha} - {self.guiche}"
    
class Atendente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    guiche = models.CharField(max_length=10)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username
    
    