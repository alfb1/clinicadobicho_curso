from django import forms
from .models  import Consulta, Animal, Cliente

# Formulário para o modulo Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['animal', 'veterinario', 'data', 'motivo', 'observacoes']
        widgets = {'data': forms.DateTimeInput(attrs={'type':'datetime-local'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        veterinario = cleaned_data.get('veterinario')

        if data and veterinario:
            qs = Consulta.objects.filter( data=data, veterinario=veterinario)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    'Já existe uma consulta agendada neste horário para este veterinário.'
                )

        #if Consulta.objects.filter( data=data, veterinario=veterinario).exists():
        #    raise forms.ValidationError('Já existe uma consulta agendada neste horário para este veterinário.')
        
        return cleaned_data

# Formulário para o modelo Animal
class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'especie', 'raca', 'idade', 'peso']
        widgets = {
            'nome': forms.TextInput(attrs={'class':'form-control'}),
            'idade': forms.NumberInput(attrs={'class':'form-control'}),
            'especie': forms.Select(attrs={'class':'form-control'}),
            'raca': forms.TextInput(attrs={'class':'form-control'}),
            'peso': forms.NumberInput(attrs={'class':'form-control'}),
        }

# Formulário para o modelo Cliente
class ClienteForm(forms.ModelForm):
    model = Cliente 
    fields  = [ 'nome', 'cpf', 'telefone', 'email', 'endereco']
    widgets = { 'endereco': forms.TextInput(attrs={'rows':3}), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})