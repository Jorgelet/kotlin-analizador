import argparse
import datetime
import os

import parser as parser_mod
import semantico as analizador

CARPETA_LOGS = "logs"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("usuarioGit")
    args = ap.parse_args()

    with open(args.archivo, encoding="utf-8") as f:
        texto = f.read()

    exito_sint, ast, _ = parser_mod.analizar_sintactico(texto)
    ok, errores = analizador.analizar_semantico(ast)

    if ok and exito_sint:
        resultado = "CORRECTO"
    else:
        resultado = "CON ERRORES"

    ahora = datetime.datetime.now()
    lineas = [
        "ANALIZADOR SEMANTICO - SUBCONJUNTO DE KOTLIN",
        f"Archivo : {args.archivo}",
        f"Usuario : {args.usuarioGit}",
        f"Fecha   : {ahora.strftime('%d-%m-%Y %H:%M:%S')}",
        f"Resultado: {resultado}",
        f"Errores semanticos: {len(errores)}",
        "",
    ]
    if not exito_sint:
        lineas.append("AVISO: hay errores sintacticos; corrigelos antes del analisis semantico.")
        lineas.append("")
    if errores:
        for e in errores:
            lineas.append(f"- {e['mensaje']}")
    else:
        lineas.append("Sin errores semanticos. El programa es valido.")
    reporte = "\n".join(lineas)
    print(reporte)

    os.makedirs(CARPETA_LOGS, exist_ok=True)
    sello = ahora.strftime("%d%m%Y-%Hh%M")
    ruta = os.path.join(CARPETA_LOGS, f"semantico-{args.usuarioGit}-{sello}.txt")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(reporte)
    print(f">> Log generado: {ruta}")


if __name__ == "__main__":
    main()
