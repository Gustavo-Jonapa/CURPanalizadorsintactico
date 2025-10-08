import ply.yacc as yacc
from lexer import tokens
import re
from datetime import datetime

errores = []

def p_input(p):
    '''entrada : PALABRA PALABRA PALABRA FECHA SEXO ESTADO'''
    errores.clear()
    
    nombre = p[1]
    apellido1 = p[2]
    apellido2 = p[3]
    fecha = p[4]
    sexo = p[5]
    estado = p[6]

    validar_palabra(nombre, "Nombre", 1)
    validar_palabra(apellido1, "Primer apellido", 2)
    validar_palabra(apellido2, "Segundo apellido", 3)
    validar_fecha(fecha, 4)
    validar_sexo(sexo, 5)
    validar_estado(estado, 6)
    
    if not errores:
        p[0] = {
            "nombre": nombre,
            "apellido1": apellido1,
            "apellido2": apellido2,
            "fecha": fecha,
            "sexo": sexo,
            "estado": estado
        }
    else:
        p[0] = None

def validar_palabra(palabra, tipo, posicion):
    if not palabra:
        errores.append(f"{tipo} está vacío")
        return
    
    if not re.match(r'^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+$', palabra):
        errores.append(f"{tipo} '{palabra}' debe comenzar con mayúscula y contener solo letras")
    
    if len(palabra) < 2:
        errores.append(f"{tipo} '{palabra}' es demasiado corto (mínimo 2 caracteres)")

def validar_fecha(fecha, posicion):
    if not re.match(r'^\d{2}-\d{2}-\d{4}$', fecha):
        errores.append(f"Fecha '{fecha}' debe estar en formato AAAA-MM-DD")
        return
    
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        
        if fecha_obj > datetime.now():
            errores.append(f"Fecha '{fecha}' no puede ser futura")
        
        if fecha_obj.year < 1900:
            errores.append(f"Fecha '{fecha}' es anterior a 1900")
        
        edad = (datetime.now() - fecha_obj).days // 365
        if edad > 150:
            errores.append(f"Fecha '{fecha}' indica una edad mayor a 150 años")
            
    except ValueError:
        errores.append(f"Fecha '{fecha}' no es válida (ejemplo: 30 de febrero no existe)")

def validar_sexo(sexo, posicion):
    """Valida que el sexo sea H o M"""
    if sexo.upper() not in ['H', 'M']:
        errores.append(f"Sexo '{sexo}' inválido. Usa H (Hombre) o M (Mujer)")

def validar_estado(estado, posicion):
    """Valida que el estado sea una clave válida de RENAPO"""
    estados_validos = {
        "AS": "Aguascalientes", "BC": "Baja California", "BS": "Baja California Sur",
        "CC": "Campeche", "CL": "Coahuila", "CM": "Colima", "CS": "Chiapas",
        "CH": "Chihuahua", "DF": "Ciudad de México", "DG": "Durango",
        "GT": "Guanajuato", "GR": "Guerrero", "HG": "Hidalgo", "JC": "Jalisco",
        "MC": "México", "MN": "Michoacán", "MS": "Morelos", "NT": "Nayarit",
        "NL": "Nuevo León", "OC": "Oaxaca", "PL": "Puebla", "QT": "Querétaro",
        "QR": "Quintana Roo", "SP": "San Luis Potosí", "SL": "Sinaloa",
        "SR": "Sonora", "TC": "Tabasco", "TS": "Tamaulipas", "TL": "Tlaxcala",
        "VZ": "Veracruz", "YN": "Yucatán", "ZS": "Zacatecas", "NE": "Nacido en el Extranjero"
    }
    
    if estado.upper() not in estados_validos:
        errores.append(f"Estado '{estado}' no es válido. Debe ser una clave de estado válida (ej: CS, DF, NL)")

def p_error(p):
    if p:
        errores.append(f"Error de sintaxis: token inesperado '{p.value}' en posición {p.lexpos}")
    else:
        errores.append("Error de sintaxis: entrada incompleta o formato incorrecto")

parser = yacc.yacc()

def analizar(datos):
    """Función principal para analizar la entrada"""
    global errores
    errores = []
    
    if not datos or not datos.strip():
        errores.append("No se proporcionaron datos para analizar")
        return None, errores
    
    resultado = parser.parse(datos, lexer=__import__('lexer').lexer)
    return resultado, errores