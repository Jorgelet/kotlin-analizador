# import ply.lex as lex

palabras_reservadas = {
    "fun": "FUN",
    "val": "VAL",
    "var": "VAR",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "print": "PRINT",
    "println": "PRINTLN",
    "readln": "READLN",
    "return": "RETURN",
}

tokens_integrante1 = ["ID"] + list(palabras_reservadas.values())

t_ignore = " \t\r"

tipos_datos = {"Int", "Double", "String", "Boolean", "Array", "List", "Map"}

literales_booleanos = {"true", "false"}

tokens_integrante2 = ["ENTERO", "FLOTANTE", "CADENA", "BOOLEANO", "TIPO"]


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value in palabras_reservadas:
        t.type = palabras_reservadas[t.value]
    elif t.value in tipos_datos:
        t.type = "TIPO"
    elif t.value in literales_booleanos:
        t.type = "BOOLEANO"
    return t


def t_COMENTARIO_LINEA(t):
    r"//[^\n]*"
    pass


def t_COMENTARIO_BLOQUE(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")
    pass


# Salto de línea: mantiene actualizado el número de línea.
def t_salto_linea(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_FLOTANTE(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_ENTERO(t):
    r"\d+"
    t.value = int(t.value)
    return t


# Cadena de texto (String) entre comillas dobles, admite escapes (\" \\ ...).
def t_CADENA(t):
    r'"([^"\\\n]|\\.)*"'
    return t
