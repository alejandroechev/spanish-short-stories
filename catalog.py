"""Catálogo de la antología: metadatos y páginas fuente en Wikisource."""

SF = "ciencia-ficcion"
POL = "policial"

STORIES = [
    dict(
        id="yzur", title="Yzur", author="Leopoldo Lugones", year=1906,
        country="Argentina", genre=SF, kind="Cuento",
        collection="Las fuerzas extrañas",
        pages=["Las Fuerzas Extrañas/Yzur"],
        teaser="Un hombre decide probar que los monos son humanos que renunciaron al habla, "
               "y somete a su chimpancé a una pedagogía implacable.",
        note="Pieza fundacional de la ciencia ficción en lengua española: experimento "
             "científico, hybris y un final célebre.",
    ),
    dict(
        id="la-lluvia-de-fuego", title="La lluvia de fuego", author="Leopoldo Lugones", year=1906,
        country="Argentina", genre=SF, kind="Cuento",
        collection="Las fuerzas extrañas",
        pages=["Las Fuerzas Extrañas/La lluvia de fuego"],
        teaser="Evocación de un hombre acomodado de Gomorra mientras del cielo empieza a caer "
               "una menudísima lluvia de cobre incandescente.",
        note="Catástrofe narrada con frialdad de cronista: un clásico del relato apocalíptico.",
    ),
    dict(
        id="la-fuerza-omega", title="La fuerza Omega", author="Leopoldo Lugones", year=1906,
        country="Argentina", genre=SF, kind="Cuento",
        collection="Las fuerzas extrañas",
        pages=["Las Fuerzas Extrañas/La fuerza Omega"],
        teaser="Un inventor logra concentrar el sonido hasta convertirlo en un arma capaz de "
               "pulverizar la materia.",
        note="Ciencia ficción especulativa construida sobre la física acústica de su época.",
    ),
    dict(
        id="un-fenomeno-inexplicable", title="Un fenómeno inexplicable", author="Leopoldo Lugones",
        year=1906, country="Argentina", genre=SF, kind="Cuento",
        collection="Las fuerzas extrañas",
        pages=["Las Fuerzas Extrañas/Un fenómeno inexplicable"],
        teaser="Un viajero se hospeda en casa de un inglés atormentado por una sombra que no "
               "se corresponde con su cuerpo.",
        note="Teosofía, darwinismo y horror científico en una misma mesa de trabajo.",
    ),
    dict(
        id="viola-acherontia", title="Viola acherontia", author="Leopoldo Lugones", year=1906,
        country="Argentina", genre=SF, kind="Cuento",
        collection="Las fuerzas extrañas",
        pages=["Las Fuerzas Extrañas/Viola acherontia"],
        teaser="Un jardinero obsesivo intenta criar una violeta que mate: sugestión vegetal, "
               "cruzas y crueldad de invernadero.",
        note="Bioingeniería imaginada medio siglo antes de la genética moderna.",
    ),
    dict(
        id="el-psychon", title="El Psychon", author="Leopoldo Lugones", year=1906,
        country="Argentina", genre=SF, kind="Cuento",
        collection="Las fuerzas extrañas",
        pages=["Las Fuerzas Extrañas/El psychon"],
        teaser="Un sabio consigue licuar el pensamiento y guardarlo en un frasco. El frasco, "
               "naturalmente, se abre.",
        note="La idea de materializar la mente, tratada con humor y rigor pseudocientífico.",
    ),
    dict(
        id="horacio-kalibang", title="Horacio Kalibang o los autómatas",
        author="Eduardo Ladislao Holmberg", year=1879, country="Argentina", genre=SF,
        kind="Cuento largo", collection=None,
        pages=["Horacio Kalibang o los autómatas"],
        start_marker="I.",
        teaser="Un constructor alemán de autómatas siembra un pueblo de muñecos indistinguibles "
               "de las personas, y nadie sabe ya quién es de carne.",
        note="Uno de los primeros relatos robóticos de la literatura hispanoamericana.",
    ),
    dict(
        id="el-rubi", title="El rubí", author="Rubén Darío", year=1888, country="Nicaragua",
        genre=SF, kind="Cuento", collection="Azul…",
        pages=["El rubí"],
        end_marker="camino de una pradera en flor",
        teaser="Los gnomos se indignan: un químico parisino ha fabricado en su laboratorio un "
               "rubí artificial idéntico al verdadero.",
        note="Ciencia de síntesis contra magia antigua, en la prosa inaugural del modernismo.",
    ),
    dict(
        id="la-extrana-muerte-de-fray-pedro", title="La extraña muerte de Fray Pedro",
        author="Rubén Darío", year=1913, country="Nicaragua", genre=SF, kind="Cuento",
        collection="Cuentos y crónicas",
        pages=["La extraña muerte de Fray Pedro"],
        teaser="Un fraile se entrega al estudio de los rayos X y decide fotografiar aquello que "
               "ningún hombre debería ver.",
        note="El descubrimiento de Röntgen convertido en fábula sobre los límites del saber.",
    ),
    dict(
        id="el-caso-de-la-senorita-amelia", title="El caso de la señorita Amelia",
        author="Rubén Darío", year=1894, country="Nicaragua", genre=SF, kind="Cuento",
        collection="Cuentos y crónicas",
        pages=["El caso de la señorita Amelia"],
        teaser="El doctor Z narra, una noche de fin de año, la historia de una niña que lleva "
               "veintitrés años sin crecer un solo día.",
        note="Tiempo detenido y ocultismo fin de siglo: ciencia ficción antes del nombre.",
    ),

    dict(
        id="el-clavo", title="El clavo (Causa célebre)", author="Pedro Antonio de Alarcón",
        year=1853, country="España", genre=POL, kind="Novela corta",
        collection="Cuentos amatorios",
        pages=["El clavo/%s" % n for n in
               ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
                "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"]],
        teaser="Una calavera aparece atravesada por un clavo. Un juez instructor sigue la pista "
               "del crimen hasta donde menos querría llegar.",
        note="Considerado el primer relato policial español, anterior a Sherlock Holmes.",
    ),
    dict(
        id="la-bolsa-de-huesos", title="La bolsa de huesos",
        author="Eduardo Ladislao Holmberg", year=1896, country="Argentina", genre=POL,
        kind="Novela corta", collection=None,
        pages=["La bolsa de huesos"],
        start_marker="I.",
        end_marker="dejarse subyugar por las armonías del viento",
        teaser="Un médico aficionado a la deducción recibe una bolsa con dos cráneos y decide "
               "resolver por su cuenta un caso que la policía ni siquiera ve.",
        note="La primera novela policial argentina, con un detective-naturalista memorable.",
    ),
    dict(
        id="la-cita", title="La cita", author="Emilia Pardo Bazán", year=1912, country="España",
        genre=POL, kind="Cuento", collection="Cuentos trágicos",
        pages=["La cita (Pardo Bazán)"],
        teaser="Una mujer acude a una cita secreta y descubre, demasiado tarde, qué clase de "
               "hombre la espera del otro lado de la puerta.",
        note="Pardo Bazán fue pionera del relato criminal en España; aquí, en estado puro.",
    ),
    dict(
        id="los-crimenes-de-la-calle-morgue", title="Los crímenes de la calle Morgue",
        author="Edgar Allan Poe", year=1841, country="Estados Unidos", genre=POL, kind="Cuento",
        collection="Novelas y cuentos (Buenos Aires, 1884)",
        translator="Carlos Olivera", translation_year=1884,
        pages=["Los crímenes de la calle Morgue (Olivera tr.)"],
        end_marker="Déjele Vd. discurrir",
        teaser="Dos mujeres aparecen asesinadas en una habitación cerrada por dentro. "
               "Auguste Dupin razona donde la policía solo mira.",
        note="El cuento que inventó el género: el primer detective de la literatura.",
    ),
    dict(
        id="la-carta-robada", title="La carta robada", author="Edgar Allan Poe", year=1844,
        country="Estados Unidos", genre=POL, kind="Cuento",
        collection="Novelas y cuentos (Buenos Aires, 1884)",
        translator="Carlos Olivera", translation_year=1884,
        pages=["La carta robada (Olivera tr.)"],
        end_marker="digne de Thyeste",
        teaser="La policía ha registrado milímetro a milímetro la casa del ministro y no "
               "encuentra la carta. Dupin solo necesita una visita.",
        note="La lección clásica sobre lo que se esconde mejor: aquello que está a la vista.",
    ),
    dict(
        id="el-carbunclo-azul", title="El carbunclo azul", author="Arthur Conan Doyle", year=1892,
        country="Reino Unido", genre=POL, kind="Cuento",
        collection="Aventuras de Sherlock Holmes, tomo I (1909)",
        translator="traducción española de 1909", translation_year=1909,
        pages=["El carbunclo azul"],
        end_marker="también una ave será el principal motivo",
        teaser="Un sombrero viejo, un ganso de Navidad y, dentro del buche, la piedra preciosa "
               "más buscada de Londres.",
        note="Sherlock Holmes en versión castellana de 1909, con su sabor de época.",
    ),
]
