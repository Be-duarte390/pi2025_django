from django import forms
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Funcionario, Funcao
from atendimento.models import Guiche

class CadastroFuncionarioForm(forms.ModelForm):
    nome = forms.CharField(label='Nome', max_length=100)
    cpf = forms.CharField(label='CPF', max_length=11)
    email = forms.EmailField(label='E-mail')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    funcoes = forms.ModelMultipleChoiceField(
        queryset=Funcao.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'funcoes']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Funcionario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('Já existe um funcionário cadastrado com esse CPF.')
        return cpf

    def generate_unique_username(self, base_username):
        username = slugify(base_username).replace('-', '')
        original = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original}{counter}"
            counter += 1
        return username

    def save(self, commit=True):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        senha = self.cleaned_data['senha']
        username = self.generate_unique_username(nome)

        user = User.objects.create_user(
            username=username,
            password=senha,
            email=email,
            first_name=nome
        )

        funcionario = super().save(commit=False)
        funcionario.user = user

        if commit:
            funcionario.save()
            funcionario.funcoes.set(self.cleaned_data['funcoes'])

        return funcionario

class GuicheForm(forms.ModelForm):
    class Meta:
        model = Guiche
        fields = ['numero']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número do guichê'}),
        }
        labels = {
            'numero': 'Número do Guichê'
        }