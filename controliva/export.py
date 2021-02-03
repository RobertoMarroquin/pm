import numpy as np
import pandas as pd
import openpyxl as ox
import xlsxwriter as xw
import matplotlib.pyplot as plt
import os

from decimal import Decimal as dec

from django.utils.dateformat import DateFormat
from django.db.models import Sum

from .models import *
from contabilidad.settings import BASE_DIR

def export_libroCF(libro_id):
    libro = Libro.objects.get(id=libro_id)
    facturas = FacturaConsumidorFinal.objects.order_by("correlativoInicial","fecha").filter(libro=libro).values()
    facturas_limpias = []
    #Creacion de de lista para dataFrame 
    for fact in facturas:
        factura_dict = {}
        fecha = DateFormat(fact.get("fecha"))

        factura_dict.update({
            "Correlativo Inicial":fact.get("correlativoInicial"),
            "Correlativo Final":fact.get("correlativoFinal"),
            "Fecha": fecha.format('d/m/Y'),
            "Exento":fact.get("exento"),
            "Locales":fact.get("locales"),
            "Exportaciones":fact.get("exportaciones"),
            "Ventas No Sujetas":fact.get("ventasNSujetas"),
            "Ventas Cta Terceros": fact.get("ventaCtaTerceros"),
            "Venta Total":fact.get("ventaTotal"),
        })
        facturas_limpias.append(factura_dict)
    #Creacion de objeto Excel para posterior salida
    writer = pd.ExcelWriter(
        BASE_DIR/f"libros_consumidor/{libro.cliente.nombre}_{libro.mes}_{libro.ano}_condumidorFinal.xlsx", 
        engine='xlsxwriter')
    
    df_facturas = pd.DataFrame(facturas_limpias)

    workbook  = writer.book
    df = df_facturas
    if libro.mes == 1 : mes = "ENERO"
    elif libro.mes == 2 : mes = "FEBRERO"
    elif libro.mes == 3 : mes = "MARZO"
    elif libro.mes == 4 : mes = "ABRIL"
    elif libro.mes == 5 : mes = "MAYO"
    elif libro.mes == 6 : mes = "JUNIO"
    elif libro.mes == 7 : mes = "JULIO"
    elif libro.mes == 8 : mes = "AGOSTO"
    elif libro.mes == 9 : mes = "SEPTIEMBRE"
    elif libro.mes == 10 : mes = "OCTUBRE"
    elif libro.mes == 11 : mes = "NOVIEMBRE"
    elif libro.mes == 12 : mes = "DICIEMBRE"
            
    bandera = 1
    #Si hay mas de 25 registros se creara una hoja por cada 20
    while len(df) >=25:
        df[:25].to_excel(writer,sheet_name=f"HOJA{bandera}",index=False,startrow=6,header=False)
        worksheet = writer.sheets[f"HOJA{bandera}"]
        #Configuracion de pagina
        worksheet.set_portrait()
        worksheet.set_paper(1)
        worksheet.set_margins(0.26,0.26,0.75,0.75)
        #formato de cabecera
        header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        "font_size":9, 
        })
        header_format.set_align("center")
        header_format.set_align("vcenter")
        #Ecritura de cabecera
        for col_num, value in enumerate(df_facturas.columns.values):
            worksheet.write(5, col_num, value, header_format)
        formato = workbook.add_format()
        formato.set_align("left")
        formato_data = workbook.add_format()
        formato_data.set_align("center")
        formato_data.set_bottom()
        formato_data.set_font_size(7)
        worksheet.set_column(2,2,8)
        worksheet.set_column(0,1,8)
        worksheet.set_column(6,7,9)
        worksheet.set_column(3,5,8)
        worksheet.set_row(5,30)
        for row in range(6,31):
            worksheet.set_row(row,20,formato_data)
        #Excritura de formato de libro
        worksheet.merge_range('A1:I1',f'{libro.cliente.nombre}',formato)
        worksheet.merge_range('A2:I2',f'NIT: {libro.cliente.nit}',formato)
        worksheet.merge_range('A3:I3',f'Numero de Registro: {libro.cliente.nRegistro}',formato)
        worksheet.merge_range('A4:I4',f'LIBRO DE VENTAS A CONSUMIDOR FINAL. MES DE {mes}/{libro.ano}',formato)
        worksheet.merge_range('A5:I5','EN DOLARES AMERICANOS',formato)
        bandera+=1
        df=df[25:]
    df.to_excel(writer,sheet_name=f"HOJA{bandera}",index=False,startrow=6,header=False)
    worksheet = writer.sheets[f"HOJA{bandera}"]
    #Configuracion de pagina
    worksheet.set_portrait()
    worksheet.set_paper(1)
    worksheet.set_margins(0.26,0.26,0.75,0.75)
    #formato de cabecera
    header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'border': 1,
    "font_size":9,
    })
    header_format.set_align("center")
    header_format.set_align("vcenter")
    #Ecritura de cabecera
    for col_num, value in enumerate(df_facturas.columns.values):
        worksheet.write(5, col_num, value, header_format)
    formato = workbook.add_format()
    formato.set_align("left")
    formato_data = workbook.add_format()
    formato_data.set_align("center")
    formato_data.set_bottom()
    formato_data.set_font_size(7)
    worksheet.set_column(2,2,8)
    worksheet.set_column(0,1,8)
    worksheet.set_column(6,7,9)
    worksheet.set_column(3,5,8)
    worksheet.set_row(5,30)
    for row in range(6,len(df)+9):
        worksheet.set_row(row,20,formato_data)
    #Excritura de formato de libro
    worksheet.merge_range('A1:I1',f'{libro.cliente.nombre}',formato)
    worksheet.merge_range('A2:I2',f'NIT: {libro.cliente.nit}',formato)
    worksheet.merge_range('A3:I3',f'Numero de Registro: {libro.cliente.nRegistro}',formato)
    worksheet.merge_range('A4:I4',f'LIBRO DE VENTAS A CONSUMIDOR FINAL. MES DE {mes}/{libro.ano}',formato)
    worksheet.merge_range('A5:I5','EN DOLARES AMERICANOS',formato)
    resumen  = [
        facturas.aggregate(Sum('exento')),
        facturas.aggregate(Sum("locales")),
        facturas.aggregate(Sum("exportaciones")),
        facturas.aggregate(Sum("ventaTotal")),
        ]
    iva = float(resumen[1].get("locales__sum") / dec(1.13))
    ventSin = float(resumen[1].get("locales__sum")) - iva
    resumen.append({"iva":iva})
    resumen.append({"ventasSinIva":ventSin})
    worksheet.merge_range(f'A{len(df)+7}:B{len(df)+7}','TOTALES',header_format)
    worksheet.write(len(df)+6,3,f"{round(resumen[0].get('exento__sum'),2)}")
    worksheet.write(len(df)+6,4,f"{round(resumen[1].get('locales__sum'),2)}")
    worksheet.write(len(df)+6,5,f"{round(resumen[2].get('exportaciones__sum'),2)}")
    worksheet.write(len(df)+6,8,f"{round(resumen[3].get('ventaTotal__sum'),2)}")
    worksheet.merge_range(f'B{len(df)+8}:D{len(df)+8}','Venta',formato_data)
    worksheet.write(len(df)+8,4,f"{round(resumen[5].get('ventasSinIva'),2):.2f}")
    worksheet.merge_range(f'B{len(df)+9}:D{len(df)+9}','IVA 13%',formato_data)
    worksheet.write(len(df)+7,4,f"{round(resumen[4].get('iva'),2):.2f}")
    writer.save()
    return writer.book
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
def export_librocm(libro_id):
    libro = Libro.objects.get(id=libro_id)
    facturas = FacturaCompras.objects.filter(libro=libro).order_by('fecha').values()
    facturas_limpias = []
    ci = 1
    #Creacion de de lista para dataFrame 
    for fact in facturas:
        factura_dict = {}
        fecha = DateFormat(fact.get("fecha"))
        empresa = int(fact.get("empresa_id"))
        empresa = Empresa.objects.get(id=empresa)
        factura_dict.update({
            "Correlativo":ci,
            "Fecha": fecha.format('d/m/Y'),
            "Num. de Comprobante":fact.get("correlativo"),
            "Num de Registro":empresa.nRegistro,
            "Empresa":empresa.nombre,
            "Com. Exe. Inter.":fact.get("cExenteInterna"),
            "Com. Exe. Impor.":fact.get("cExenteImportaciones"),
            "Com. Gra. Inter.":fact.get("cGravadaInterna"),
            "Com. Gra. Impor.":fact.get("cGravadaImportaciones"),
            "Compras No Sujetas":fact.get("comprasNSujetas"),
            "IVA Cdto Fiscal":fact.get("ivaCdtoFiscal"),
            "Compra Total":fact.get("totalCompra"),
            "Ret. Percep. 1%":fact.get("retencionPretencion"),
            "Ant. a Cta IVA 2%":fact.get("anticipoCtaIva"),
            "IVA Terceros": fact.get("ivaTerceros"),
        })
        facturas_limpias.append(factura_dict)
        ci+=1
    #Creacion de objeto Excel para posterior salida
    writer = pd.ExcelWriter(
        BASE_DIR/f"libros_compras/{libro.cliente.nombre}_{libro.mes}_{libro.ano}_compras.xlsx", 
        engine='xlsxwriter')
    
    df_facturas = pd.DataFrame(facturas_limpias)

    workbook  = writer.book
    df = df_facturas
    if libro.mes == 1 : mes = "ENERO"
    elif libro.mes == 2 : mes = "FEBRERO"
    elif libro.mes == 3 : mes = "MARZO"
    elif libro.mes == 4 : mes = "ABRIL"
    elif libro.mes == 5 : mes = "MAYO"
    elif libro.mes == 6 : mes = "JUNIO"
    elif libro.mes == 7 : mes = "JULIO"
    elif libro.mes == 8 : mes = "AGOSTO"
    elif libro.mes == 9 : mes = "SEPTIEMBRE"
    elif libro.mes == 10 : mes = "OCTUBRE"
    elif libro.mes == 11 : mes = "NOVIEMBRE"
    elif libro.mes == 12 : mes = "DICIEMBRE"  
    bandera = 1
    #Si hay mas de 10 registros se creara una hoja por cada 20
    while len(df) >=15:
        df[:15].to_excel(writer,sheet_name=f"HOJA{bandera}",index=False,startrow=6,header=False)
        worksheet = writer.sheets[f"HOJA{bandera}"]
        #Configuracion de pagina
        worksheet.set_landscape()
        worksheet.set_paper(1)
        worksheet.set_margins(0.26,0.26,0.75,0.75)
        #formato de cabecera
        header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        "font_size":8, 
        })
        header_format.set_align("center")
        header_format.set_align("vcenter")
        #Ecritura de cabecera
        for col_num, value in enumerate(df_facturas.columns.values):
            worksheet.write(5, col_num, value, header_format)
        formato = workbook.add_format()
        formato.set_align("left")
        formato_data = workbook.add_format()
        formato_data.set_align("center")
        formato_data.set_bottom()
        formato_data.set_font_size(7)
        worksheet.set_column(0,0,4)
        worksheet.set_column(1,3,7)
        worksheet.set_column(4,4,15)
        worksheet.set_column(5,9,6)
        worksheet.set_column(10,14,5)
        worksheet.set_row(5,40)
        for row in range(6,21):
            worksheet.set_row(row,20,formato_data)
        #Excritura de formato de libro
        worksheet.merge_range('A1:I1',f'{libro.cliente.nombre}',formato)
        worksheet.merge_range('A2:I2',f'NIT: {libro.cliente.nit}',formato)
        worksheet.merge_range('A3:I3',f'Numero de Registro: {libro.cliente.nRegistro}',formato)
        worksheet.merge_range('A4:I4',f'LIBRO DE COMPRAS. MES DE {mes}/{libro.ano}',formato)
        worksheet.merge_range('A5:I5','EN DOLARES AMERICANOS',formato)
        bandera+=1
        df=df[15:]
    df.to_excel(writer,sheet_name=f"HOJA{bandera}",index=False,startrow=6,header=False)
    worksheet = writer.sheets[f"HOJA{bandera}"]
    #Configuracion de pagina
    worksheet.set_landscape()
    worksheet.set_paper(1)
    worksheet.set_margins(0.26,0.26,0.75,0.75)
    #formato de cabecera
    header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'border': 1,
    "font_size":8,
    })
    header_format.set_align("center")
    header_format.set_align("vcenter")
    #Ecritura de cabecera
    for col_num, value in enumerate(df_facturas.columns.values):
        worksheet.write(5, col_num, value, header_format)
    formato = workbook.add_format()
    formato.set_align("left")
    formato_data = workbook.add_format()
    formato_data.set_align("center")
    formato_data.set_bottom()
    formato_data.set_font_size(7)
    worksheet.set_column(0,0,4)
    worksheet.set_column(1,3,7)
    worksheet.set_column(4,4,15)
    worksheet.set_column(5,9,6)
    worksheet.set_column(10,14,5)
    worksheet.set_row(5,40)
    for row in range(6,len(df)+9):
        worksheet.set_row(row,20,formato_data)
    #Excritura de formato de libro
    worksheet.merge_range('A1:I1',f'{libro.cliente.nombre}',formato)
    worksheet.merge_range('A2:I2',f'NIT: {libro.cliente.nit}',formato)
    worksheet.merge_range('A3:I3',f'Numero de Registro: {libro.cliente.nRegistro}',formato)
    worksheet.merge_range('A4:I4',f'LIBRO DE COMPRAS. MES DE {mes}/{libro.ano}',formato)
    worksheet.merge_range('A5:I5','EN DOLARES AMERICANOS',formato)
    total_comexin = round(facturas.aggregate(Sum('cExenteInterna')).get("cExenteInterna__sum"),2)
    total_comexim = round(facturas.aggregate(Sum('cExenteImportaciones')).get("cExenteImportaciones__sum"),2)
    total_comgrin = round(facturas.aggregate(Sum('cGravadaInterna')).get("cGravadaInterna__sum"),2)
    total_comgrim = round(facturas.aggregate(Sum('cGravadaImportaciones')).get("cGravadaImportaciones__sum"),2)
    total_ivacrdt = round(facturas.aggregate(Sum('ivaCdtoFiscal')).get("ivaCdtoFiscal__sum"),2)
    total_compras = round(facturas.aggregate(Sum('totalCompra')).get("totalCompra__sum"),2)
    total_retperc = round(facturas.aggregate(Sum('retencionPretencion')).get("retencionPretencion__sum"),2)
    total_antciva = round(facturas.aggregate(Sum('anticipoCtaIva')).get("anticipoCtaIva__sum"),2)
    total_ivaterc = round(facturas.aggregate(Sum('ivaTerceros')).get("ivaTerceros__sum"),2)
    total_nosujet = round(facturas.aggregate(Sum('comprasNSujetas')).get("comprasNSujetas__sum"),2)
    #Escritura lde totales
    worksheet.merge_range(f'A{len(df)+7}:B{len(df)+7}','TOTALES',header_format)
    worksheet.write(len(df)+6,5,f"{total_comexin}")
    worksheet.write(len(df)+6,6,f"{total_comexim}")
    worksheet.write(len(df)+6,7,f"{total_comgrin}")
    worksheet.write(len(df)+6,8,f"{total_comgrim}")
    worksheet.write(len(df)+6,9,f"{total_nosujet}")
    worksheet.write(len(df)+6,10,f"{total_ivacrdt}")
    worksheet.write(len(df)+6,11,f"{total_compras}")
    worksheet.write(len(df)+6,12,f"{total_retperc}")
    worksheet.write(len(df)+6,13,f"{total_antciva}")
    worksheet.write(len(df)+6,14,f"{total_ivaterc}")
    worksheet.write(len(df)+7,4,"Total Compras")
    worksheet.write(len(df)+8,4,"Total N/C")
    compras = FacturaCompras.objects.filter(libro=libro,cGravadaInterna__gte=dec(0.00))
    compras_t = round(compras.aggregate(Sum('cGravadaInterna')).get('cGravadaInterna__sum'),2) 
    iva_compras_t = round(compras.aggregate(Sum('ivaCdtoFiscal')).get('ivaCdtoFiscal__sum'),2) 
    notas_credito = FacturaCompras.objects.filter(libro=libro,cGravadaInterna__lt=dec(0.00))
    notas_credito_t = round(notas_credito.aggregate(Sum('cGravadaInterna')).get('cGravadaInterna__sum'),2) if len(notas_credito) > 0 else '0.00'
    iva_notas_credito_t = round(notas_credito.aggregate(Sum('ivaCdtoFiscal')).get('ivaCdtoFiscal__sum'),2) if len(notas_credito) > 0 else '0.00'
    worksheet.write(len(df)+7,7,f"{compras_t}")
    worksheet.write(len(df)+7,10,f"{iva_compras_t}")
    worksheet.write(len(df)+8,7,f"{notas_credito_t}")
    worksheet.write(len(df)+8,10,f"{iva_notas_credito_t}")
    writer.save()
    return writer.book
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
def export_libroct(libro_id):
    libro = Libro.objects.get(id=libro_id)
    facturas = FacturaContribuyente.objects.order_by("correlativo","fecha").filter(libro=libro).values()
    facturas_limpias = []
    ci = 1
    #Creacion de de lista para dataFrame 
    for fact in facturas:
        factura_dict = {}
        fecha = DateFormat(fact.get("fecha"))
        contribuyente = int(fact.get("contribuyente_id"))
        contribuyente = Empresa.objects.get(id=contribuyente)
        factura_dict.update({
            "Correlativo":ci,
            "Fecha": fecha.format('d/m/Y'),
            "Corr. Int. Uni.":fact.get("corrIntUni") if fact.get("corrIntUni") is not None else "",
            "Num. de Comprobante":fact.get("correlativo"),
            "Num de Registro":contribuyente.nRegistro,
            "Contribuyente":contribuyente .nombre,
            "Vent. Exe.":fact.get("venExentas"),
            "Vent. Gra.":fact.get("venGravadas"),
            "Ventas No Sujetas":fact.get("ventasNSujetas"),
            "IVA Dbto Fiscal":fact.get("ivaDebFiscal"),
            "Ventas Terceros":fact.get("vtVentas"),
            "IVA Terceros":fact.get("vtIVA"),
            "Iva Retenido":fact.get("ivaRetenido"),
            "Venta Total": fact.get("total"),
        })
        facturas_limpias.append(factura_dict)
        ci+=1
    #Creacion de objeto Excel para posterior salida
    writer = pd.ExcelWriter(
        BASE_DIR/f"libros_contribuyente/{libro.cliente.nombre}_{libro.mes}_{libro.ano}_contribuyente.xlsx", 
        engine='xlsxwriter')
    
    df_facturas = pd.DataFrame(facturas_limpias)

    workbook  = writer.book
    df = df_facturas
    if libro.mes == 1 : mes = "ENERO"
    elif libro.mes == 2 : mes = "FEBRERO"
    elif libro.mes == 3 : mes = "MARZO"
    elif libro.mes == 4 : mes = "ABRIL"
    elif libro.mes == 5 : mes = "MAYO"
    elif libro.mes == 6 : mes = "JUNIO"
    elif libro.mes == 7 : mes = "JULIO"
    elif libro.mes == 8 : mes = "AGOSTO"
    elif libro.mes == 9 : mes = "SEPTIEMBRE"
    elif libro.mes == 10 : mes = "OCTUBRE"
    elif libro.mes == 11 : mes = "NOVIEMBRE"
    elif libro.mes == 12 : mes = "DICIEMBRE"  
    bandera = 1
    #Si hay mas de 10 registros se creara una hoja por cada 20
    while len(df) >=15:
        df[:15].to_excel(writer,sheet_name=f"HOJA{bandera}",index=False,startrow=6,header=False)
        worksheet = writer.sheets[f"HOJA{bandera}"]
        #Configuracion de pagina
        worksheet.set_landscape()
        worksheet.set_paper(1)
        worksheet.set_margins(0.26,0.26,0.75,0.75)
        #formato de cabecera
        header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        "font_size":8, 
        })
        header_format.set_align("center")
        header_format.set_align("vcenter")
        #Ecritura de cabecera
        for col_num, value in enumerate(df_facturas.columns.values):
            worksheet.write(5, col_num, value, header_format)
        formato = workbook.add_format()
        formato.set_align("left")
        formato_data = workbook.add_format()
        formato_data.set_align("center")
        formato_data.set_bottom()
        formato_data.set_font_size(7)
        worksheet.set_column(0,0,4)
        worksheet.set_column(1,3,7)
        worksheet.set_column(4,4,15)
        worksheet.set_column(5,9,6)
        worksheet.set_column(10,14,5)
        worksheet.set_row(5,40)
        for row in range(6,21):
            worksheet.set_row(row,20,formato_data)
        #Excritura de formato de libro
        worksheet.merge_range('A1:I1',f'{libro.cliente.nombre}',formato)
        worksheet.merge_range('A2:I2',f'NIT: {libro.cliente.nit}',formato)
        worksheet.merge_range('A3:I3',f'NNUMERO DE REGISTRO: {libro.cliente.nRegistro}',formato)
        worksheet.merge_range('A4:I4',f'LIBRO DE VENTAS A CONTRIBUYENTE. MES DE {mes}/{libro.ano}',formato)
        worksheet.merge_range('A5:I5','EN DOLARES AMERICANOS',formato)
        bandera+=1
        df=df[15:]
    df.to_excel(writer,sheet_name=f"HOJA{bandera}",index=False,startrow=6,header=False)
    worksheet = writer.sheets[f"HOJA{bandera}"]
    #Configuracion de pagina
    worksheet.set_landscape()
    worksheet.set_paper(1)
    worksheet.set_margins(0.26,0.26,0.75,0.75)
    #formato de cabecera
    header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'border': 1,
    "font_size":8,
    })
    header_format.set_align("center")
    header_format.set_align("vcenter")
    #Ecritura de cabecera
    for col_num, value in enumerate(df_facturas.columns.values):
        worksheet.write(5, col_num, value, header_format)
    formato = workbook.add_format()
    formato.set_align("left")
    formato_data = workbook.add_format()
    formato_data.set_align("center")
    formato_data.set_bottom()
    formato_data.set_font_size(7)
    worksheet.set_column(0,0,4)
    worksheet.set_column(1,4,7)
    worksheet.set_column(5,5,15)
    worksheet.set_column(6,9,6)
    worksheet.set_column(10,14,6)
    worksheet.set_row(5,40)
    for row in range(6,len(df)+9):
        worksheet.set_row(row,20,formato_data)
    #Excritura de formato de libro
    worksheet.merge_range('A1:I1',f'{libro.cliente.nombre}',formato)
    worksheet.merge_range('A2:I2',f'NIT: {libro.cliente.nit}',formato)
    worksheet.merge_range('A3:I3',f'NUMERO DE REGISTRO: {libro.cliente.nRegistro}',formato)
    worksheet.merge_range('A4:I4',f'LIBRO DE VENTAS A CONTRIBUYENTES. MES DE {mes}/{libro.ano}',formato)
    worksheet.merge_range('A5:I5','EN DOLARES AMERICANOS',formato)
    total_venexe = round(facturas.aggregate(Sum('venExentas')).get("venExentas__sum"),2)
    total_vengra = round(facturas.aggregate(Sum('venGravadas')).get("venGravadas__sum"),2)
    total_ivadbt = round(facturas.aggregate(Sum('ivaDebFiscal')).get("ivaDebFiscal__sum"),2)
    total_vtsven = round(facturas.aggregate(Sum('vtVentas')).get("vtVentas__sum"),2)
    total_vtsiva = round(facturas.aggregate(Sum('vtIVA')).get("vtIVA__sum"),2)
    total_ivaret = round(facturas.aggregate(Sum('ivaRetenido')).get("ivaRetenido__sum"),2)
    total_ventas = round(facturas.aggregate(Sum('total')).get("total__sum"),2)
    total_vennsu = round(facturas.aggregate(Sum('ventasNSujetas')).get("ventasNSujetas__sum"),2)
    worksheet.merge_range(f'A{len(df)+7}:B{len(df)+7}','TOTALES',header_format)
    
    worksheet.write(len(df)+6,6,f"{total_venexe}")
    worksheet.write(len(df)+6,7,f"{total_vengra}")
    worksheet.write(len(df)+6,8,f"{total_vennsu}")
    worksheet.write(len(df)+6,9,f"{total_ivadbt}")
    worksheet.write(len(df)+6,10,f"{total_vtsven}")
    worksheet.write(len(df)+6,11,f"{total_vtsiva}")
    worksheet.write(len(df)+6,12,f"{total_ivaret}")
    worksheet.write(len(df)+6,13,f"{total_ventas}")
    ventas = FacturaContribuyente.objects.filter(libro=libro,venGravadas__gte=dec(0.00))
    ventas_t = round(ventas.aggregate(Sum('venGravadas')).get('venGravadas__sum'),2) 
    iva_ventas_t = round(ventas.aggregate(Sum('ivaDebFiscal')).get('ivaDebFiscal__sum'),2) 
    notas_credito = FacturaContribuyente.objects.filter(libro=libro,venGravadas__lt=dec(0.00))
    notas_credito_t = round(notas_credito.aggregate(Sum('venGravadas')).get('venGravadas__sum'),2) if len(notas_credito) > 0 else '0.00'
    iva_notas_credito_t = round(notas_credito.aggregate(Sum('ivaDebFiscal')).get('ivaDebFiscal__sum'),2) if len(notas_credito) > 0 else '0.00'
    ventas_positivas = round(ventas.aggregate(Sum('total')).get('total__sum'),2) 
    ventas_negativas = round(notas_credito.aggregate(Sum('total')).get('total__sum'),2) if len(notas_credito) > 0 else '0.00'
    worksheet.write(len(df)+7,7,f"{ventas_t}")
    worksheet.write(len(df)+7,9,f"{iva_ventas_t}")
    worksheet.write(len(df)+8,7,f"{notas_credito_t}")
    worksheet.write(len(df)+8,9,f"{iva_notas_credito_t}")
    worksheet.write(len(df)+7,13,f"{ventas_positivas}")
    worksheet.write(len(df)+8,13,f"{ventas_negativas}")
    worksheet.write(len(df)+7,5,"Total Ventas")
    worksheet.write(len(df)+8,5,"Total N/C")
    writer.save()
    return writer.book
