# Cuentos clásicos en español

Antología web de veintiuna obras completas de dominio público: ciencia ficción temprana en
lengua española, cinco cuentos de Asimov traducidos para esta antología, y relato policial
clásico. Textos íntegros, sin fragmentos ni resúmenes. Todo se lee en español.

**Sitio:** https://alejandroechev.github.io/spanish-short-stories/

## Qué contiene

| Género | Obras | Autores |
| --- | --- | --- |
| Ciencia ficción | 15 | Leopoldo Lugones, Eduardo L. Holmberg, Rubén Darío, Isaac Asimov |
| Policial | 6 | Pedro Antonio de Alarcón, E. L. Holmberg, Emilia Pardo Bazán, Edgar Allan Poe, Arthur Conan Doyle |

Poe y Conan Doyle aparecen en traducciones de época —la de Carlos Olivera (Buenos Aires, 1884)
y la española de 1909—, también en dominio público. Los cinco cuentos de Asimov se traducen
aquí por primera vez para este proyecto.

Total: ~113.000 palabras, unas 9 horas de lectura.

## De dónde salen los textos

Los originales en español provienen de [Wikisource](https://es.wikisource.org), que transcribe
y coteja contra los facsímiles. Los cuentos de Asimov provienen de
[Project Gutenberg](https://www.gutenberg.org). Cada cuento enlaza su página de origen.

Se conserva la ortografía de la época (`fué`, `á`, `razon`). No son erratas: es el castellano
impreso de 1879 o de 1906. Solo se elimina el aparato de la edición digital —números de página,
portadillas, índices, interwikis— para dejar el texto corrido.

## Los cuentos de Asimov, y su situación legal

Cinco relatos de revista publicados entre 1940 y 1958 cuyo copyright **no fue renovado** en el
plazo de 28 años que exigía la ley estadounidense de entonces. Project Gutenberg los distribuye
con esa base, tras su proceso de *copyright clearance*.

> ⚠️ Ese dominio público es **específico de los Estados Unidos**. Donde rige el plazo de vida del
> autor más 70 u 80 años —España, Argentina, Chile, México— la obra de Asimov, fallecido en 1992,
> puede seguir protegida, y una traducción es obra derivada. Cada cuento del bloque lleva esa
> advertencia visible en su página.

Las traducciones son propias y siguen la guía de [`TRADUCCION.md`](TRADUCCION.md): fidelidad
párrafo a párrafo, español neutro, diálogo con raya. `translate_tools.py assemble` falla si el
número de párrafos traducidos no coincide exactamente con el original.

## Cómo está construido

HTML estático, sin framework ni dependencias en tiempo de ejecución. El sitio publicado vive en
`docs/` y se sirve con GitHub Pages.

```
catalog.py           metadatos y páginas fuente de cada obra
fetch.py             descarga el HTML renderizado desde la API de Wikisource
fetch_gutenberg.py   descarga y segmenta los originales en inglés de Project Gutenberg
translate_tools.py   traduce por tramos y valida el 1:1 con el original
clean.py             limpia el marcado, recorta portadillas y detecta capítulos -> stories.json
build_site.py        genera docs/ (índice, páginas de lectura, CSS y JS)
```

Para reconstruirlo:

```bash
pip install beautifulsoup4
python3 fetch.py "Las Fuerzas Extrañas/Yzur" ...   # solo si falta raw/
python3 fetch_gutenberg.py                          # originales en inglés
python3 clean.py
python3 build_site.py
```

Las traducciones ya hechas viven en `es/*.json` y se versionan; `en/` y `raw/` no.

`fetch.py` espera 3 segundos entre peticiones y envía un `User-Agent` identificable, como pide
la política de la API de Wikimedia. Los archivos de `raw/` no se versionan.

## Lectura

- Tres temas: día, sepia y noche.
- Tamaño de texto ajustable, con la preferencia guardada en el navegador.
- Barra de progreso e índice de capítulos en las obras largas.
- Filtros por género y autor, orden por extensión o año, y búsqueda (atajo `/`).

## Licencia

Las obras están en dominio público. El código y el diseño se publican bajo licencia MIT
(ver `LICENSE`). Las transcripciones de Wikisource se reutilizan conforme a sus términos.
