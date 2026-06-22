import ply.yacc as yacc

import lexer as lexer_mod
from lexer import tokens  # noqa: F401

errores_sintacticos = []

precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("nonassoc", "IGUAL", "DIFERENTE", "MAYOR", "MENOR", "MAYOR_IGUAL", "MENOR_IGUAL"),
    ("left", "MAS", "MENOS"),
    ("left", "POR", "DIV"),
    ("right", "NOT"),
)


def p_programa(p):
    "programa : lista_sentencias"
    p[0] = ("programa", p[1])

def p_lista_sentencias(p):
    "lista_sentencias : lista_sentencias sentencia"
    p[0] = p[1] + [p[2]]

def p_lista_sentencias_vacia(p):
    "lista_sentencias : empty"
    p[0] = []

def p_sentencia(p):
    """sentencia : declaracion
                 | asignacion
                 | impresion
                 | lectura
                 | estructura_if
                 | estructura_while
                 | declaracion_funcion
                 | llamada_funcion
                 | retorno"""
    p[0] = p[1]

def p_bloque(p):
    "bloque : LLAVE_IZQ lista_sentencias LLAVE_DER"
    p[0] = ("bloque", p[2])

def p_empty(p):
    "empty :"
    p[0] = None

def p_expresion_aritmetica(p):
    """expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIV expresion"""
    p[0] = ("op", p[2], p[1], p[3])

def p_expresion_agrupada(p):
    "expresion : PAR_IZQ expresion PAR_DER"
    p[0] = p[2]

def p_expresion_id(p):
    "expresion : ID"
    p[0] = ("id", p[1])

def p_expresion_literal(p):
    """expresion : ENTERO
                 | FLOTANTE
                 | CADENA
                 | BOOLEANO"""
    p[0] = ("literal", p[1])

def p_expresion_llamada(p):
    "expresion : llamada_funcion"
    p[0] = p[1]

def p_expresion_estructura(p):
    "expresion : estructura_datos"
    p[0] = p[1]

def p_llamada_funcion(p):
    "llamada_funcion : ID PAR_IZQ argumentos PAR_DER"
    p[0] = ("llamada", p[1], p[3])

def p_argumentos(p):
    """argumentos : lista_argumentos
                  | empty"""
    p[0] = p[1] if p[1] else []

def p_lista_argumentos(p):
    "lista_argumentos : lista_argumentos COMA expresion"
    p[0] = p[1] + [p[3]]

def p_lista_argumentos_uno(p):
    "lista_argumentos : expresion"
    p[0] = [p[1]]

def p_impresion(p):
    """impresion : PRINT PAR_IZQ argumentos PAR_DER
                 | PRINTLN PAR_IZQ argumentos PAR_DER"""
    p[0] = ("impresion", p[1], p[3])

def p_estructura_datos_list(p):
    "estructura_datos : LISTOF PAR_IZQ argumentos PAR_DER"
    p[0] = ("list", p[3])

def p_if(p):
    "estructura_if : IF PAR_IZQ expresion PAR_DER bloque"
    p[0] = ("if", p[3], p[5])

def p_funcion_sin_retorno(p):
    "declaracion_funcion : FUN ID PAR_IZQ parametros PAR_DER bloque"
    p[0] = ("funcion", p[2], p[4], None, p[6])

def p_parametros(p):
    """parametros : lista_parametros
                  | empty"""
    p[0] = p[1] if p[1] else []

def p_lista_parametros(p):
    "lista_parametros : lista_parametros COMA parametro"
    p[0] = p[1] + [p[3]]

def p_lista_parametros_uno(p):
    "lista_parametros : parametro"
    p[0] = [p[1]]

def p_parametro(p):
    "parametro : ID DOS_PUNTOS TIPO"
    p[0] = (p[1], p[3])


SUGERENCIAS = {
    "PAR_DER": "Revisa los parentesis: falta abrir o cerrar uno.",
    "LLAVE_DER": "Revisa las llaves: falta abrir o cerrar un bloque.",
    "ASIGNAR": 'Para comparar usa "==", para asignar usa "=".',
    "TIPO": 'Despues de ":" debe ir un tipo (Int, Double, String, Boolean...).',
}

def p_error(p):
    if p:
        errores_sintacticos.append({
            "token": p.value, "tipo": p.type, "linea": p.lineno,
            "sugerencia": SUGERENCIAS.get(p.type, "Verifica la estructura de la sentencia."),
        })
    else:
        errores_sintacticos.append({
            "token": "EOF", "tipo": "FIN_DE_ARCHIVO", "linea": "-",
            "sugerencia": "Codigo incompleto: falta cerrar un bloque, parentesis o expresion.",
        })

def construir_parser(**kwargs):
    return yacc.yacc(**kwargs)

def analizar_sintactico(texto):
    errores_sintacticos.clear()
    lx = lexer_mod.construir_lexer()
    parser = construir_parser()
    arbol = parser.parse(texto, lexer=lx)
    return len(errores_sintacticos) == 0, arbol, list(errores_sintacticos)
