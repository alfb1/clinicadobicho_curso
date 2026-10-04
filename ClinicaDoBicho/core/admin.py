from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Cliente, Animal, Veterinario, Consulta

admin.site.register(Cliente)
admin.site.register(Animal)
admin.site.register(Veterinario)
admin.site.register(Consulta)
