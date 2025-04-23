from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

class SenhaPaciente(models.Model):
    TIPOS_SENHA = [
        ('E', 'Exames'),
        ('C', 'Curativos'),
        ('P', 'Psicologia'),
        ('G', 'Geral'),
        ('D', 'Dentista'),
        ('A', 'Primeiro Atendimento'),
        ('NH', 'Hansenologia'),
        ('H', 'Hansenologia Retorno'),
        ('U', 'Ultrassom'),
    ]
    tipo_senha = models.CharField(max_length=2, choices=TIPOS_SENHA)
    numero = models.IntegerField()
    senha_completa = models.CharField(max_length=5, unique=True)
    nome_paciente = models.CharField(max_length=255)
    profissional = models.ForeignKey('Profissional', on_delete=models.CASCADE)
    horario_agendado = models.DateTimeField()
    observacao = models.TextField(blank=True, null=True)
    horario_registro = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_emissao = models.DateTimeField(default=timezone.now)
    chamada = models.BooleanField(default=False)

    def gerar_senha(self):
        # Lógica para gerar a senha com base no tipo e sequência numérica
        ultima_senha = SenhaPaciente.objects.filter(tipo_senha=self.tipo_senha).order_by('-numero').first()
        proximo_numero = ultima_senha.numero + 1 if ultima_senha else 1
        self.numero = proximo_numero
        self.senha_completa = f"{self.tipo_senha}{proximo_numero:03d}"
    
    def save(self, *args, **kwargs):
        self.gerar_senha()
        super().save(*args, **kwargs)

class Paciente(models.Model):
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    # Outros campos do paciente...

    def __str__(self):
        return self.nome
    
class TipoAtendimento(models.Model):
    codigo = models.CharField(max_length=10)
    # Outros campos...

    def __str__(self):
        return f'{self.codigo}'