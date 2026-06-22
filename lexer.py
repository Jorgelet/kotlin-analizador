import ply.lex as lex

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

estructuras_datos = {"listOf": "LISTOF", "arrayOf": "ARRAYOF", "mapOf": "MAPOF", "to": "TO"}
tokens_avance2 = ["LISTOF", "ARRAYOF", "MAPOF", "TO"]

tokens_integrante2 = ["ENTERO", "FLOTANTE", "CADENA", "BOOLEANO", "TIPO"]

tokens_integrante3 = [
    # Aritméticos
    "MAS",
    "MENOS",
    "POR",
    "DIV",
    # Lógicos
    "AND",
    "OR",
    "NOT",
    # Asignación
    "ASIGNAR",
    # Comparación
    "IGUAL",
    "MAYOR",
    "MENOR",
    "MAYOR_IGUAL",
    "MENOR_IGUAL",
    "DIFERENTE",
    # Delimitadores y separadores
    "PAR_IZQ",
    "PAR_DER",
    "LLAVE_IZQ",
    "LLAVE_DER",
    "COMA",
    "DOS_PUNTOS",
]


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value in palabras_reservadas:
        t.type = palabras_reservadas[t.value]
    elif t.value in tipos_datos:
        t.type = "TIPO"
    elif t.value in literales_booleanos:
        t.type = "BOOLEANO"
    elif t.value in estructuras_datos:
        t.type = estructuras_datos[t.value]
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


# Aritméticos
t_MAS = r"\+"
t_MENOS = r"-"
t_POR = r"\*"
t_DIV = r"/"

# Lógicos
t_AND = r"&&"
t_OR = r"\|\|"
t_NOT = r"!"

# Asignación
t_ASIGNAR = r"="

t_IGUAL = r"=="
t_DIFERENTE = r"!="
t_MAYOR_IGUAL = r">="
t_MENOR_IGUAL = r"<="
t_MAYOR = r">"
t_MENOR = r"<"

# Delimitadores y separadores
t_PAR_IZQ = r"\("
t_PAR_DER = r"\)"
t_LLAVE_IZQ = r"\{"
t_LLAVE_DER = r"\}"
t_COMA = r","
t_DOS_PUNTOS = r":"

tokens = tokens_integrante1 + tokens_integrante2 + tokens_integrante3 + tokens_avance2

errores_lexicos = []


def t_error(t):
    """Se invoca cuando ningún patrón casa con el carácter actual."""
    errores_lexicos.append(
        {
            "caracter": t.value[0],
            "linea": t.lineno,
            "posicion": t.lexpos,
        }
    )
    t.lexer.skip(1)


def construir_lexer(**kwargs):
    """Crea una instancia nueva del lexer y limpia los errores previos."""
    errores_lexicos.clear()
    return lex.lex(**kwargs)