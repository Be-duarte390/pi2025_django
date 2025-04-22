from django.db import models
from django.contrib.auth.models import User

FUNCOES_CHOICES = [
    ('administrador', 'Administrador'),
    ('recepcionista', 'Recepcionista'),
    ('guiche', 'Guichê'),
    ('profissional_saude', 'Profissional de Saúde'),
]

class Funcao(models.Model):
    nome = models.CharField(max_length=50, choices=FUNCOES_CHOICES, unique=True)

    def __str__(self):
        return dict(FUNCOES_CHOICES).get(self.nome, self.nome)

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    funcoes = models.ManyToManyField(Funcao)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Profissional(models.Model):
    funcionario = models.OneToOneField(Funcionario, on_delete=models.CASCADE)
    especialidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.funcionario.nome

