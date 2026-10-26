#!/usr/bin/env python3
"""Genera una página por auto en autos/<VIN>.html (para que al compartir el link
por WhatsApp/Facebook aparezca la foto, el título y el precio) y el sitemap.xml.

Correr después de cada actualización de stock:
    python3 tools/generar_paginas.py
"""
import html, json, re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://palmtreemotors.net/"
OUT = ROOT / "autos"

TYPES_ES = {"pickup": "Pickup", "suv": "SUV", "sedan": "Sedán", "minivan": "Minivan",
            "hatchback": "Hatchback", "coupe": "Coupé", "convertible": "Convertible"}
BODY = {"pickup": "Pickup", "suv": "SUV", "sedan": "Sedan", "minivan": "Minivan",
        "hatchback": "Hatchback", "coupe": "Coupe", "convertible": "Convertible"}


def load_vehicles():
    src = (ROOT / "assets/js/vehicles.js").read_text(encoding="utf-8")
    cars = []
    for line in src.splitlines():
        if "vin:" not in line:
            continue
        f = dict(re.findall(r'(\w+):"([^"]*)"', line))
        f["year"] = re.search(r"year:(\d+)", line).group(1)
        m = re.search(r'photo:(null|"[^"]*")', line)
        f["photo"] = None if not m or m.group(1) == "null" else m.group(1).strip('"')
        cars.append(f)
    return cars


def page(v):
    label = f'{v["year"]} {v["make"]} {v["model"]}'
    price = v.get("price", "")
    img = BASE + (v["photo"] or "assets/og-palmtree.jpg")
    title = f"{label} | Palm Tree Motors"
    desc = (f'{TYPES_ES.get(v["type"], "")} · {v["miles"]} millas · Monto a financiar desde ${price} (sujeto a aprobación). '
            f'Título limpio y 3 años de garantía. Financiamiento para todo tipo de crédito.')
    target = f'../auto.html?id={v["vin"]}'
    url = f'{BASE}autos/{v["vin"]}.html'
    num_price = re.sub(r"[^\d]", "", price) or "0"
    ld = {
        "@context": "https://schema.org", "@type": "Car", "name": label,
        "brand": {"@type": "Brand", "name": v["make"]}, "model": v["model"],
        "vehicleModelDate": v["year"], "vehicleIdentificationNumber": v["vin"],
        "bodyType": BODY.get(v["type"], ""), "itemCondition": "https://schema.org/UsedCondition",
        "mileageFromOdometer": {"@type": "QuantitativeValue",
                                "value": re.sub(r"[^\d]", "", v["miles"]) or "0", "unitCode": "SMI"},
        "image": img, "url": url,
        "offers": {"@type": "Offer", "price": num_price, "priceCurrency": "USD",
                   "availability": "https://schema.org/InStock",
                   "seller": {"@type": "AutoDealer", "name": "Palm Tree Motors",
                              "telephone": "+1-571-424-6410"}},
    }
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="Palm Tree Motors">
<meta property="og:title" content="{e(label)} — ${e(price)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{e(img)}">
<meta property="og:locale" content="es_US">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace({json.dumps(target)});</script>
</head>
<body style="font-family:sans-serif;padding:40px;text-align:center">
<p><a href="{target}">{e(label)} — Palm Tree Motors</a></p>
</body>
</html>
"""


def main():
    cars = load_vehicles()
    OUT.mkdir(exist_ok=True)
    keep = set()
    for v in cars:
        if not v.get("vin"):
            continue
        name = f'{v["vin"]}.html'
        keep.add(name)
        (OUT / name).write_text(page(v), encoding="utf-8")
    removed = 0
    for p in OUT.glob("*.html"):
        if p.name not in keep:
            p.unlink(); removed += 1
    today = date.today().isoformat()
    urls = [BASE] + [f"{BASE}autos/{n}" for n in sorted(keep)]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls]
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    print(f"Páginas de autos: {len(keep)} (borradas {removed}) · sitemap.xml actualizado")


if __name__ == "__main__":
    main()
