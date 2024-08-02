from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .forms import *
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from workalendar.america import Brazil
import locale

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Sua conta foi criada! Você já pode fazer login, {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def calendario(request):
    locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
    cal = Brazil()
    eventos = CalendarioEvento.objects.all()

    if 'calendarioResponsavel' in request.path:
        if request.user.is_authenticated:
            eventos = eventos.filter(responsavelEvento = request.user)
        else:
            return redirect('login')

    eventos_serializados = []
    hoje = datetime.today().date()

    for evento in eventos:
        color = '#337CA0'
        textColor = 'white'
        if evento.concluido:
            color = '#60993E'
        elif evento.data_limite < hoje:
            color = '#A10702'
        elif cal.get_working_days_delta(hoje, evento.data_limite) <= 3:
            color = '#F0A202'
            textColor = 'black'

        eventos_serializados.append({
            'title': evento.titulo,
            'start': evento.data_limite.isoformat(),
            'url': '/calendario/detalhes/' + str(evento.id),
            'responsavel': evento.responsavelEvento.username,
            'color': color,
            'obs': evento.observacao,
            'data': evento.data_limite.strftime("%d de %B de %Y"),
            'id': evento.id,
            'textColor': textColor
        })
    eventos_serializados.sort(key=lambda x: (x['start'] < hoje.isoformat(), abs((datetime.fromisoformat(x['start']).date() - hoje).days)))
    context = {'eventos_serializados': json.dumps(eventos_serializados), 'eventos':eventos_serializados}
    return render(request, 'calendario.html', context)

def calendario_detalhes(request, id):
    objetos = CalendarioEvento.objects.get(pk=id)
    form = EventoForm(instance = objetos)
    for field in form.fields.values():
        field.widget.attrs['disabled'] = True
    return render(request, 'calendarioDetalhe.html', {'evento': objetos, 'form':form})

@login_required
def CalenadarioNovo_evento(request):    
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            messages.success(request, 'Evento adicionado!')
            return redirect('/calendario')
    else:
        form = EventoForm()
    return render(request, 'calendarioNovo_evento.html', {'form': form})
    
@login_required
def CalendarioEdit(request, id):
    objetos = CalendarioEvento.objects.get(pk=id)
    
    form = EventoForm(instance = objetos)

    if request.method != 'POST':
        return render(request, 'calendarioNovo_evento.html', {'form':form})

    if 'observacao' in request.path:
        objetos.observacao = request.POST.get('obs')
        objetos.save()
        messages.success(request, 'Observação adicionada!')
        return redirect("/calendario/detalhes/"+str(id))

    form = EventoForm(request.POST, instance=objetos)
    if not form.is_valid():
        messages.success(request, 'Texto não pode ser editado!')
        return redirect("/calendario") 

    obj = form.save(commit=False)
    obj.save()
    messages.success(request, 'Evento editado!')
    return redirect("/calendario/detalhes/"+str(id))
    
@login_required  
def CalendarioConcluido(request, id):
    objetos = CalendarioEvento.objects.get(pk=id)

    if not (request.user.is_superuser or objetos.responsavelEvento == request.user):
        messages.warning(request, "Você não tem permissão para concluir esse evento!")
        return redirect("/calendario/detalhes/"+str(id))

    if objetos.concluido == False:
        objetos.concluido = True
        objetos.save()
        messages.success(request, 'Evento concluído!')
    else:
        messages.warning(request, 'Evento já foi concluído!')
    return redirect("/calendario/detalhes/"+str(id))

@login_required
def CalendarioDelete(request, id):
    objetos = CalendarioEvento.objects.get(pk=id)
    if not (request.user.is_superuser or objetos.responsavelEvento == request.user):
        messages.warning(request, 'Você não possui permissão para excuir o evento!')
        return redirect("/calendario/detalhes/"+str(id))

    objetos.delete()
    messages.success(request, 'Evento excluido!')
    return redirect("/calendario")
