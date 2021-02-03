from django import forms
from django.core.exceptions import ValidationError
#from bootstrap_modal_forms.forms import BSModalModelForm


from .models import Empresa, Libro, FacturaCompras,FacturaConsumidorFinal,FacturaContribuyente, Cliente

class EmpresaForm(forms.ModelForm):
    
    class Meta:
        model = Empresa
        fields = (  "nRegistro",
                    "nombre",
                    "nit",
                )
        widgets = {
            "nit"   :  forms.TextInput(attrs={'data-mask':"0000-000000-000-0"}),
        }
    


class NuevoCliente(forms.ModelForm):
    nRegistro   =  forms.CharField(label='No Registro',widget=forms.TextInput(attrs={"placeholder":"Numero de Registro"}), max_length=100, required=True)
    nombre      =  forms.CharField(label='Nombre',widget=forms.TextInput(attrs={"placeholder":"Nombre"}), max_length=100, required=True)
    razonSocial =  forms.CharField(label='Razon Social',widget=forms.TextInput(attrs={"placeholder":"Razon Social"}), max_length=100, required=False)
    nit         =  forms.CharField(label='NIT',widget=forms.TextInput(attrs={'data-mask':"0000-000000-000-0"}), max_length=18, required=True)
    actEcon1    =  forms.CharField(label='Actividad Economica 1',widget=forms.TextInput(attrs={"placeholder":"Actividad Economica 1"}), max_length=100, required=False)
    actEcon2    =  forms.CharField(label='Actividad Economica 2',widget=forms.TextInput(attrs={"placeholder":"Actividad Economica 2"}), max_length=100, required=False)
    actEcon3    =  forms.CharField(label='Actividad Economica 3',widget=forms.TextInput(attrs={"placeholder":"Actividad Economica 3"}), max_length=100, required=False)
    telefono    =  forms.CharField(label='Telefono',widget=forms.TextInput(attrs={'data-mask':"0000-0000"}), max_length=100, required=False)
    direccion   =  forms.CharField(
            label='Direccion',
            widget=forms.Textarea(attrs={"rows":"2","cols":"50"}),
            max_length=200,
            required=False
        )

    class Meta:
        model = Cliente
        fields = (
            "nRegistro",  
            "nombre",     
            "razonSocial",
            "nit",        
            "actEcon1",   
            "actEcon2",   
            "actEcon3",   
            "telefono",   
            "direccion",    
        )
    
    def clean_nRegisto(self):
        data = self.cleaned_data['nRegisto']
        if data in Cliente.objects.all():
            raise ValidationError("Numero de registro ya existe")

       
class LibroForm(forms.ModelForm):
    
    class Meta:
        model = Libro
        fields = ('mes','ano','tipo','cliente')
        widgets = {
            'ano'       :forms.NumberInput(attrs={'max': 2050,'min':2000}),
            'tipo'      :forms.HiddenInput(),
            'cliente'   :forms.HiddenInput(),
            }

class ContribuyenteForm(forms.ModelForm):
    fecha = forms.DateField(input_formats=["%d/%m/%Y","%d/%m/%y"],
            widget=forms.DateInput(attrs={"data-mask":"00/00/00"}),
            required=False)
    falsoContribuyente = forms.CharField(widget=forms.TextInput(attrs={"":""}),
            required=True,label="Contribuyente")
    class Meta:
        model = FacturaContribuyente
        fields = ("correlativo",
                    "fecha",
                    #"nComprobacion",
                    "serie",
                    "corrIntUni",
                    "contribuyente",
                    'falsoContribuyente',
                    "venExentas",
                    "venGravadas",
                    "ventasNSujetas",
                    "ivaDebFiscal",
                    "vtVentas",
                    "vtIVA",
                    "ivaRetenido",
                    "total",
                    "libro"
                    )
        widgets = {
            "correlativo"   :  forms.TextInput(attrs={"required":"true","autofocus":"true"}),
            #"fecha"        :  forms.DateInput(attrs={"":""}),
            #"nComprobacion" :  forms.TextInput(attrs={"":""}),
            "serie"         :  forms.NumberInput(attrs={"":""}),
            "contribuyente" :  forms.HiddenInput,
            "corrIntUni"    :  forms.NumberInput(attrs={}),
            "venExentas"    :  forms.NumberInput(attrs={"value":"0.00"}),
            "venGravadas"   :  forms.NumberInput(attrs={"value":"0.00"}),
            "ivaDebFiscal"  :  forms.NumberInput(attrs={"value":"0.00"}),
            "vtVentas"      :  forms.NumberInput(attrs={"value":"0.00"}),
            "vtIVA"         :  forms.NumberInput(attrs={"value":"0.00"}),
            "ivaRetenido"   :  forms.NumberInput(attrs={"value":"0.00"}),
            "total"         :  forms.NumberInput(attrs={"value":"0.00","readonly":"true"}),
            "ventasNSujetas":  forms.NumberInput(attrs={"value":"0.00"}),
            "libro"         :  forms.HiddenInput(attrs={"":""}),
        }


class ConsumidorFinalForm(forms.ModelForm):
    fecha = forms.DateField(input_formats=["%d/%m/%Y","%d/%m/%y"],
            widget=forms.DateInput(attrs={"data-mask":"00/00/00"}),
            required=False)
    class Meta:
        model = FacturaConsumidorFinal
        fields =(
            "correlativoInicial",
            "correlativoFinal",
            "fecha" ,
            "exento",
            "locales" ,
            "exportaciones",
            "ventasNSujetas",
            "ventaTotal",
            "ventaCtaTerceros",
            "libro", 
        )
        widgets = {
            "correlativoInicial"    : forms.NumberInput(attrs={"autofocus":"true"}),
            "correlativoFinal"      : forms.NumberInput(attrs={"":""}),
            #"fecha"                : forms.DateInput(attrs={"data-mask":"00/00/2000"}),
            "exento"                : forms.NumberInput(attrs={"value":"0.00"}),
            "locales"               : forms.NumberInput(attrs={"value":"0.00"}),
            "ventaTotal"            : forms.NumberInput(attrs={"value":"0.00","readonly":"true"}),
            "ventaCtaTerceros"      : forms.NumberInput(attrs={"value":"0.00"}),
            "exportaciones"         : forms.NumberInput(attrs={"value":"0.00"}),
            "ventasNSujetas"        : forms.NumberInput(attrs={"value":"0.00"}),
            "libro"                 : forms.HiddenInput(attrs={"":""}),
        }


class ComprasForm(forms.ModelForm):
    fecha = forms.DateField(input_formats=["%d/%m/%Y","%d/%m/%y"],
            widget=forms.DateInput(attrs={"data-mask":"00/00/00"}),
            required=False)
    falsaEmpresa = forms.CharField(widget=forms.TextInput(attrs={"":""}),
            required=True,label="Proveedor")
    class Meta:
        model = FacturaCompras
        fields =(
        "correlativo",       
        "fecha",              
        "empresa",
        "falsaEmpresa",           
        "cExenteInterna",     
        "cExenteImportaciones", 
        "cGravadaInterna",     
        "cGravadaImportaciones",
        "comprasNSujetas",
        "ivaCdtoFiscal",     
        "totalCompra",        
        "retencionPretencion",
        "anticipoCtaIva",     
        "ivaTerceros",
        "libro",   
        )    

        widgets = {
        "correlativo"          : forms.NumberInput(attrs={"autofocus":"true"}),
        #"fecha"                : forms.TextInput(attrs={"":""}),
        "empresa"              : forms.HiddenInput(attrs={"":""}),
        "cExenteInterna"       : forms.NumberInput(attrs={"value":"0.00"}),
        "cExenteImportaciones" : forms.NumberInput(attrs={"value":"0.00"}),
        "cGravadaInterna"      : forms.NumberInput(attrs={"value":"0.00"}),
        "cGravadaImportaciones": forms.NumberInput(attrs={"value":"0.00"}),
        "ivaCdtoFiscal"        : forms.NumberInput(attrs={"value":"0.00"}),
        "totalCompra"          : forms.NumberInput(attrs={"value":"0.00","readonly":"true"}),
        "retencionPretencion"  : forms.NumberInput(attrs={"value":"0.00"}),
        "anticipoCtaIva"       : forms.NumberInput(attrs={"value":"0.00"}),
        "ivaTerceros"          : forms.NumberInput(attrs={"value":"0.00"}),
        "comprasNSujetas"      : forms.NumberInput(attrs={"value":"0.00"}),
        "libro"                : forms.HiddenInput(attrs={"":""}),
        }