import argparse
import datetime
import os

import parser as analizador

CARPETA_LOGS = "logs"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("usuarioGit")
    args = ap.parse_args()

    with open(args.archivo, encoding="utf-8") as f:
        texto = f.read()

    exito, _, errores = analizador.analizar_sintactico(texto)

    ahora = datetime.datetime.now()
    lineas = [
        "ANALIZADOR SINTACTICO - SUBCONJUNTO DE KOTLIN",
        f"Archivo : {args.archivo}",
        f"Usuario : {args.usuarioGit}",
        f"Fecha   : {ahora.strftime('%d-%m-%Y %H:%M:%S')}",
        f"Resultado: {'CORRECTO' if exito else 'CON ERRORES'}",
        f"Errores sintacticos: {len(errores)}",
        "",
    ]
    if errores:
        for e in errores:
            lineas.append(f'Token inesperado "{e["token"]}" ({e["tipo"]}), linea {e["linea"]}')
            lineas.append(f"   Sugerencia: {e['sugerencia']}")
    else:
        lineas.append("Sin errores sintacticos. El programa es valido.")
    reporte = "\n".join(lineas)
    print(reporte)

    os.makedirs(CARPETA_LOGS, exist_ok=True)
    sello = ahora.strftime("%d%m%Y-%Hh%M")
    ruta = os.path.join(CARPETA_LOGS, f"sintactico-{args.usuarioGit}-{sello}.txt")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(reporte)
    print(f">> Log generado: {ruta}")


if __name__ == "__main__":
    main()
