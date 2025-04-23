from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from principal.models import TipoAtendimento
from atendimento.models import Guiche
from django.utils import timezone

@login_required
def pagina_guiche(request):
    if request.method == 'POST':
        guiche_numero = int(request.POST.get('numero_guiche'))
        tipos_atendimento = request.POST.getlist('tipos_atendimento')

        guiche = Guiche.objects.get(numero=guiche_numero)
        funcionario = request.user.funcionario
        funcionario.guiche = guiche
        funcionario.save()

        proporcoes = {}
        guiche.tipos_atendimento.clear()

        for tipo in tipos_atendimento:
            try:
                tipo_obj = get_object_or_404(TipoAtendimento, codigo=tipo)
                guiche.tipos_atendimento.add(tipo_obj)
                proporcao = request.POST.get(f'proporcao_{tipo}')
                if proporcao:
                    proporcoes[tipo] = int(proporcao)
            except TipoAtendimento.DoesNotExist:
                messages.error(request, f"Tipo de atendimento '{tipo}' não encontrado.")
                return redirect('pagina_guiche')

        guiche.proporcoes = proporcoes
        guiche.save()

        messages.success(request, 'Guichê configurado com sucesso!')
        return redirect('atendimento_guiche', guiche_numero=guiche_numero)

    guiches_disponiveis = Guiche.objects.all()
    from principal.models import SenhaPaciente
    tipos_senha = SenhaPaciente.TIPOS_SENHA
    funcionario = request.user.funcionario
    funcionario_nome = funcionario.nome

    return render(request, 'Guiche/inicio.html', {
        'guiches_disponiveis': guiches_disponiveis,
        'tipos_senha': tipos_senha,
        'funcionario_nome': funcionario_nome,
    })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from principal.models import SenhaPaciente
from atendimento.models import Guiche, SenhaChamada, Atendente

@login_required
def atendimento_guiche(request, guiche_numero):
    guiche = get_object_or_404(Guiche, numero=guiche_numero)
    tipos = guiche.tipos_atendimento.values_list('codigo', flat=True)
    senhas = SenhaPaciente.objects.filter(tipo_senha__in=tipos, chamada=False).order_by('data_emissao', 'horario_agendado')
    senha_chamada = None

    if request.method == 'POST':
        if 'chamar_senha_id' in request.POST:
            senha_id = request.POST['chamar_senha_id']
            senha_chamada = get_object_or_404(SenhaPaciente, id=senha_id)
            senha_chamada.chamada = True
            senha_chamada.save()

            atendente = Atendente.objects.get(usuario=request.user)
            SenhaChamada.objects.create(
                senha=senha_chamada.senha_completa,
                guiche=guiche.numero,
                atendente=atendente,
                atendido=False
            )

        elif 'reanunciar' in request.POST:
            senha_id = request.POST['reanunciar']
            senha_chamada = get_object_or_404(SenhaPaciente, id=senha_id)

    return render(request, 'Guiche/atendimento.html', {
        'guiche': guiche,
        'senhas': senhas,
        'senha_chamada': senha_chamada,
    })


def painel_tv1(request):
    senha_atual = SenhaPaciente.objects.filter(chamada=True).order_by('-data_emissao').first()
    ultimas_senhas = SenhaPaciente.objects.filter(chamada=True).order_by('-data_emissao')[:5]

    context = {
        'senha_atual': senha_atual,
        'ultimas_senhas': ultimas_senhas,
        'hora_atual': datetime.now(),
    }

    return render(request, 'atendimento/painel_tv1.html', context)


def ultima_senha_chamada(request):
    ultima = SenhaChamada.objects.filter(atendido=False).order_by('-data_hora_chamada').first()
    if ultima:
        return JsonResponse({
            'senha': ultima.senha,
            'guiche': ultima.guiche
        })
    return JsonResponse({'senha': '', 'guiche': ''})
