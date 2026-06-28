errores_semanticos = []


class Ambito:
    def __init__(self, padre=None):
        self.simbolos = {}
        self.padre = padre

    def declarar(self, nombre, info):
        if nombre in self.simbolos:
            return False
        self.simbolos[nombre] = info
        return True

    def buscar(self, nombre):
        amb = self
        while amb is not None:
            if nombre in amb.simbolos:
                return amb.simbolos[nombre]
            amb = amb.padre
        return None


def _error(mensaje):
    errores_semanticos.append({"mensaje": mensaje})


def _tipo_literal(valor):
    if isinstance(valor, bool):
        return "Boolean"
    if isinstance(valor, int):
        return "Int"
    if isinstance(valor, float):
        return "Double"
    if isinstance(valor, str):
        if valor in ("true", "false"):
            return "Boolean"
        return "String"
    return None


def inferir_tipo(nodo, ambito):
    if nodo is None:
        return None
    etiqueta = nodo[0]
    if etiqueta == "literal":
        return _tipo_literal(nodo[1])
    if etiqueta == "id":
        info = ambito.buscar(nodo[1])
        if info:
            return info["tipo"]
        return None
    if etiqueta == "op":
        if nodo[1] in ("&&", "||"):
            return "Boolean"
        ti = inferir_tipo(nodo[2], ambito)
        td = inferir_tipo(nodo[3], ambito)
        if ti == "Double" or td == "Double":
            return "Double"
        return "Int"
    if etiqueta in ("comp", "not"):
        return "Boolean"
    if etiqueta == "list":
        return "List"
    if etiqueta == "array":
        return "Array"
    if etiqueta == "map":
        return "Map"
    if etiqueta == "readln":
        return "String"
    if etiqueta == "llamada":
        info = ambito.buscar(nodo[1])
        if info:
            return info["tipo"]
        return None
    return None


# Integrante 1 - Reglas semanticas: (1) uso de variable/identificador no
# declarado, (2) redeclaracion de un nombre en el mismo ambito.
def regla_variable_no_declarada(nombre, ambito):
    if ambito.buscar(nombre) is None:
        _error(f'Variable o identificador "{nombre}" usado sin declarar.')
        return False
    return True


def regla_redeclaracion(nombre, ambito):
    if nombre in ambito.simbolos:
        _error(f'"{nombre}" ya fue declarado en este ambito (redeclaracion).')
        return False
    return True


def recorrer_expr(nodo, ambito):
    if nodo is None:
        return
    etiqueta = nodo[0]
    if etiqueta == "id":
        regla_variable_no_declarada(nodo[1], ambito)
    elif etiqueta in ("op", "comp"):
        recorrer_expr(nodo[2], ambito)
        recorrer_expr(nodo[3], ambito)
    elif etiqueta == "not":
        recorrer_expr(nodo[1], ambito)
    elif etiqueta == "llamada":
        for arg in nodo[2]:
            recorrer_expr(arg, ambito)
    elif etiqueta in ("list", "array"):
        for arg in nodo[1]:
            recorrer_expr(arg, ambito)
    elif etiqueta == "map":
        for clave, valor in nodo[1]:
            recorrer_expr(clave, ambito)
            recorrer_expr(valor, ambito)


def recorrer(sentencias, ambito):
    for sentencia in sentencias:
        recorrer_sentencia(sentencia, ambito)


def recorrer_sentencia(nodo, ambito):
    etiqueta = nodo[0]
    if etiqueta == "declaracion":
        _, clase, nombre, tipo_declarado, expr = nodo
        regla_redeclaracion(nombre, ambito)
        recorrer_expr(expr, ambito)
        tipo_expr = inferir_tipo(expr, ambito)
        ambito.declarar(nombre, {"clase": clase, "tipo": tipo_declarado or tipo_expr})
    elif etiqueta == "asignacion":
        _, nombre, expr = nodo
        regla_variable_no_declarada(nombre, ambito)
        recorrer_expr(expr, ambito)
    elif etiqueta == "impresion":
        for arg in nodo[2]:
            recorrer_expr(arg, ambito)
    elif etiqueta == "llamada":
        for arg in nodo[2]:
            recorrer_expr(arg, ambito)
    elif etiqueta == "return":
        recorrer_expr(nodo[1], ambito)
    elif etiqueta in ("if", "if-else"):
        recorrer_expr(nodo[1], ambito)
        recorrer(nodo[2][1], Ambito(ambito))
        if etiqueta == "if-else":
            recorrer(nodo[3][1], Ambito(ambito))
    elif etiqueta == "while":
        recorrer_expr(nodo[1], ambito)
        recorrer(nodo[2][1], Ambito(ambito))
    elif etiqueta in ("funcion", "funcion-expr"):
        _, _nombre, params, _tipo_ret, cuerpo = nodo
        amb_fn = Ambito(ambito)
        for pnombre, ptipo in params:
            amb_fn.declarar(pnombre, {"clase": "param", "tipo": ptipo})
        if etiqueta == "funcion":
            recorrer(cuerpo[1], amb_fn)
        else:
            recorrer_expr(cuerpo, amb_fn)


def registrar_funciones(sentencias, ambito):
    for s in sentencias:
        if s[0] in ("funcion", "funcion-expr"):
            if not ambito.declarar(s[1], {"clase": "fun", "tipo": s[3]}):
                _error(f'La funcion "{s[1]}" ya fue declarada.')


def analizar_semantico(ast):
    errores_semanticos.clear()
    if ast is None or ast[0] != "programa":
        return True, []
    global_amb = Ambito()
    registrar_funciones(ast[1], global_amb)
    recorrer(ast[1], global_amb)
    return len(errores_semanticos) == 0, list(errores_semanticos)
