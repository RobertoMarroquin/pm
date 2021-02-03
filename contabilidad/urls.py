"""contabilidad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from controliva.views import *
from general.views import *

router = routers.DefaultRouter()
router.register(r'subcuentas', SubcuentaViewSet)
router.register(r'cuentas', CuentaVieSet)
router.register(r'partidas', PartidaVieSet)
router.register(r'transacciones', TransaccionVieSet)
router.register(r'catalogos', CatalogoVieSet)
router.register(r'clientes', ClienteVieSet)

admin.site.site_header = "Administracion DGO"
admin.site.site_title = "AdministracionDGO"
admin.site.index_title = "Bienvenido al Portal de Administracion"

urlpatterns = [
    path('admin/', admin.site.urls),
    #path("", Home.as_view(), name="home"),
    path("", Clientes.as_view(), name="clientes"),
    path("iva/cliente/<int:pk>/", ClienteDetalle.as_view(), name="cliente"),
    path("iva/cliente/<int:pk>/libros/<int:tipo>/", LibroCreateView.as_view(), name="libros"),
    path("iva/cliente/<int:pk>/libros/<int:tipo>/consumidorfinal/<int:id>/", FacturaConsumidorFinalCreateView.as_view(), name="librocf"),
    path("iva/cliente/<int:pk>/libros/<int:tipo>/contribuyente/<int:id>/", FacturaContribuyenteCreateView.as_view(), name="libroct"),
    path("iva/cliente/<int:pk>/libros/<int:tipo>/compras/<int:id>/", FacturaComprasCreateView.as_view(), name="librocm"),
    path("empresa/<slug:nReg>/", EmpresaDetail.as_view(), name="detalle"),
    path("libro/<int:id_libro>/<int:tipo>", ExportarView.as_view(), name="export"),
    path("empresa/",EmpresaCreateView.as_view(),name="empresa"),
    path("crear_cliente", ClienteCreateView.as_view(), name="crear_cliente"),
    path("api/", include(router.urls)),
]

