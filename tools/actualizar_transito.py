#!/usr/bin/env python3
"""Regenera assets/js/transito.js (sección "Próximos ingresos") con los autos
"In Transit" de DealerNode.

Uso: python3 tools/actualizar_transito.py transito.txt
Formato (una línea por auto, separado por |):
  T|VIN|año|marca|modelo|trim|estilo|combustible|millas|costo|llegada estimada (ej. November 12, 2026)

El archivo reemplaza la lista completa: un auto que ya no está en la lista
(llegó o se canceló) desaparece de "Próximos ingresos". Las fotos que ya
tenían los autos que siguen en tránsito se conservan.
"""
import re, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from actualizar_stock import make_name, model_name, money, TYPES, FUEL  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TFILE = ROOT / "assets/js/transito.js"


def old_photos():
    if not TFILE.exists():
        return {}
    src = TFILE.read_text(encoding="utf-8")
    return {m.group(1): m.group(2) for m in re.finditer(r'vin:"([A-Z0-9]+)"[^\n]*photo:"([^"]+)"', src)}


def eta_iso(s):
    s = (s or "").strip()
    for f in ("%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, f).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ""


def main(path):
    photos = old_photos()
    rows, seen = [], set()
    for l in Path(path).read_text(encoding="utf-8").splitlines():
        p = [x.strip() for x in l.split("|")]
        if len(p) < 11 or p[0] != "T" or p[1] in seen:
            continue
        _, vin, year, make, model, trim, style, fuel, miles, cost, eta = p[:11]
        seen.add(vin)
        photo = f'"{photos[vin]}"' if vin in photos and (ROOT / photos[vin]).exists() else "null"
        rows.append(('    { year:%s, make:"%s", model:"%s", type:"%s", miles:"%s", '
                     'trans:"%s · Automática", price:"%s", priceNote:"Monto a financiar desde", '
                     'eta:"%s", vin:"%s", photo:%s },') % (
            int(year), make_name(make), model_name(model, trim),
            TYPES.get(style.upper(), "suv"), miles, FUEL.get(fuel.upper(), "Gasolina"),
            money(cost), eta_iso(eta), vin, photo))
    out = ("  // Autos comprados que todavía no llegaron (DealerNode: In Transit).\n"
           "  // Lo genera tools/actualizar_transito.py — no editar a mano.\n"
           "  const transito = [\n" + "\n".join(rows) + "\n  ];\n")
    TFILE.write_text(out, encoding="utf-8")
    print(f"Próximos ingresos: {len(rows)} autos")


if __name__ == "__main__":
    main(sys.argv[1])
