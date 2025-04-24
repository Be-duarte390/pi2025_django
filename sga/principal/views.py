from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Funcionario, Profissional, Paciente, TipoAtendimento, SenhaPaciente
from login.models import RegistroLogin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .forms import CadastroFuncionarioForm

# VIEWS REFERENTES AO ADMIN
def is_admin(user):
    return user.is_superuser or user.funcionario.funcoes.filter(nome='administrador').exists()

#Painel inicial - Admin
@login_required
@user_passes_test(lambda user: user.funcionario.funcoes.filter(nome='administrador').exists())
def pagina_administrador(request):
    return render(request, 'principal/pagina_administrador.html')

#Cadastro de Funcionários - Admin
@login_required
@user_passes_test(is_admin)
def cadastrar_funcionario(request):
    cadastro_realizado = False

    if request.method == 'POST':
        form = CadastroFuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário cadastrado com sucesso!')
            form = CadastroFuncionarioForm()  # Limpa o formulário
            cadastro_realizado = True
        else:
            messages.error(request, 'Erro ao cadastrar funcionário. Verifique os dados.')
    else:
        form = CadastroFuncionarioForm()

    return render(request, 'principal/cadastro_funcionario.html', {
        'form': form,
        'cadastro_realizado': cadastro_realizado
    })

#Exibição da lista de funcionários - Admin
@login_required
@user_passes_test(is_admin)
def lista_funcionarios(request):
    funcionarios = Funcionario.objects.select_related('user').prefetch_related('funcoes').all()
    return render(request, 'principal/lista_funcionarios.html', {
        'funcionarios': funcionarios
    })

#Relatório de logins - Admin
@login_required
@user_passes_test(is_admin)
def relatorio_logins(request):
    logins = RegistroLogin.objects.select_related('usuario').order_by('-horario_login')
    return render(request, 'principal/relatorio_logins.html', {
        'logins': logins
    })



def pagina_inicial(request):
    return render(request, 'principal/inicio.html')

# VIEWS REFERENTES AO RECEPCIONISTA
#Painel inicial - Recepcionista
@login_required
def pagina_recepcao(request):
    profissionais = Funcionario.objects.filter(funcoes__nome='profissional_saude').select_related('user')
    tipo_senhas = SenhaPaciente.TIPOS_SENHA

    if request.method == 'POST':
        return gerar_senha(request)

    return render(request, 'principal/pagina_inicial_recepcao.html', {
        'profissionais': profissionais,
        'tipo_senhas': tipo_senhas,
    })

@login_required
def confirmar_agendamento(request):
    if request.method == 'POST':
        nome_paciente = request.POST['nome_paciente']
        hora_agendada = request.POST['hora_agendada']
        profissional_id = request.POST['profissional']
        observacao = request.POST['observacao']
        tipo_senha = request.POST['tipo_senha']

        funcionario = get_object_or_404(Funcionario, id=profissional_id)
        profissional, _ = Profissional.objects.get_or_create(funcionario=funcionario)
        horario_agendado = datetime.strptime(hora_agendada, "%H:%M")

        SenhaPaciente.objects.create(
            tipo_senha=tipo_senha,
            nome_paciente=nome_paciente,
            profissional=profissional,
            horario_agendado=horario_agendado,
            observacao=observacao,
            criado_por=request.user,
            data_emissao=timezone.now()
        )

        messages.success(request, 'Agendamento confirmado com sucesso!')
        return redirect('pagina_recepcionista')

    tipo_senhas = SenhaPaciente.TIPOS_SENHA
    profissionais = Funcionario.objects.filter(funcoes__nome='profissional_saude').select_related('user')

    return render(request, 'principal/inicio.html', {
        'profissionais': profissionais,
        'tipo_senhas': tipo_senhas,
    })

@login_required
def gerar_senha(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        profissional_id = request.POST.get('profissional')
        tipo_senha = request.POST.get('tipo_senha')

        try:
            paciente = Paciente.objects.get(id=paciente_id)
        except Paciente.DoesNotExist:
            messages.error(request, 'Paciente não encontrado.')
            return redirect('pagina_recepcionista')

        try:
            profissional = Funcionario.objects.get(id=profissional_id, funcoes__nome='profissional_saude')
        except Funcionario.DoesNotExist:
            messages.error(request, 'Profissional não encontrado.')
            return redirect('pagina_recepcionista')

        senha = SenhaPaciente.objects.create(
            paciente=paciente,
            profissional=profissional,
            tipo_senha=tipo_senha,
            horario_agendado=timezone.now(),
            observacao="",
            criado_por=request.user,
            data_emissao=timezone.now()
        )

        senha.gerar_senha()
        senha.save()

        messages.success(request, 'Senha gerada com sucesso!')
        return redirect('pagina_recepcionista')

    profissionais = Funcionario.objects.filter(funcoes__nome='profissional_saude').select_related('user')
    return render(request, 'principal/inicio.html', {
        'profissionais': profissionais,
        'tipo_senhas': SenhaPaciente.TIPOS_SENHA
    })