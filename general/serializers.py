from .models import *
from controliva.models import Cliente
from rest_framework import serializers


class PartidaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Partida
        fields = ['fecha', 'libro_auxiliar']


class SubCuentaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCuenta
        fields = [
            'codigo',
            'nombre',
            'cuenta_padre',
            'cuenta_principal',
            'catalogo',
            'creado',
        ]


class CuentaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CuentaPrincipal
        fields = [
            'codigo',
            'nombre',
            'catalogo',
            'creado',
        ]


class CatalogoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CatalogoCuentas
        fields = [
            'propietario',
            'creado',
        ]


class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields=[
            'nRegistro',
            'nombre',
            'nit',
        ]


class TransaccionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaccion
        fields = [
            'fecha',
            'monto',
            'creado',
            'subcuenta',
            'partida',
        ]
