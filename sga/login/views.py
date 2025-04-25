from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from principal.models import Funcionario
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def login_funcionario(request):
    if request.method == 'POST':
        cpf = request.POST['cpf']
        senha = request.POST['senha']
        try:
            funcionario = Funcionario.objects.get(cpf=cpf)
            user = authenticate(request, username=funcionario.user.username, password=senha)
            if user is not None:
                login(request, user)

                # Redirecionamento por função
                funcoes = list(funcionario.funcoes.values_list('nome', flat=True))

                if len(funcoes) == 1:
                    funcao = funcoes[0]
                    request.session['funcao_ativa'] = funcao
                    return redirecionar_por_funcao(funcao)
                elif len(funcoes) > 1:
                    request.session['funcoes_disponiveis'] = funcoes
                    return redirect('escolher_funcao')
                else:
                    messages.warning(request, 'Funcionário sem função atribuída.')
                    return redirect('login_funcionario')
            else:
                messages.error(request, 'Senha incorreta.')
        except Funcionario.DoesNotExist:
            messages.error(request, 'CPF não encontrado.')

    return render(request, 'login/login.html')

@login_required
def escolher_funcao(request):
    funcoes = request.session.get('funcoes_disponiveis', [])

    if request.method == 'POST':
        funcao_escolhida = request.POST.get('funcao')
        request.session['funcao_ativa'] = funcao_escolhida 
        return redirecionar_por_funcao(funcao_escolhida)

    return render(request, 'login/escolher_funcao.html', {'funcoes': funcoes})

def redirecionar_por_funcao(funcao):
    if funcao == 'administrador':
        return redirect('pagina_administrador')
    elif funcao == 'recepcionista':
        return redirect('pagina_recepcionista')
    elif funcao == 'guiche':
        return redirect('pagina_guiche')
    else:
        return redirect('login_funcionario')

def logout_funcionario(request):
    logout(request)
    return redirect('login_funcionario')