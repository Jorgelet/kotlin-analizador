import argparse
import datetime
import os

import lexer as analizador

CARPETA_LOGS = "logs"


def calcular_columna(texto, posicion):
    """Devuelve la columna (1-indexada) de un carácter dado su lexpos."""
    ultimo_salto = texto.rfind("\n", 0, posicion)
    return posicion - ultimo_salto


def analizar_codigo(texto):
    """Tokeniza el texto y devuelve (lista_de_tokens, lista_de_errores)."""
    lx = analizador.construir_lexer()
    lx.input(texto)

    tokens = []
    while True:
        tok = lx.token()
        if tok is None:
            break
        tokens.append(
            {
                "tipo": tok.type,
                "valor": tok.value,
                "linea": tok.lineno,
                "columna": calcular_columna(texto, tok.lexpos),
            }
        )

    # Los errores se acumulan en el módulo durante el análisis.
    errores = []
    for err in analizador.errores_lexicos:
        errores.append(
            {
                "caracter": err["caracter"],
                "linea": err["linea"],
                "columna": calcular_columna(texto, err["posicion"]),
            }
        )

    return tokens, errores


def construir_reporte(ruta_archivo, autor, tokens, errores):
    """Arma el texto del log/reporte."""
    ahora = datetime.datetime.now()
    lineas = []
    lineas.append("=" * 64)
    lineas.append(" ANALIZADOR LÉXICO - SUBCONJUNTO DE KOTLIN")
    lineas.append("=" * 64)
    lineas.append(f"Archivo analizado : {ruta_archivo}")
    lineas.append(f"Analizado por     : {autor}")
    lineas.append(f"Fecha y hora      : {ahora.strftime('%d-%m-%Y %H:%M:%S')}")
    lineas.append(f"Tokens reconocidos: {len(tokens)}")
    lineas.append(f"Errores léxicos   : {len(errores)}")
    lineas.append("")

    # Tabla de tokens.
    lineas.append("-" * 64)
    lineas.append(" TOKENS RECONOCIDOS")
    lineas.append("-" * 64)
    lineas.append(f"{'#':>4}  {'TIPO':<14} {'LEXEMA':<22} {'LÍNEA':>6} {'COL':>5}")
    for i, tok in enumerate(tokens, start=1):
        valor = str(tok["valor"])
        if len(valor) > 22:
            valor = valor[:19] + "..."
        lineas.append(
            f"{i:>4}  {tok['tipo']:<14} {valor:<22} {tok['linea']:>6} {tok['columna']:>5}"
        )

    # Tabla de errores.
    lineas.append("")
    lineas.append("-" * 64)
    lineas.append(" ERRORES LÉXICOS")
    lineas.append("-" * 64)
    if errores:
        for err in errores:
            lineas.append(
                f'  Carácter no reconocido "{err["caracter"]}" '
                f"(línea {err['linea']}, columna {err['columna']})"
            )
    else:
        lineas.append("  Sin errores léxicos.")

    lineas.append("")
    return "\n".join(lineas)


def nombre_archivo_log(autor):
    """Genera el nombre del log: lexico-Autor-DD-MM-YYYY-HHhMM.txt"""
    ahora = datetime.datetime.now()
    sello = ahora.strftime("%d-%m-%Y-%Hh%M")
    return f"lexico-{autor}-{sello}.txt"


def main():
    parser = argparse.ArgumentParser(
        description="Analizador léxico de un subconjunto de Kotlin (PLY)."
    )
    parser.add_argument("archivo", help="Ruta del archivo .kt a analizar")
    parser.add_argument("autor", help="NombreApellido para el log (sin espacios)")
    args = parser.parse_args()

    if not os.path.isfile(args.archivo):
        raise SystemExit(f"No se encontró el archivo: {args.archivo}")

    with open(args.archivo, encoding="utf-8") as f:
        texto = f.read()

    tokens, errores = analizar_codigo(texto)
    reporte = construir_reporte(args.archivo, args.autor, tokens, errores)

    # Salida por consola.
    print(reporte)

    # Guardar el log.
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    ruta_log = os.path.join(CARPETA_LOGS, nombre_archivo_log(args.autor))
    with open(ruta_log, "w", encoding="utf-8") as f:
        f.write(reporte)

    print(f">> Log generado: {ruta_log}")


if __name__ == "__main__":
    main()
