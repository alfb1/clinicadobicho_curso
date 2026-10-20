import random
from django.shortcuts import render, redirect
from django.http import JsonResponse 
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required 
from .forms import ConsultaForm, AnimalForm, ClienteForm
from .models import Animal, Consulta, Cliente, Veterinario
from datetime import datetime, timedelta, date 


def str_to_date(arg):
    ano = int(arg[0:4])
    mes = int(arg[5:7])
    dia = int(arg[8:10])
    date_conv = date(ano, mes, dia)
    return date_conv




@login_required(login_url='login')
def consulta_eventos_veterinario(request):

    veterinario_id = request.GET.get("veterinario")
    start_date = request.GET.get("start")
    end_date = request.GET.get("end")
    eventos = []

    if not ( veterinario_id and start_date and end_date ):
        return JsonResponse([], safe=False)

    # Consultas agendadas

    start_date = start_date[0:10]
    end_date = end_date[0:10]

    consultas =  Consulta.objects.filter(veterinario__id=veterinario_id, data__date__range=(start_date,end_date)).select_related("animal", "veterinario").order_by("data")

    consultas_dict = {
         c.data.strftime("%Y-%m-%d-%H"): c.id for c in consultas
    }

    for c in consultas:
        eventos.append({
            "id" : c.id,
            "title" : f"{c.animal} | {c.veterinario.nome}",
            "start" : c.data.strftime("%Y-%m-%dT%H:%M:%S"),
            "color" : "#dc3545", # red
        })

#  for c in consultas:
#        eventos.append({
#            "id" : c.id,
#            "title" : f"{c.animal} | {c.veterinario.nome}",
#            "start" : c.data.strftime("%Y-%m-%dT%H:%M:%S"),
#            "color" : "#dc3545", # red
#        })

    hoje = str_to_date(start_date)
    horarios = [8,9,10,11,13,14,15,16]
    
    for i in range(7):
        data = hoje + timedelta(days=i)
        # excludes saturday and sunday
        if data.weekday()>=5:
            continue

        for hora in horarios:
            key = f"{data.strftime("%Y-%m-%d")}-{hora}"
            if key not in consultas_dict:
                slot_inicio = datetime.combine(data, datetime.min.time().replace(hour=hora))
                eventos.append(
                    {
                        "id" : f"disp-{data}-(hora)",
                        "title" : "Disponível",
                        "start" : slot_inicio.strftime("%Y-%m-%dT%H:%M:%S"),
                        "color" : "#28a745" #verde
                    }
                )            

    return JsonResponse(eventos, safe=False)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):

    if request.method == "POST":
        
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def consulta_eventos(request):
    eventos=[]

    for c in Consulta.objects.all():
        eventos.append({
            "id" : c.id,
            "title" : f"{c.animal.nome}",
            "start" : c.data.strftime("%Y-%m-%dT%H:%M:%S"),
            "color" : "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)])
        })
    print(eventos)
    return JsonResponse(eventos, safe=False)


@login_required(login_url='login')
def agendar_consulta(request):

    cliente = None
    animais = None 
    # animal foi cadastrado durange o agendamento
    id_animal_select = 0
    # For add_animal_modal
    form_pet = AnimalForm()
    # For add_cliente_modal
    form_cliente = ClienteForm()
    form = ConsultaForm()

    if request.method == 'POST':
    
        if "buscar" in request.POST:
            cpf = request.POST.get("cpf")
                        
            try:
                cliente  = Cliente.objects.get(cpf=cpf)
                id_animal_select = request.POST.get("animal")
                animais  = cliente.animais.filter(doneo=cliente)
               
            except Cliente.DoesNotExist:
                messages.error(request, "Cliente não encontrado.")

        elif "salvar" in request.POST:
            form = ConsultaForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Consulta agendada com sucesso!')
                return redirect('lista_consultas')
            else:
                form._errors.clear()
                messages.error(request, 'Problemas ao enviar os dados, tente novamente.') 

    return render(request, 
                  'agendar_consulta.html',
                  {'form': form, 
                   'cliente' : cliente,  
                   'animais':animais,
                   'id_animal_select':id_animal_select,
                   'form_pet' : form_pet,
                   'form_cliente' : form_cliente },  )



@login_required(login_url='login')
def lista_animais(request):
    animais = Animal.objects.all()
    return render(request, 
                  'lista_animais.html', 
                  {'animais' : animais}
                  )


@login_required(login_url='login')
def lista_consultas(request):
    consultas = Consulta.objects.all().order_by('data')
    return render(request, 'lista_consultas.html', {'consultas':consultas})

# Adiciona Animal 
def add_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)

        if form.is_valid():
            animal = form.save(commit=False)
            cpf = request.POST.get("cpf")
            dono = Cliente.objects.get(cpf=cpf)
            animal.doneo =dono
            animal.save()
            # To create list agendar_consulta "Selecionar"  from add_animal_modal.html after save presssed
            return JsonResponse({'id':animal.id, 'nome' : animal.nome, 'raca' : animal.raca})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = AnimalForm()

    return render(request, 'add_animal_modal.html', {'form':form})

# Adiciona Cliente
def add_cliente(request):

    if request.method == 'POST':

        form = ClienteForm(request.POST)

        if form.is_valid():
            cliente = form.save()
            return JsonResponse({
                'id'  : cliente.id,
                'cpf' : cliente.cpf })
        else:
            return JsonResponse({'errors' : form.errors}, status=400)

    else:
        form = ClienteForm()


    return render(request, 'add_cliente_modal.html', {'formCliente' : form})