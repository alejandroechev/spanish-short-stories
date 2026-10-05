# Guía de traducción

Reglas que siguen todas las traducciones al español de esta antología.

## Fidelidad

- **Uno a uno.** Cada párrafo del original produce exactamente un párrafo traducido, en el mismo
  orden. No se funden ni se parten párrafos, aunque la sintaxis española lo pida.
- **Nada se resume ni se omite.** Ni una frase. Tampoco se añaden notas del traductor.
- **Los nombres propios no se traducen:** Red, Slim, Naron, Walter Sills, Eugene Taylor,
  Elias Lynn. Los topónimos con forma española consolidada sí: *Everest*, *Hudson*, *Nueva York*.

## Registro

- Español literario **neutro**: tuteo (nunca *vos* ni *vosotros*), léxico panhispánico.
- Se prefiere el término latinoamericano cuando hay dos: *computadora* (no *ordenador*),
  *auto* o *coche* según el ritmo de la frase, *celular* no aparece en estos textos.
- Se respeta el tono de cada pieza: Asimov alterna la comedia seca con la exposición técnica.
  Las explicaciones científicas se traducen con precisión, no con aproximaciones.

## Puntuación

- **Diálogo con raya**, a la española, no con comillas inglesas:
  `—No lo creo —dijo Lynn—. Es imposible.`
- Comillas españolas «» para citas dentro del texto; comillas inglesas solo si están anidadas.
- Signos de apertura obligatorios: `¿` y `¡`.
- Las cursivas del original, marcadas `_así_` en el texto de Gutenberg, pasan a `<em>así</em>`.
- Los separadores de escena (líneas de asteriscos, `* * *`) se conservan tal cual, como párrafo
  propio.

## Procedimiento

Se traduce por tramos y se valida el recuento al final:

```bash
python3 translate_tools.py show <slug> <desde> <hasta>   # ver el original numerado
python3 translate_tools.py assemble <slug>               # unir tramos y validar 1:1
python3 translate_tools.py status                        # avance
```

Cada tramo se guarda en `es/parts/<slug>-<índice-inicial>.json` como un array JSON de cadenas.
`assemble` falla si hay huecos, solapamientos, párrafos vacíos o si el recuento no coincide con
el original.
