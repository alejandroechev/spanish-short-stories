"""Herramientas para traducir por tramos y validar que no se pierda texto.

Uso:
    python3 translate_tools.py show <slug> <desde> <hasta>   # muestra párrafos numerados
    python3 translate_tools.py assemble <slug>               # une los tramos y valida
    python3 translate_tools.py status                        # avance de cada cuento
"""
import glob
import json
import os
import re
import sys

EN = "en"
ES = "es"
PARTS = os.path.join(ES, "parts")


def load_en(slug):
    return json.load(open(os.path.join(EN, slug + ".json")))["paragraphs"]


def show(slug, start, end):
    paragraphs = load_en(slug)
    for index in range(int(start), min(int(end), len(paragraphs))):
        print(f"[{index}] {paragraphs[index]}")
        print()


def assemble(slug):
    """Une es/parts/<slug>-<inicio>.json en un único archivo y valida el recuento."""
    source = load_en(slug)
    chunks = {}
    for path in glob.glob(os.path.join(PARTS, f"{slug}-*.json")):
        start = int(re.search(rf"{re.escape(slug)}-(\d+)\.json$", path).group(1))
        chunks[start] = json.load(open(path))
    if not chunks:
        raise SystemExit(f"No hay tramos para {slug}")

    merged = []
    for start in sorted(chunks):
        if start != len(merged):
            raise SystemExit(
                f"Hueco o solapamiento en {slug}: el tramo {start} llega cuando van {len(merged)}")
        merged.extend(chunks[start])

    if len(merged) != len(source):
        raise SystemExit(
            f"{slug}: {len(merged)} párrafos traducidos frente a {len(source)} originales")
    empty = [i for i, p in enumerate(merged) if not p.strip()]
    if empty:
        raise SystemExit(f"{slug}: párrafos vacíos en {empty[:10]}")

    os.makedirs(ES, exist_ok=True)
    json.dump({"slug": slug, "paragraphs": merged},
              open(os.path.join(ES, slug + ".json"), "w"), ensure_ascii=False, indent=1)
    print(f"OK {slug}: {len(merged)} párrafos, "
          f"{sum(len(p.split()) for p in merged)} palabras")


def status():
    for path in sorted(glob.glob(os.path.join(EN, "*.json"))):
        slug = os.path.basename(path)[:-5]
        total = len(load_en(slug))
        done = 0
        for part in glob.glob(os.path.join(PARTS, f"{slug}-*.json")):
            done += len(json.load(open(part)))
        final = "✓" if os.path.exists(os.path.join(ES, slug + ".json")) else " "
        print(f"{final} {slug:<30} {done:>4}/{total:<4} tramos")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    command = sys.argv[1]
    if command == "show":
        show(sys.argv[2], sys.argv[3], sys.argv[4])
    elif command == "assemble":
        assemble(sys.argv[2])
    elif command == "status":
        status()
    else:
        raise SystemExit(__doc__)
