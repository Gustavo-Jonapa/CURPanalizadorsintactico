import re
from unicodedata import normalize

PALABRAS_INCONVENIENTES = {
    'BACA', 'BAKA', 'BUEI', 'BUEY', 'CACA', 'CACO', 'CAGA', 'CAGO',
    'CAKA', 'CAKO', 'COGE', 'COGI', 'COJA', 'COJE', 'COJI', 'COJO',
    'COLA', 'CULO', 'FALO', 'FETO', 'GETA', 'GUEI', 'GUEY', 'JETA',
    'JOTO', 'KACA', 'KACO', 'KAGA', 'KAGO', 'KAKA', 'KAKO', 'KOGE',
    'KOGI', 'KOJA', 'KOJE', 'KOJI', 'KOJO', 'KOLA', 'KULO', 'LILO',
    'LOCA', 'LOCO', 'LOKA', 'LOKO', 'MAME', 'MAMO', 'MEAR', 'MEAS',
    'MEON', 'MIAR', 'MION', 'MOCO', 'MOKO', 'MULA', 'MULO', 'NACA',
    'NACO', 'PEDA', 'PEDO', 'PENE', 'PIPI', 'PITO', 'POPO', 'PUTA',
    'PUTO', 'QULO', 'RATA', 'ROBA', 'ROBE', 'ROBO', 'RUIN', 'SENO',
    'TETA', 'VACA', 'VAGA', 'VAGO', 'VAKA', 'VUEI', 'VUEY', 'WUEI', 'WUEY'
}
PREPOSICIONES = {'DE', 'DEL', 'LA', 'LOS', 'LAS', 'MC', 'MAC', 'VON', 'VAN'}

def limpiar_texto(texto):
    texto_sin_acentos = normalize('NFD', texto)
    texto_sin_acentos = ''.join(c for c in texto_sin_acentos if not normalize('NFD', c).startswith('\u0301'))
    return texto_sin_acentos.upper()

def obtener_primera_vocal_interna(palabra):
    palabra_limpia = limpiar_texto(palabra)
    for char in palabra_limpia[1:]:
        if char in 'AEIOU':
            return char
    return 'X'

def obtener_primera_consonante_interna(palabra):
    palabra_limpia = limpiar_texto(palabra)
    for char in palabra_limpia[1:]:
        if char.isalpha() and char not in 'AEIOU':
            return char
    return 'X'

def procesar_apellido(apellido):
    partes = apellido.upper().split()
    partes_validas = [p for p in partes if p not in PREPOSICIONES]
    return partes_validas[0] if partes_validas else apellido.upper()

def calcular_digito_verificador(curp_base):
    valores = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    suma = 0
    
    for i, char in enumerate(curp_base):
        valor = valores.index(char) if char in valores else 0
        suma += valor * (18 - i)
    
    digito = 10 - (suma % 10)
    return '0' if digito == 10 else str(digito)

def generar_curp(nombre, apellido1, apellido2, fecha, sexo, estado):
    nombre_limpio = limpiar_texto(nombre)
    ap1_limpio = limpiar_texto(procesar_apellido(apellido1))
    ap2_limpio = limpiar_texto(procesar_apellido(apellido2))
    
    año, mes, dia = fecha.split('-')
    
    primera_letra_ap1 = ap1_limpio[0]
    primera_vocal_ap1 = obtener_primera_vocal_interna(apellido1)
    primera_letra_ap2 = ap2_limpio[0]
    primera_letra_nombre = nombre_limpio[0]
    
    cuatro_letras = primera_letra_ap1 + primera_vocal_ap1 + primera_letra_ap2 + primera_letra_nombre
    
    if cuatro_letras in PALABRAS_INCONVENIENTES:

        cuatro_letras = cuatro_letras[0] + 'X' + cuatro_letras[2:]
    
    curp_base = (
        cuatro_letras +
        año[-2:] + mes + dia +
        sexo.upper() +
        estado.upper() +
        obtener_primera_consonante_interna(apellido1) +
        obtener_primera_consonante_interna(apellido2) +
        obtener_primera_consonante_interna(nombre) +
        ('A' if int(año) >= 2000 else '0')
    )
    digito = calcular_digito_verificador(curp_base)
    
    return curp_base + digito

def formatear_curp(curp):
    if len(curp) != 18:
        return curp
    return f"{curp[:4]} {curp[4:10]} {curp[10:16]} {curp[16:]}"