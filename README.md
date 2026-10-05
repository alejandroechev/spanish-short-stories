# Cuentos clásicos en español

Antología web de dieciséis obras completas de dominio público: ciencia ficción temprana en
lengua española y relato policial clásico. Textos íntegros, sin fragmentos ni resúmenes.

**Sitio:** https://alejandroechev.github.io/spanish-short-stories/

## Qué contiene

| Género | Obras | Autores |
| --- | --- | --- |
| Ciencia ficción | 10 | Leopoldo Lugones, Eduardo L. Holmberg, Rubén Darío |
| Policial | 6 | Pedro Antonio de Alarcón, E. L. Holmberg, Emilia Pardo Bazán, Edgar Allan Poe, Arthur Conan Doyle |

Poe y Conan Doyle aparecen en traducciones de época —la de Carlos Olivera (Buenos Aires, 1884)
y la española de 1909—, también en dominio público.

Total: ~89.000 palabras, unas 7 horas de lectura.

## De dónde salen los textos

Todos provienen de [Wikisource en español](https://es.wikisource.org), que transcribe y coteja
contra los facsímiles originales. Cada cuento enlaza su página de origen.

Se conserva la ortografía de la época (`fué`, `á`, `razon`). No son erratas: es el castellano
impreso de 1879 o de 1906. Solo se elimina el aparato de la edición digital —números de página,
portadillas, índices, interwikis— para dejar el texto corrido.

## Cómo está construido

HTML estático, sin framework ni dependencias en tiempo de ejecución. El sitio publicado vive en
`docs/` y se sirve con GitHub Pages.

```
catalog.py      metadatos y páginas fuente de cada obra
fetch.py        descarga el HTML renderizado desde la API de Wikisource
clean.py        limpia el marcado, recorta portadillas y detecta capítulos -> stories.json
build_site.py   genera docs/ (índice, páginas de lectura, CSS y JS)
```

Para reconstruirlo:

```bash
pip install beautifulsoup4
python3 fetch.py "Las Fuerzas Extrañas/Yzur" ...   # solo si falta raw/
python3 clean.py
python3 build_site.py
```

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
