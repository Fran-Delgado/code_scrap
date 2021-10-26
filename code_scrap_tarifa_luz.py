#!/usr/bin/env python3

import requests as req
from bs4 import BeautifulSoup
import re
import datetime
import calendar

fecha = datetime.datetime.now()
hoy = str(fecha.year)+"/"+str(fecha.month)+"/"+str(fecha.day)

def recuperar_sopa(web):
    resp = req.get(web)
    sopa=BeautifulSoup(resp.text, 'html.parser')
    return sopa

def filtrar_sopa(sopa,clase_html,palabra):
    muestra = sopa.findAll(True, {'class':[clase_html]})
    str_muestra = str(muestra)
    matches = re.finditer(palabra, str_muestra)
    matches_positions = [match.start() for match in matches]
    return matches_positions,str(muestra)

def busca_categorias(empieza,acaba):
    categorias=[]
    for i in range(len(matches_positions)):
        inicio= matches_positions[i]
        sublinea = str_muestra[matches_positions[i]+5:]
        inicio = sublinea.index(empieza)
        fin    = sublinea.index(acaba)
        categorias.append(sublinea[inicio+1:fin-1])
    return categorias


year = 2021
month = int(input("¿Para que mes quieres extraer datos (uno de los últimos 5 meses)? "))
num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]


direcciones=[]
fechas=[]
for fecha in days:
    año_editado = fecha.strftime('%Y')
    mes_editado = fecha.strftime('%m')
    dia_editado = fecha.strftime('%d')
    fecha_editada =  dia_editado+'%2F'+mes_editado+'%2F'+año_editado
    fecha_dato = año_editado+'-'+mes_editado+'-'+dia_editado
    webs = "https://tarifaluzhora.es/?tarifa=pcb&fecha="+fecha_editada
    direcciones.append(webs)
    fechas.append(fecha_dato)

print("Datos de coste de la luz:")

for direccion in direcciones:
    
    base =direccion
    
    sopa = recuperar_sopa(base)
    matches_positions,str_muestra = filtrar_sopa(sopa,'col-xs-9','style="color: #333;')
    horas=busca_categorias('>','<')

    sopa = recuperar_sopa(base)
    matches_positions,str_muestra = filtrar_sopa(sopa,'col-xs-9','span itemprop="price"')
    precio=busca_categorias('>','<')

    result = zip(horas,precio)
    for s in list(result):
        with open ('datos.txt','a') as fichero_texto:
            print(fechas[direcciones.index(direccion)],*s) 
    
