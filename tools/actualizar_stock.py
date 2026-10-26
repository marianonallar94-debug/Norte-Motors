#!/usr/bin/env python3
"""Aplica a assets/js/vehicles.js los cambios de stock sacados de DealerNode.

Uso: python3 tools/actualizar_stock.py cambios.txt
Formato de cambios.txt (una línea por cambio, separado por |):
  R|VIN                                  -> sacar (vendido / ya no disponible)
  P|VIN|precio_web_actual|costo_nuevo     -> cambiar precio (precio = costo)
  A|VIN|año|marca|modelo|trim|estilo|combustible|millas|costo  -> agregar
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VFILE = ROOT / "assets/js/vehicles.js"

UPPER_MAKES = {"GMC", "RAM", "BMW", "KIA"}
MODEL_FIX = {"RAV4": "RAV4", "CR-V": "CR-V", "HR-V": "HR-V", "C-HR": "C-HR",
             "4RUNNER": "4Runner", "CX-5": "Cx-5", "CX-30": "Cx-30", "F-150": "F-150",
             "SQ5": "SQ5", "Q5": "Q5", "Q7": "Q7", "COROLLA CROSS": "Corolla Cross"}
TRIM_KEEP = {"PLATINIUM": "Platinum"}
TYPES = {"SUV": "suv", "PICKUP": "pickup", "SEDAN": "sedan", "MINIVAN": "minivan",
         "COUPE": "coupe", "HATCHBACK": "hatchback", "CONVERTIBLE": "convertible"}
FUEL = {"GASOLINE": "Gasolina", "HYBRID": "Híbrido", "DIESEL": "Diesel",
        "FLEX FUEL": "Flex Fuel", "ELECTRIC": "Eléctrico"}


def money(c):
    return f"{round(float(c.replace('$', '').replace(',', ''))):,}"


def make_name(m):
    m = m.strip()
    return m if m in UPPER_MAKES else m.title()


def word(w):
    # siglas cortas (LE, XLE, SR5, EX-L) en mayúscula; palabras normales en Title
    if any(ch.isdigit() for ch in w) or len(w) <= 3 or "-" in w:
        return w.upper()
    return TRIM_KEEP.get(w, w.title())


def model_name(model, trim):
    model = model.strip().upper()
    base = MODEL_FIX.get(model, " ".join(word(w) for w in model.split()))
    t = trim.split(",")[0].strip()  # DealerNode a veces lista varias versiones
    t = " ".join(word(w) for w in t.split()) if t and t.upper() != "N/A" else ""
    return f"{base} {t}".strip()


def main(path):
    src = VFILE.read_text(encoding="utf-8")
    lines = [l.strip() for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    removed = added = repriced = 0
    for l in lines:
        p = l.split("|")
        kind, vin = p[0], p[1]
        row_re = re.compile(r'^[ \t]*\{[^\n]*vin:"%s"[^\n]*\},?[ \t]*\n' % re.escape(vin), re.M)
        if kind == "R":
            src, n = row_re.subn("", src)
            removed += n
        elif kind == "P":
            new = money(p[3])
            def rep(m):
                return re.sub(r'price:"[^"]*"', f'price:"{new}"', m.group(0))
            src, n = row_re.subn(rep, src)
            repriced += n
        elif kind == "A":
            if row_re.search(src):
                continue
            _, vin, year, make, model, trim, style, fuel, miles, cost = p[:10]
            entry = ('    { year:%s, make:"%s", model:"%s", type:"%s", miles:"%s", '
                     'trans:"%s · Automática", price:"%s", priceNote:"Monto a financiar desde", '
                     'vin:"%s", photo:null },\n') % (
                int(year), make_name(make), model_name(model, trim),
                TYPES.get(style.upper(), "suv"), miles.strip(),
                FUEL.get(fuel.upper(), "Gasolina"), money(cost), vin)
            src = re.sub(r"\n\s*\];\s*$", "\n" + entry.rstrip("\n") + "\n  ];\n", src.rstrip() + "\n", count=1)
            added += 1
    VFILE.write_text(src, encoding="utf-8")
    total = len(re.findall(r'vin:"', src))
    print(f"Sacados: {removed} | Agregados: {added} | Precios cambiados: {repriced} | Total en la web: {total}")
    # Regenera las páginas para compartir (autos/<VIN>.html) y el sitemap
    import subprocess
    subprocess.run([sys.executable, str(Path(__file__).with_name("generar_paginas.py"))], check=False)


if __name__ == "__main__":
    main(sys.argv[1])
