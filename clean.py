"""Limpia el HTML renderizado de Wikisource y produce el cuerpo de cada cuento."""
import json
import os
import re
import unicodedata

from bs4 import BeautifulSoup, Comment, NavigableString

from catalog import STORIES

RAW = "raw"
ALLOWED = {"p", "em", "strong", "i", "b", "br", "blockquote", "h2", "h3", "hr", "small"}
INLINE = {"em", "strong", "i", "b", "br"}
DROP_CLASSES = {"ws-noexport", "noprint", "pagenum", "pagebreak", "mw-editsection",
                "prp-page-image", "prp-page-qualityheader", "reference", "mw-cite-backlink",
                "prp-pagequality", "ws-pagenum", "interwiki-extra", "interwiki-info",
                "mw-interlanguage-selector", "ws-notes", "prp-page-footer"}
JUNK_RE = re.compile(
    r"^(?:i:\s*i|english|fran[çc]ais|polski|svenska|[\u0400-\u04ff\s]+)$", re.I)


def raw_path(title):
    return os.path.join(RAW, re.sub(r"[^A-Za-z0-9]+", "_", title) + ".json")


def normalize(text):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", text)


def plain(fragment):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment)).strip()


def strip_junk(soup):
    for comment in soup.find_all(string=lambda s: isinstance(s, Comment)):
        comment.extract()
    for tag in soup.find_all(["style", "link", "table", "figure", "img", "span", "sup"]):
        if tag.decomposed:
            continue
        if tag.name in ("style", "link", "table", "figure", "img", "sup"):
            tag.decompose()
        elif set(tag.get("class") or []) & DROP_CLASSES:
            tag.decompose()
    for tag in soup.find_all(style=lambda v: v and "display:none" in v.replace(" ", "")):
        if not tag.decomposed:
            tag.decompose()
    for ident in ("headertemplate", "ws-data", "footertemplate", "conv-idiomas"):
        node = soup.find(id=ident)
        if node:
            node.decompose()
    for tag in soup.find_all(class_=lambda c: c and (set(c) & DROP_CLASSES)):
        if not tag.decomposed:
            tag.decompose()
    for tag in soup.find_all("a"):
        tag.unwrap()


def sanitize(node, out, in_block=False):
    """Reconstruye un árbol con solo las etiquetas permitidas, sin bloques anidados."""
    for child in node.children:
        if isinstance(child, Comment):
            continue
        if isinstance(child, NavigableString):
            out.append(str(child))
            continue
        name = child.name
        if name == "br":
            out.append("<br>")
        elif name == "hr":
            out.append("<hr>")
        elif name in INLINE:
            inner = []
            sanitize(child, inner, in_block)
            content = "".join(inner)
            if content.strip():
                out.append(f"<{name}>{content}</{name}>")
        elif name in ALLOWED:
            if in_block:
                sanitize(child, out, True)
                out.append("<br>")
                continue
            inner = []
            sanitize(child, inner, True)
            content = "".join(inner).strip()
            if content:
                out.append(f"<{name}>{content}</{name}>")
        else:
            sanitize(child, out, in_block)


def to_blocks(fragment):
    """Divide el texto en bloques limpios a partir de saltos dobles."""
    fragment = re.sub(r"(?:\s*<br>\s*){2,}", "\n\n", fragment)
    fragment = re.sub(r"</?(p|h2|h3|blockquote)>", r"\n\n", fragment)
    parts = re.split(r"\n\s*\n", fragment)
    blocks = []
    for part in parts:
        part = re.sub(r"[ \t]+", " ", part).strip()
        if not part or part == "<hr>":
            continue
        text = plain(part)
        if not text or JUNK_RE.match(text):
            continue
        part = re.sub(r"^(?:\s*<br>\s*)+|(?:\s*<br>\s*)+$", "", part.replace("\n", " ")).strip()
        if part:
            blocks.append("<p>" + part + "</p>")
    return blocks


def clean_page(title):
    data = json.load(open(raw_path(title)))
    soup = BeautifulSoup(data["html"], "html.parser")
    strip_junk(soup)
    root = soup.find(class_="mw-parser-output") or soup
    out = []
    sanitize(root, out)
    return to_blocks("".join(out))


ROMANS = ["XVIII", "XVII", "XIII", "VIII", "XIX", "XVI", "XIV", "XII", "VII", "III",
          "XX", "XV", "XI", "IX", "IV", "VI", "II", "X", "V", "I"]
ROMAN_ALT = "|".join(ROMANS)
ROMAN_START = re.compile(
    r"^<p>\s*(" + ROMAN_ALT + r")(?:\s*\.\s*|\s+)"
    r"(?=[^a-z0-9]*[A-Z\u00c1\u00c9\u00cd\u00d3\u00da\u00d1\u00a1\u00bf\u2014\u2013-])")
ROMAN_ONLY = re.compile(r"^(" + ROMAN_ALT + r")\.?$")
TRAILING_JUNK = re.compile(r"^(fin|findeltomo\w*|indice|pag|regresar\w*|notas?|)$", re.I)


def looks_like_heading(text):
    if not text or len(text) > 60:
        return False
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    return sum(c.islower() for c in letters) / len(letters) < 0.2


TRAILING_ROMAN = re.compile(r"\s+(" + "|".join(r for r in ROMANS if len(r) > 1) +
                            r")\s*</p>\s*$")


def split_trailing_romans(blocks):
    """El numeral de capitulo a veces queda pegado al final del parrafo anterior."""
    result = []
    for block in blocks:
        match = TRAILING_ROMAN.search(block)
        if match and len(plain(block)) > 40:
            result.append(block[: match.start()] + "</p>")
            result.append('<h2 class="chapter">%s</h2>' % match.group(1))
            continue
        result.append(block)
    return result


def split_roman_headings(blocks):
    """Convierte los numerales romanos iniciales en encabezados de capitulo."""
    blocks = split_trailing_romans(blocks)
    result = []
    for block in blocks:
        text = plain(block)
        match = ROMAN_START.match(block)
        if match and len(text) > 25:
            rest = "<p>" + block[match.end():]
            result.append('<h2 class="chapter">%s</h2>' % match.group(1))
            if plain(rest):
                result.append(rest)
            continue
        if ROMAN_ONLY.match(text):
            result.append('<h2 class="chapter">%s</h2>' % text.rstrip("."))
            continue
        if result and result[-1].startswith("<h2") and looks_like_heading(text):
            subtitle = text.rstrip(".").capitalize()
            result[-1] = result[-1][:-5] + " \u00b7 %s</h2>" % subtitle
            continue
        result.append(block)
    return result


def drop_trailing_junk(blocks):
    while blocks and TRAILING_JUNK.match(normalize(plain(blocks[-1]))):
        blocks.pop()
    return blocks


def is_heading(block):
    return block.startswith("<h2") or block.startswith("<h3")


def chapter_heading(blocks, label):
    """Usa el encabezado impreso del capítulo si existe; si no, sintetiza uno."""
    title = ""
    while blocks and (is_heading(blocks[0]) or len(plain(blocks[0])) < 70):
        text = plain(blocks[0])
        if not is_heading(blocks[0]) and (not text or text.endswith((".", "!", "?", "…", "»"))):
            break
        parts = [p.strip(" -–—·.") for p in re.split(r"\s*[-–—]\s*", text) if p.strip(" -–—·.")]
        parts = [p for p in parts if normalize(p) != normalize(label)]
        if parts:
            title = " ".join(parts)
        blocks.pop(0)
        if title:
            break
    label_html = label + (f" · {title}" if title else "")
    return f'<h2 class="chapter">{label_html}</h2>', blocks


def trim_front_matter(blocks, marker):
    """Descarta portadilla, dedicatoria e índice hasta el comienzo real del texto."""
    key = normalize(marker)
    for exact in (True, False):
        for index, block in enumerate(blocks):
            text = normalize(plain(block))
            if (text == key) if exact else (key in text):
                return blocks[index:]
    raise SystemExit(f"Marcador no encontrado: {marker!r}")


def drop_leading_title(blocks, story):
    targets = {normalize(story["title"]), normalize(story["title"].split("(")[0]),
               normalize(story["author"])}
    while blocks:
        text = plain(blocks[0])
        if not text or normalize(text) in targets:
            blocks.pop(0)
            continue
        break
    return blocks


def build_story(story):
    body = []
    multi = len(story["pages"]) > 1
    for page in story["pages"]:
        blocks = clean_page(page)
        if multi:
            heading, blocks = chapter_heading(blocks, page.split("/")[-1])
            blocks = [b.replace('<h2 class="chapter">', '<h3 class="seccion">')
                       .replace("</h2>", "</h3>") if b.startswith('<h2 class="chapter">') else b
                      for b in split_roman_headings(blocks)]
            body.append(heading)
        else:
            blocks = drop_leading_title(blocks, story)
        body.extend(blocks)
    if story.get("start_marker") and not multi:
        body = trim_front_matter(body, story["start_marker"])
    if not multi:
        body = split_roman_headings(body)
    if story.get("end_marker"):
        key = normalize(story["end_marker"])
        for index in range(len(body) - 1, -1, -1):
            if key in normalize(plain(body[index])):
                body = body[: index + 1]
                break
    body = drop_trailing_junk(body)
    html = "\n".join(body)
    words = len(plain(html).split())
    return html, words


def main():
    built = []
    for story in STORIES:
        html, words = build_story(story)
        record = {k: v for k, v in story.items() if k not in ("start_marker", "end_marker")}
        record["body"] = html
        record["words"] = words
        record["minutes"] = max(1, round(words / 200))
        record["source_urls"] = [
            "https://es.wikisource.org/wiki/" + p.replace(" ", "_") for p in story["pages"]
        ]
        built.append(record)
        print(f"{words:>7} palabras  {story['id']}")
    json.dump(built, open("stories.json", "w"), ensure_ascii=False, indent=1)
    print("\nTotal:", sum(b["words"] for b in built), "palabras en", len(built), "obras")


if __name__ == "__main__":
    main()
