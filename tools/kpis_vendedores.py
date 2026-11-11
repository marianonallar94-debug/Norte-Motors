#!/usr/bin/env python3
"""Publica los números de la campaña para el portal de vendedores.

Junta el resumen que escribe el CRM (resumen/kpis) con los números de Meta
y escribe vendedores/kpis.json. Solo cambia el archivo si cambió algún número,
así no hay commits vacíos.

Uso:
  python3 tools/kpis_vendedores.py --resumen RUTA.json \
      --gasto-total 7.15 --chats-total 1 --gasto-hoy 7.15 --chats-hoy 1
"""
import argparse
import datetime as dt
import json
import os
import sys

INICIO = "2026-11-11"
FIN = "2026-12-13"
SALIDA = os.path.join(os.path.dirname(__file__), "..", "vendedores", "kpis.json")


def cargar_resumen(ruta):
    with open(ruta, encoding="utf-8") as f:
        obj = json.load(f)
    # el archivo puede traer el documento solo o envuelto como {"id":..., "data": {...}}
    if isinstance(obj, dict) and "embudo" not in obj and isinstance(obj.get("data"), dict):
        obj = obj["data"]
    if not isinstance(obj, dict) or "embudo" not in obj:
        sys.exit("El resumen del CRM no tiene el formato esperado (falta 'embudo').")
    return obj


def numero(v):
    return round(float(v), 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resumen", required=True)
    ap.add_argument("--gasto-total", type=float, required=True)
    ap.add_argument("--chats-total", type=int, required=True)
    ap.add_argument("--gasto-hoy", type=float, required=True)
    ap.add_argument("--chats-hoy", type=int, required=True)
    a = ap.parse_args()

    r = cargar_resumen(a.resumen)
    equipo = []
    for x in r.get("equipo") or []:
        equipo.append({
            "nombre": str(x.get("nombre") or "Vendedor").split()[0],
            "clientes": int(x.get("clientes") or 0),
            "activos": int(x.get("activos") or 0),
            "sinContestar": int(x.get("sinContestar") or 0),
            "respuestaMin": x.get("respuestaMin"),
            "citas": int(x.get("citas") or 0),
            "vinieron": int(x.get("vinieron") or 0),
            "ventas": int(x.get("ventas") or 0),
        })

    nuevo = {
        "campana": {
            "inicio": INICIO, "fin": FIN,
            "gastoTotal": numero(a.gasto_total), "chatsTotal": a.chats_total,
            "gastoHoy": numero(a.gasto_hoy), "chatsHoy": a.chats_hoy,
        },
        "embudo": r.get("embudo") or {},
        "meta": r.get("meta") or {"chats": 100, "citas": 30, "vinieron": 18, "ventas": 5},
        "sinAsignar": int(r.get("sinAsignar") or 0),
        "hoy": r.get("hoy") or {},
        "equipo": equipo,
    }

    ruta = os.path.normpath(SALIDA)
    viejo = None
    if os.path.exists(ruta):
        try:
            with open(ruta, encoding="utf-8") as f:
                viejo = json.load(f)
            viejo.pop("actualizado", None)
        except (OSError, ValueError):
            viejo = None
    if viejo == nuevo:
        print("Sin cambios en los números; no se toca kpis.json")
        return

    nuevo = dict(actualizado=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **nuevo)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(nuevo, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("kpis.json actualizado")


if __name__ == "__main__":
    main()
