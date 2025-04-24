from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from principal.models import Funcionario
from django.contrib.auth.models import User


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
                funcoes = funcionario.funcoes.values_list('nome', flat=True)
                if 'administrador' in funcoes:
                    return redirect('pagina_administrador')
                elif 'recepcionista' in funcoes:
                    return redirect('pagina_recepcionista')
                elif 'guiche' in funcoes:
                    return redirect('pagina_guiche')
                else:
                    messages.warning(request, 'Função não reconhecida.')
                    return redirect('login_funcionario')
            else:
                messages.error(request, 'Senha incorreta.')
        except Funcionario.DoesNotExist:
            messages.error(request, 'CPF não encontrado.')

    return render(request, 'login/login.html')