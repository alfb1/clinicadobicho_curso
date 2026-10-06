from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import ConsultaForm, AnimalForm 
from .models import Animal, Consulta, Cliente



def agendar_consulta(request):

    cliente = None
    animais = None 

    if request.method == 'POST':
    
        if "buscar" in request.POST:
            cpf = request.POST.get("cpf")
                        
            try:
                cliente = Cliente.objects.get(cpf=cpf)
                animais = cliente.animais.all()
               
            except Cliente.DoesNotExist:
                messages.error(request, "Cliente não encontrado.")

            form = ConsultaForm()

        elif "salvar" in request.POST:
            form = ConsultaForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Consulta agendada com sucesso!')
                return redirect('lista_consultas')
            else:
                form._errors.clear()
                messages.error(request, 'Problemas ao enviar os dados, tente novamente.') 
    else:
        form = ConsultaForm()

    print(animais)
    return render(request, 
                  'agendar_consulta.html',
                  {'form': form, 'cliente' : cliente, 'animais':animais} )



def lista_animais(request):
    animais = Animal.objects.all()
    return render(request, 
                  'lista_animais.html', 
                  {'animais' : animais}
                  )

def lista_consultas(request):
    consultas = Consulta.objects.all().order_by('data')
    return render(request, 'lista_consultas.html', {'consultas':consultas})

# Adiciona animal 
def add_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)

        if form.is_valid():
            animal = form.save(commit=False)
            cpf = request.POST.get("cpf")
            #animal.dono = Cliente.objects.get(cpf=cpf)
            animal.doneo = Cliente.objects.get(cpf=cpf)
            animal.save()
            return JsonResponse({'id':animal.id, 'nome' : animal.nome})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = AnimalForm()

    return render(request, 'add_animal_modal.html', {'form':form})