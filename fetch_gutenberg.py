"""Descarga los cuentos de Asimov desde Project Gutenberg y los segmenta en párrafos."""
import json
import os
import re
import sys
import time
import urllib.request

OUT = "en"
UA = "SpanishStoryCollector/1.0 (https://github.com/alejandroechev public-domain anthology)"

BOOKS = {
    31547: "youth",
    76871: "the-magnificent-possession",
    68377: "lets-get-together",
    77254: "everest",
    78751: "silly-asses",
}

# Primera frase del relato: todo lo anterior es portadilla o reclamo de la revista.
START = {
    "youth": "Red and Slim found the two strange little animals",
    "the-magnificent-possession": "Walter Sills reflected now",
    "lets-get-together": "A kind of peace had endured",
    "everest": "In 1952 they were about ready",
    "silly-asses": "Naron of the long-lived Rigellian race",
}

DROP = re.compile(
    r"Transcriber|Extensive research|etext was produced|This story appeared|Produced by|"
    r"Obvious errors|^\[Illustration|^\s*\[?Illustration\]?\s*$|Project Gutenberg",
    re.I)


def download(book_id):
    last = None
    for url in (f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
                f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(request, timeout=40).read().decode("utf8", "ignore")
        except Exception as error:  # noqa: BLE001
            last = error
    raise SystemExit(f"No se pudo descargar {book_id}: {last}")


def fix_mojibake(text):
    """Algunos volcados de Gutenberg traen UTF-8 releído como Latin-1."""
    if not re.search(r"Ã.|â€|Â.", text):
        return text
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def extract(raw):
    body = re.split(r"\*\*\* ?START OF TH[EI]S? PROJECT GUTENBERG EBOOK.*?\*\*\*", raw, 1)[-1]
    body = re.split(r"\*\*\* ?END OF TH[EI]S? PROJECT GUTENBERG EBOOK", body, 1)[0]
    body = body.replace("\r\n", "\n")
    # El encabezado de la transcripción va entre corchetes; la nota de PD no es del autor.
    body = re.sub(r"\[Transcriber's Note:.*?\]", "", body, flags=re.S)
    body = re.sub(r"\[Illustration:.*?\]", "", body, flags=re.S)
    paragraphs = [fix_mojibake(re.sub(r"\s+", " ", p).strip())
                  for p in re.split(r"\n\s*\n", body)]
    return [p for p in paragraphs if p]


def trim(paragraphs, slug):
    marker = START[slug]
    for index, paragraph in enumerate(paragraphs):
        if paragraph.startswith(marker):
            paragraphs = paragraphs[index:]
            break
    else:
        raise SystemExit(f"Marcador inicial no encontrado en {slug}")
    return [p for p in paragraphs if not DROP.search(p)]


def main():
    os.makedirs(OUT, exist_ok=True)
    for book_id, slug in BOOKS.items():
        paragraphs = trim(extract(download(book_id)), slug)
        path = os.path.join(OUT, slug + ".json")
        json.dump({"gutenberg_id": book_id, "slug": slug, "paragraphs": paragraphs},
                  open(path, "w"), ensure_ascii=False, indent=1)
        words = sum(len(p.split()) for p in paragraphs)
        print(f"{words:>7} palabras  {len(paragraphs):>4} párrafos  {slug}")
        time.sleep(2)


if __name__ == "__main__":
    main()
