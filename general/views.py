import json
#-----------------------------------
from django.views.generic import View, ListView, CreateView, DetailView,DeleteView
from django.shortcuts import render
from django.core.serializers import serialize
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse, FileResponse
from rest_framework import viewsets,permissions
#-----------------------------------
from .models import *
from .serializers import *

class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request,'adminlte/top-nav.html',{})

class CreacionCatalogo(View):
    def post(self, request, *args, **kwargs):
        propietario = request.POST['propietario']
        catalogo = CatalogoCuentas(propietario=propietario)
        catalogo.save()
        
        return HttpResponse('POST request!')


class SubcuentaViewSet(viewsets.ModelViewSet):
    queryset = SubCuenta.objects.all()
    serializer_class = SubCuentaSerializer


class CuentaVieSet(viewsets.ModelViewSet):
    queryset = CuentaPrincipal.objects.all()
    serializer_class = CuentaSerializer


class CatalogoVieSet(viewsets.ModelViewSet):
    queryset = CatalogoCuentas.objects.all()
    serializer_class = CatalogoSerializer


class ClienteVieSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class PartidaVieSet(viewsets.ModelViewSet):
    queryset = Partida.objects.all()
    serializer_class = PartidaSerializer


class TransaccionVieSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer
 