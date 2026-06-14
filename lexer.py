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


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value in palabras_reservadas:
        t.type = palabras_reservadas[t.value]
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
