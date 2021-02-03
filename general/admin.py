from django.contrib import admin
from .models import *

@admin.register(CuentaPrincipal)
class CuentaPrincipalAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre','creado','catalogo')

@admin.register(SubCuenta)
class SubCuentaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre','cuenta_padre','cuenta_principal','creado')
    #list_filter = ('',)
    search_fields = ('nombre','codigo')

@admin.register(AuxiliarDiarioMayor)
class AuxiliarDiarioMayorAdmin(admin.ModelAdmin):
    list_display = ('mes','ano','cliente','creado')
    #list_filter = ('cliente',)
    search_fields = ('mes','ano',)

@admin.register(DiarioMayor)
class DiarioMayorAdmin(admin.ModelAdmin):
    list_display = ('mes','ano','cliente','creado')
    #list_filter = ('cliente',)
    search_fields = ('mes','ano',)

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('fecha','monto','subcuenta')
    list_filter = ('subcuenta',)
    search_fields = ('fecha','monto','subcuenta')


class CuentaPrincipalInline(admin.TabularInline):
    model = CuentaPrincipal
    min_num = 1
    extra = 1
    raw_id_fields = ('catalogo',)


@admin.register(CatalogoCuentas)
class CatalogoCuentasAdmin(admin.ModelAdmin):
    '''Admin View for CatalogoCuentas'''

    list_display = ('propietario','creado')
    inlines = [
        #CuentaPrincipalInline,
    ]
