from django.shortcuts import render, redirect
from django.http import JsonResponse 
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import ConsultaForm, AnimalForm, ClienteForm
from .models import Animal, Consulta, Cliente



def agendar_consulta(request):

    cliente = None
    animais = None 
    # For add_animal_modal
    form_pet = AnimalForm()
    # For add_cliente_modal
    form_cliente = ClienteForm()
    form = ConsultaForm()

    if request.method == 'POST':
    
        if "buscar" in request.POST:
            cpf = request.POST.get("cpf")
                        
            try:
                cliente = Cliente.objects.get(cpf=cpf)
                animais = cliente.animais.all()
               
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
                   'form_pet' : form_pet,
                   'form_cliente' : form_cliente },  )



def lista_animais(request):
    animais = Animal.objects.all()
    return render(request, 
                  'lista_animais.html', 
                  {'animais' : animais}
                  )

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
                'id':cliente.id, 
                'nome' : cliente.nome,
                'cpf': cliente.cpf})
        else:
            return JsonResponse({'errors' : form.errors}, status=400)

    else:
        form = ClienteForm()

    return render(request, 'add_cliente_modal.html', {'formCliente' : form})