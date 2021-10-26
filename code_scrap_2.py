#!/usr/bin/env python3

import requests as req
from bs4 import BeautifulSoup
import re
import time

base = "https://www.heubach-edelmetalle.de"

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
        categorias.append(base+sublinea[inicio:fin-2])
    return categorias

sopa = recuperar_sopa(base)
matches_positions,str_muestra = filtrar_sopa(sopa,'btn btn-light text-primary font-weight-bold','href="')

# Obtención de paths relativos de los catálogos.
print (" Paths relativos de los catálogos de nivel 1: \n")

catalogo = []
for i in range(len(matches_positions)):
    inicio= matches_positions[i]
    sublinea = str_muestra[matches_positions[i]+5:]
    inicio = sublinea.index('"')
    fin    = sublinea.index('>')
    web_de_catalogo = base + sublinea[inicio+1:fin-1]
    catalogo.append(web_de_catalogo)

for contador,elemento in enumerate(catalogo):
    print(contador,elemento)

# Nos centraremos por ahora en las categorías 1,2 y 4
# print("Monedas de oro :\n")
# sopa = recuperar_sopa(catalogo[1])
# matches_positions,str_muestra = filtrar_sopa(sopa,'mt-xs-2','href="')
# categ_mone_oro=busca_categorias('/katalog','title')
# for elemento in categ_mone_oro: print(elemento)

# print("Lingotes de oro :\n")
# sopa = recuperar_sopa(catalogo[2])
# matches_positions,str_muestra = filtrar_sopa(sopa,'mt-xs-2','href="')
# categ_lingo_oro=busca_categorias('/katalog','title')
# for elemento in categ_lingo_oro: print(elemento)

print("Monedas de plata :\n")
sopa = recuperar_sopa(catalogo[4])
matches_positions,str_muestra = filtrar_sopa(sopa,'mt-xs-2','href="')
categ_mone_plata=busca_categorias('/katalog','title')
for elemento in categ_mone_plata: print(elemento)
print(categ_mone_plata)

for web in categ_mone_plata:
    sopa=recuperar_sopa(web)
    matches_positions,str_muestra = filtrar_sopa(sopa,'mt-xs-2','href="')
    categ_mone_plata=busca_categorias('/katalog','title')
    for elemento in categ_mone_plata: print(elemento)
    time.sleep(10)