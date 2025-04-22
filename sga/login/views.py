from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from principal.models import Funcionario
from django.contrib.auth.models import User

# Create your views here.
def login_funcao(request, funcao):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        try:
            funcionario = Funcionario.objects.get(cpf=cpf)
            if funcionario.user:
                user_authenticated = authenticate(request, username=funcionario.user.username, password=senha)
                if user_authenticated is not None:
                    if funcionario.funcoes.filter(nome=funcao.lower()).exists():
                        login(request, user_authenticated)
                        messages.success(request, 'Login realizado com sucesso.')
                        return redirect(f'/{funcao.lower()}/')
                    else:
                        messages.error(request, 'Você não tem permissão para essa função.')
                else:
                    messages.error(request, 'Senha inválida.')
            else:
                messages.error(request, 'Funcionário não vinculado a um usuário válido.')
        except Funcionario.DoesNotExist:
            messages.error(request, 'Funcionário não encontrado.')
    return render(request, f'{funcao}/login.html')