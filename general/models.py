from django.db import models

class AuxiliarDiarioMayor(models.Model):
    mes = models.IntegerField(("Mes"),choices = (
        (1,"Enero"),(2,"Febrero"),(3,"Marzo"),(4,"Abril"),
        (5,"Mayo"),(6,"Junio"),(7,"Julio"),(8,"Agosto"),
        (9,"Septiembre"),(10,"Octubre"),(11,"Noviembre"),(12,"Diciembre"),
    ))
    ano = models.IntegerField(("Ano"))
    cliente = models.ForeignKey("controliva.Cliente", verbose_name=("Cliente"), on_delete=models.CASCADE)
    creado = models.DateTimeField(("Creado"),auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = ("Libro Auxiliar Diario Mayor")
        verbose_name_plural = ("Libros Auxiliar Diario Mayor")

    def __str__(self):
        return f'{self.mes}-{self.ano}-{self.cliente}'

 
class DiarioMayor(models.Model):
    mes = models.IntegerField(("Mes"),choices = (
        (1,"Enero"),(2,"Febrero"),(3,"Marzo"),(4,"Abril"),
        (5,"Mayo"),(6,"Junio"),(7,"Julio"),(8,"Agosto"),
        (9,"Septiembre"),(10,"Octubre"),(11,"Noviembre"),(12,"Diciembre"),
    ))
    ano = models.IntegerField(("Ano"))
    cliente = models.ForeignKey("controliva.Cliente", verbose_name=("Cliente"), on_delete=models.CASCADE)
    creado = models.DateTimeField(("Creado"),auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name =("Libro Diario Mayor")
        verbose_name_plural = ("Libros Diario Mayor")

    def __str__(self):
        return f'{self.mes}-{self.ano}-{self.cliente}'


class CatalogoCuentas(models.Model):
    propietario = models.ForeignKey("controliva.Cliente", verbose_name=("Propietario"), on_delete=models.CASCADE)
    creado = models.DateTimeField(("Creado"),auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'{self.propietario}'

    class Meta:
        verbose_name = 'Catalogo de Cuentas'
        verbose_name_plural = 'Catalogos de Cuentas'


class CuentaPrincipal(models.Model):
    catalogo = models.ForeignKey("general.CatalogoCuentas", verbose_name=("Catalogo de Cuentas"), on_delete=models.CASCADE)
    codigo = models.CharField(("Codigo"), max_length=15)    
    nombre = models.CharField(("Nombre"), max_length=150)
    creado = models.DateTimeField(("Creado"),auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = ("Cuenta Principal")
        verbose_name_plural = ("Cuentas Principales")

    def __str__(self):
        return f'{self.nombre}-:-{self.codigo}'


class SubCuenta(models.Model):
    codigo = models.CharField(("Codigo"), max_length=15)    
    nombre = models.CharField(("Nombre"), max_length=150)
    cuenta_padre = models.ForeignKey('general.SubCuenta', verbose_name=("Cuenta Padre"),on_delete=models.CASCADE,blank=True, null=True)
    cuenta_principal = models.ForeignKey("general.CuentaPrincipal", verbose_name=("Cuenta Principal"), on_delete=models.CASCADE,blank=True, null=True)
    catalogo = models.ForeignKey('general.CatalogoCuentas', on_delete=models.CASCADE)
    creado = models.DateTimeField(("Creado"),auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = ("Subcuenta")
        verbose_name_plural = ("Subcuentas")

    def __str__(self):
        return f'{self.nombre}-:-{self.codigo}'
            

class Partida(models.Model):
    fecha = models.DateField(("Fecha"), auto_now=False, auto_now_add=False)
    libro_auxiliar = models.ForeignKey("general.AuxiliarDiarioMayor", verbose_name=("Libro Auxiliar"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Partida")
        verbose_name_plural = ("Partidas")

    def __str__(self):
        return self.fecha


class Transaccion(models.Model):
    fecha = models.DateField(("Fecha"), auto_now=False, auto_now_add=False)
    monto = models.FloatField(("Monto"))
    creado = models.DateTimeField(("Creado"),auto_now=False, auto_now_add=True)
    subcuenta = models.ForeignKey("general.SubCuenta", verbose_name=(""), on_delete=models.CASCADE)
    partida = models.ForeignKey("general.Partida", verbose_name=("Partida"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Transaccion")
        verbose_name_plural = ("Transacciones")

    def __str__(self):
        return f'{self.fecha}-{self.subcuenta}'
