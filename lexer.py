import ply.lex as lex
import re

tokens = [
    'PALABRA', 'FECHA', 'SEXO', 'ESTADO'
]

t_ignore = ' \t'

def t_PALABRA(t):
    r'[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+'
    return t

def t_FECHA(t):
    r'\d{4}-\d{2}-\d{2}'
    patron = re.match(r'(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])', t.value)
    if not patron:
        print(f"Advertencia: Formato de fecha sospechoso: {t.value}")
    return t

def t_SEXO(t):
    r'[HhMm]'
    t.value = t.value.upper()
    return t

def t_ESTADO(t):
    r'[A-Z]{2}'
    estados_validos = {
        "AS", "BC", "BS", "CC", "CL", "CM", "CS", "CH", "DF", "DG",
        "GT", "GR", "HG", "JC", "MC", "MN", "MS", "NT", "NL", "OC",
        "PL", "QT", "QR", "SP", "SL", "SR", "TC", "TS", "TL", "VZ",
        "YN", "ZS", "NE"
    }
    if t.value not in estados_validos:
        print(f"Advertencia: Clave de estado no reconocida: {t.value}")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter no válido '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()