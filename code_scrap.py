#!/usr/bin/env python3

import requests as req
from bs4 import BeautifulSoup
import re

def busca_info(rango):
	# la información está contenida entre > y <. Lo que hace la función es localizar esos delimitadores y recuperar 
	# la info deseada. Hay dos casos: tres o dos columnas de información
	for i in range(rango):
					
		inicio= matches_positions[i]
		sublinea = str(linea)[matches_positions[i]+5:]
		
		inicio = sublinea.index(">")
		fin    = sublinea.index("<")
		
		if i == 0:
			a_0=sublinea[inicio+1:fin]
		elif i == 1: 
			a_1=sublinea[inicio+1:fin]
		elif i == 2: 
			a_2=sublinea[inicio+1:fin]
	
	if rango == 2: 
		a_2 = ""

	return a_0, a_1, a_2
	


resp = req.get("https://www.heubach-edelmetalle.de/preisuebersicht")

sopa=BeautifulSoup(resp.text, 'html.parser')
z=sopa.findAll(True, {'class':['even', 'odd']})

for linea in z:
	# buscamos las posiciones a partir de los cuales encontramos la etiqueta donde está contenido 
	# el dato que buscamos 
	str_linea = str(linea)
	matches = re.finditer('<td><a', str_linea)
	matches_positions = [match.start() for match in matches]

	

	if len(matches_positions) == 3:
		a_0,a_1,a_2= busca_info(3)
		print(a_0.ljust(70),a_1.ljust(20),a_2.ljust(20))

	if len(matches_positions) == 2:
		a_0,a_1,a_2= busca_info(2)
		print(a_0.ljust(70)," ".ljust(20),a_1.ljust(20))
		
	
		
		
