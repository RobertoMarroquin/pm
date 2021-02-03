import json
#-----------------------------------------------------------#
from django.core.serializers import serialize
from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, DetailView,DeleteView
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse, FileResponse
#from bootstrap_modal_forms.generic import BSModalCreateView


#-----------------------------------------------------------#
from .models import *
from .forms import  EmpresaForm, NuevoCliente, LibroForm, ConsumidorFinalForm,ComprasForm,ContribuyenteForm
from .export import *
class Home(View):
    def get(self, request, *args, **kwargs):

        return render(request,"home.html",{})

class Clientes(View):
    contexto={}
    clientes = list(Cliente.objects.all())

    def get(self, request, *args, **kwargs):
        self.clientes = list(Cliente.objects.all())
        form = NuevoCliente()
        self.contexto.update({'clientes':self.clientes,'form':form})
        return render(request,"controliva/listaClientes.html",self.contexto)

    def post(self, request, *args, **kwargs):
        self.clientes = list(Cliente.objects.all())
        form = NuevoCliente(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            print(form.cleaned_data)
            
            nuevoCliente = Cliente(
                    nRegistro=d.get('nRegistro'),
                    nombre=d.get('nombre'),
                    razonSocial=d.get('razonSocial'),
                    nit=d.get('nit'),
                    actEcon1=d.get('actEcon1'),
                    actEcon2=d.get('actEcon2'),
                    actEcon3=d.get('actEcon3'),
                    telefono=d.get("telefono"),
                    direccion=d.get('direccion')
                )
            
            nuevoCliente.save()

        self.contexto.update({'clientes':self.clientes,'form':form})
        return self.get(request)


class ClienteCreateView(CreateView):
    model = Cliente
    template_name = "controliva/modalCliente.html"
    form_class = NuevoCliente
   
    def get_success_url(self,**kwargs):
        return reverse('clientes')


class ClienteDetalle(DetailView):
    model = Cliente
    template_name='controliva/detalleCliente.html'


class LibroCreateView(CreateView):
    model = Libro
    template_name = "controliva/libros.html"
    form_class = LibroForm
    def get_initial(self,**kwargs):
        initial = super(LibroCreateView, self).get_initial()
        initial['tipo']=self.kwargs['tipo']
        initial['cliente']=Cliente.objects.get(id = self.kwargs['pk'])
        return initial

    def get_context_data(self,**kwargs):
        context = super(LibroCreateView,self).get_context_data(**kwargs)
        context["libros"] = list(Libro.objects.filter(cliente__id=self.kwargs['pk'],tipo=self.kwargs['tipo']))
        context['cliente'], context['tipo'] = Cliente.objects.get(id = self.kwargs['pk']),self.kwargs['tipo']
        
        return context
    
    def get_success_url(self,**kwargs):
        return reverse('libros',args=(self.kwargs['pk'], self.kwargs['tipo']))


class FacturaConsumidorFinalCreateView(CreateView):
    model = FacturaConsumidorFinal
    template_name = "controliva/librocf.html"
    form_class = ConsumidorFinalForm
    def get_initial(self,**kwargs):
        initial = super(FacturaConsumidorFinalCreateView, self).get_initial()
        initial['libro']=Libro.objects.get(id = self.kwargs['id'])
        return initial

    def get_context_data(self,**kwargs):
        context = super(FacturaConsumidorFinalCreateView,self).get_context_data(**kwargs)
        context["facts"] = list(FacturaConsumidorFinal.objects.filter(libro__id=self.kwargs['id']).order_by("-fecha"))
        context['libro'],context['cliente'], context['tipo'] = Libro.objects.get(id=self.kwargs['id']),Cliente.objects.get(id = self.kwargs['pk']),self.kwargs['tipo']
        return context
    
    def get_success_url(self,**kwargs):
        return reverse('librocf',args=(self.kwargs['pk'], self.kwargs['tipo'],self.kwargs['id']))


class FacturaComprasCreateView(CreateView):
    model = FacturaCompras
    template_name = "controliva/librocm.html"
    form_class = ComprasForm

    def get_initial(self,**kwargs):
        initial = super(FacturaComprasCreateView, self).get_initial()
        initial['libro']=Libro.objects.get(id = self.kwargs['id'])
        return initial

    def get_context_data(self,**kwargs):
        context = super(FacturaComprasCreateView,self).get_context_data(**kwargs)
        context["facts"] = list(FacturaCompras.objects.filter(libro__id=self.kwargs['id']))
        context['libro'],context['cliente'], context['tipo'] = Libro.objects.get(id=self.kwargs['id']),Cliente.objects.get(id = self.kwargs['pk']),self.kwargs['tipo']
        return context

    def get_success_url(self,**kwargs):
        return reverse('librocm',args=(self.kwargs['pk'], self.kwargs['tipo'],self.kwargs['id']))


class FacturaContribuyenteCreateView(CreateView):
    model = FacturaContribuyente
    template_name = "controliva/libroct.html"
    form_class = ContribuyenteForm

    def get_initial(self,**kwargs):
        initial = super(FacturaContribuyenteCreateView, self).get_initial()
        initial['libro']=Libro.objects.get(id = self.kwargs['id'])
        return initial

    def get_context_data(self,**kwargs):
        context = super(FacturaContribuyenteCreateView,self).get_context_data(**kwargs)
        context["facts"] = list(FacturaContribuyente.objects.filter(libro__id=self.kwargs['id']))
        context['libro'],context['cliente'], context['tipo'] = Libro.objects.get(id=self.kwargs['id']),Cliente.objects.get(id = self.kwargs['pk']),self.kwargs['tipo']
        return context
    
    def get_success_url(self,**kwargs):
        return reverse('libroct',args=(self.kwargs['pk'], self.kwargs['tipo'],self.kwargs['id']))



class EmpresaDetail(DetailView):
    model = Empresa
    template_name='empresaJson.html'
    def get(self,request,*args, **kwarg ):
        empresa = Empresa.objects.get(nRegistro = self.kwargs['nReg'])
        empresa = serialize('json',[empresa,]) 
        return HttpResponse(empresa,'application/json')

class ExportarView(View):
    def get(self, request, *args, **kwargs):
        tipo = self.kwargs.get('tipo')
        id_libro = self.kwargs.get('id_libro')
        libro = Libro.objects.get(id=id_libro)
        
        if tipo == 1:
            tipol = "Consumidor"
            libroEx = export_libroCF(id_libro)
        elif tipo == 2:
            tipol = "Contibuyente"
            libroEx = export_libroct(id_libro)
        elif tipo == 3:
            tipol = "Compras"
            libroEx = export_librocm(id_libro)
        print(libro)
        # create the HttpResponse object ...
        response = FileResponse(open(libroEx.filename, 'rb'))
        return response


class EmpresaCreateView(CreateView):
    model = Empresa
    template_name = "controliva/empresa.html"
    form_class = EmpresaForm

    def get_success_url(self,**kwargs):
        return reverse('empresa')
    

def factCFDelete(self,request):
    if request.method == "POST":
        idfact = request.POST["pk"]
        fact = FacturaConsumidorFinal.objects.get(id = idfact)
        fact.delete()

