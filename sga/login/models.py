from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RegistroLogin(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    horario_login = models.DateTimeField(auto_now_add=True)
    horario_logout = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.usuario} - {self.horario_login}'
    