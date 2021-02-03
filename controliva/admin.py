from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(FacturaCompras)
class FacturaComprasAdmin(admin.ModelAdmin):
    '''Admin View for FacturaCompras'''

    list_display = ('correlativo','empresa','fecha','libro')
    search_by = ('libro','correlativo','fecha')
    

@admin.register(FacturaContribuyente)
class FacturaContribuyenteAdmin(admin.ModelAdmin):
    '''Admin View for FacturaContribuyente'''

    list_display = ('correlativo','fecha','contribuyente','libro')
    search_by = ('libro','correlativo','fecha')
    
    

@admin.register(FacturaConsumidorFinal)
class FacturaConsumidorFinalAdmin(admin.ModelAdmin):
    '''Admin View for FacturaConsumidorFinal'''

    list_display = ('correlativoInicial','correlativoFinal','fecha','libro')
    search_by = ('libro','correlativoInicial','correlativoFinal','fecha')
    
    

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    '''Admin View for Empresa'''

    list_display = ('nRegistro','nombre','nit')
    search_by = ('nRegistro','nombre','nit')
   


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    '''Admin View for Libro'''

    list_display = ("id",'mes','ano','cliente',"tipo")
    search_by = ('mes','ano',)
    

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    '''Admin View for Cliente'''

    list_display = ('nRegistro','nombre','nit',)
    search_by = ('nRegistro','nombre','nit',)
    