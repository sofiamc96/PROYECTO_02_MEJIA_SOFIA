# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 12:09:26 2021

@author: Sofia
"""
# Importación de la base de datos (archivo csv)
import csv

datos = []
with open("synergy_logistics_database.csv", "r") as archivo:
    lector = csv.DictReader(archivo)

    for registro in lector:
        datos.append(registro)

# Generación del listado de todas las rutas (origen, destino) 
# y ordenamiento por orden alfabético       
rutas = []
for dato in datos:
    ruta = [dato["origin"], dato["destination"]]
    if ruta not in rutas:
        rutas.append(ruta)
rutas.sort(key = lambda x: (x[0], x[1]))   

# print(rutas)


### Opción 1

# Función que contabiliza el número de veces que se utiliza
# una ruta, genera un listado de las rutas con sus respectivos 
# conteos, las ordena de mayor a menor y regresa un listado con
# las primeras 10. La variable que recibe es la dirección
def rutas_exp_imp (direccion):
    n = 0
    rutas_contabilizadas = []
    rutas_conteo = []
    rutas_10 = []
    
    for dato in datos:
        if dato["direction"] == direccion:
            ruta_actual = [dato["origin"], dato["destination"]]
            if ruta_actual not in rutas_contabilizadas:
                for ruta in datos:
                    if ruta_actual == [ruta["origin"], ruta["destination"]]:
                        n += 1
                
                rutas_contabilizadas.append(ruta_actual)
                rutas_conteo.append([dato["origin"], dato["destination"], n])    
                n = 0
    
    rutas_conteo.sort(reverse = True, key = lambda x:x[2])
    for i in range(10):
        rutas_10.append(rutas_conteo[i])        
    
    return rutas_10

# Generación de un listado de las 10 rutas más utilizadas para 
# exportaciones y uno de las 10 más utilizadas para importaciones
exportaciones_10 = rutas_exp_imp("Exports")
importaciones_10 = rutas_exp_imp("Imports")

# Generación de un listado ordenado que contiene las 20 rutas 
# tomadas de los dos listados generados anteriormente 
rutas_20 = []
for ruta in exportaciones_10:
    rutas_20.append(ruta)
for ruta in importaciones_10:
    rutas_20.append(ruta)
rutas_20.sort(reverse = True, key = lambda x:x[2])

# Generación de un listado que contenga las 10 rutas más demandadas
# con sus respectivos conteos, a partir del listado previo
rutas_mas_demandadas_cont = []
n = 0
i = 0
while n < 10:
    if rutas_20[i] not in rutas_mas_demandadas_cont:
        rutas_mas_demandadas_cont.append(rutas_20[i])
        n += 1
    i += 1

# print(rutas_mas_demandadas_cont)

# Se calcula el porcentaje del valor total de las exportaciones
# e importaciones generado por las 10 rutas más demandadas
sumas = 0
for ruta in rutas_mas_demandadas_cont:
    sumas += ruta[2]
porcentaje_mov_rutas_mas_demandadas = round((sumas/len(datos))*100, 2)

# print(len(datos))
# print(porcentaje_mov_rutas_mas_demandadas)

### Opción 2

# Función que calcula el valor total generado por un medio de 
# transporte. Recibe el nombre del medio de transporte y regresa
# una lista con el nombre del medio, el número de movimientos que 
# se realizan mediante él y el valor total que genera
def transporte_valor (medio):
    n = 0
    valor = 0
            
    for dato in datos:
        if dato["transport_mode"] == medio:
           n += 1
           valor += int(dato["total_value"])
                
           medio_conteo = [dato["transport_mode"], n, valor]
           
    return medio_conteo

# Generación de un listado ordenado que incluye la información
# dada por la función previa para todos los medios de transporte
medios_cont_valores = [transporte_valor("Sea"),transporte_valor("Air"),
                             transporte_valor("Rail"),transporte_valor("Road")]
medios_cont_valores.sort(reverse = True, key = lambda x:x[2])

# print(medios_cont_valores)


### Opción 3

# Función que recibe una lista de rutas y calcula los valores generados 
# por cada una de las rutas y regresa un listado que contiene las rutas 
# con sus respectivos valores totales
def rutas_valores (lista_rutas):
    ruta_valor = []
    valor_tot = 0
        
    for ruta in lista_rutas:    
        for dato in datos: 
            if [dato["origin"], dato["destination"]] == ruta:
                valor_tot += int(dato["total_value"])
                    
        ruta_valor.append([ruta[0], ruta[1], valor_tot])
        valor_tot = 0
    
    return ruta_valor

# Se guarda y se ordena la lista generada mediante la función anterior
valores_rutas = (rutas_valores(rutas))
valores_rutas.sort(reverse = True, key = lambda x:x[2])

# print(valores_rutas)

# Función que recibe una dirección (origen o destino) y un porcentaje.
# Con los datos recibidos se devuelven los países (tomados de la lista
# generada con la función previa) que generan dicho porcentaje con su 
# respectivo valor, porcentaje y el porcentaje acumulado
def porcentaje_valor_paises (direccion_pais, porcentaje, lista_paises = valores_rutas):
    valor_total = 0
    porcentaje_acum = 0
    paises_valores_ord = []
    paises_porcentajes_ord = []
    paises_porcentajes = []
    paises_contabilizados = []
    
    for valor in valores_rutas:
        valor_total += valor[2]
    
    if direccion_pais == 'origen':
        i = 0
    elif direccion_pais == 'destino':
        i = 1
            
    for pais in lista_paises:
        if pais[i] not in paises_contabilizados:
            pais_actual = pais[i]
            valor_actual = pais[2]
            for ruta in valores_rutas:
                if i == 0:
                    if ruta[i] == pais_actual and ruta[i+1] != pais[i+1]:
                        valor_actual += ruta[2]
                elif i == 1:
                    if ruta[i] == pais_actual and ruta[i-1] != pais[i-1]:
                        valor_actual += ruta[2]
            paises_valores_ord.append([pais_actual, valor_actual])
            paises_contabilizados.append(pais_actual)
    paises_valores_ord.sort(reverse = True, key = lambda x:x[1])
    
    for pais in paises_valores_ord:
        valor_actual = pais[1]
        porcentaje_actual = round(valor_actual/valor_total*100, 2)
        porcentaje_acum += porcentaje_actual
        paises_porcentajes_ord.append([pais[0], valor_actual, porcentaje_actual, round(porcentaje_acum, 2)])
       
    for pais in paises_porcentajes_ord:
            if pais[3] < porcentaje + 2.5:
                paises_porcentajes.append(pais)
                                     
    return paises_porcentajes

# Generación de los listados de países origen y destino que generan
# aproximadamente el 80% del valor total
porcentaje_valor_paises_exp = porcentaje_valor_paises('origen', 80)
porcentaje_valor_paises_imp = porcentaje_valor_paises('destino', 80)

# print(porcentaje_valor_paises_exp)
# print(porcentaje_valor_paises_imp)

#####################

# Se presentan los resultados obtenidos previamente
print('\n\nA continuación se presenta el análisis de las 3 opciones de enfoque solicitadas por la Dirección de Synergy Logistics: ')

print('\n\nOPCIÓN 1 - 10 rutas con mayor flujo de importaciones y exportaciones: ')
print('\n  País origen\t\t\tPaís destino\t\tNúmero de movimientos\n  -----------\t\t\t------------\t\t---------------------')
i = 1
for ruta in rutas_mas_demandadas_cont:
    if len(ruta[0]) < 5:
        print('\n' + str(i) + '.\t' + ruta[0] + '\t\t\t\t\t   ' + ruta[1] + '\t\t\t   ' + str(ruta[2]))
        i += 1
    elif len(ruta[0]) < 8:
        print('\n' + str(i) + '.\t' + ruta[0] + '\t\t\t\t   ' + ruta[1] + '\t\t\t\t   ' + str(ruta[2]))
        i += 1
    else:
        print('\n' + str(i) + '.\t' + ruta[0] + '\t\t\t   ' + ruta[1] + '\t\t\t\t   ' + str(ruta[2]))
        i += 1
print('\nPorcentaje que representan estas 10 rutas del total de movimientos realizados en todas las rutas:\t' + str(porcentaje_mov_rutas_mas_demandadas) + '%')
        
print('\n\n\nOPCIÓN 2 - Medios de transporte por orden de importancia de acuerdo al valor total de las importaciones y exportaciones: ')
print('\n  Medio de transporte\t\t\tValor total de importaciones y exportaciones\n  -------------------\t\t\t--------------------------------------------')
i = 1
for medio in medios_cont_valores:
    if len(medio[0]) < 4:
        print('\n' + str(i) + '.\t' + medio[0] + '\t\t\t\t\t\t\t\t\t' + str(medio[2]))   
        i += 1
    else:
        print('\n' + str(i) + '.\t' + medio[0] + '\t\t\t\t\t\t\t\t' + str(medio[2]))   
        i += 1

print('\n\n\nOPCIÓN 3 - Países que generan aproximadamente el 80% del valor total de las importaciones y exportaciones: ')
print('\n\t\t\t\tEXPORTACIONES\n\t\t\t\t-------------')
print('\n\tPaís\t\t\t   Valor\t\tPorcentaje\n\t----\t\t\t   -----\t\t----------')
i = 1
for pais_exp in porcentaje_valor_paises_exp:
    if len(pais_exp[0]) < 5:
        print('\n' + str(i) + '.\t' + pais_exp[0] + '\t\t\t\t' + str(pais_exp[1]) + '\t\t  ' + str(pais_exp[2]) + '%')
        i += 1
    elif len(pais_exp[0]) < 8:
        print('\n' + str(i) + '.\t' + pais_exp[0] + '\t\t\t' + str(pais_exp[1]) + '\t\t  ' + str(pais_exp[2]) + '%')
        i += 1
    else:
        print('\n' + str(i) + '.\t' + pais_exp[0] + '\t\t' + str(pais_exp[1]) + '\t\t  ' + str(pais_exp[2]) + '%')
        i += 1
print('\nPORCENTAJE TOTAL:\t\t\t\t\t  ' + str(porcentaje_valor_paises_exp[-1][3]) + '%')
print('\n\n\t\t\t\tIMPORTACIONES\n\t\t\t\t-------------')
print('\n\tPaís\t\t\t\t\t   Valor\t\tPorcentaje\n\t----\t\t\t\t\t   -----\t\t----------')
i = 1
for pais_imp in porcentaje_valor_paises_imp:
    if len(pais_imp[0]) < 5:
        print('\n' + str(i) + '.\t' + pais_imp[0] + '\t\t\t\t\t\t' + str(pais_imp[1]) + '\t\t  ' + str(pais_imp[2]) + '%')
        i += 1
    elif len(pais_imp[0]) < 8:
        print('\n' + str(i) + '.\t' + pais_imp[0] + '\t\t\t\t\t' + str(pais_imp[1]) + '\t\t  ' + str(pais_imp[2]) + '%')
        i += 1
    elif len(pais_imp[0]) < 12:
        print('\n' + str(i) + '.\t' + pais_imp[0] + '\t\t\t\t' + str(pais_imp[1]) + '\t\t  ' + str(pais_imp[2]) + '%')
        i += 1
    elif len(pais_imp[0]) < 15:
        print('\n' + str(i) + '.\t' + pais_imp[0] + '\t\t\t' + str(pais_imp[1]) + '\t\t  ' + str(pais_imp[2]) + '%')
        i += 1
    else:
        print('\n' + str(i) + '.\t' + pais_imp[0] + '\t' + str(pais_imp[1]) + '\t\t  ' + str(pais_imp[2]) + '%')
        i += 1
print('\nPORCENTAJE TOTAL:\t\t\t\t\t\t\t  ' + str(porcentaje_valor_paises_imp[-1][3]) + '%')
