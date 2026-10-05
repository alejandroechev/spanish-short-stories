
(function () {
  var cuerpo = document.body;
  var temas = ['dia', 'sepia', 'noche'];

  function aplicarTema(tema) {
    cuerpo.dataset.tema = tema;
    localStorage.setItem('antologia-tema', tema);
  }

  document.querySelectorAll('[data-accion="tema"]').forEach(function (boton) {
    boton.addEventListener('click', function () {
      var actual = cuerpo.dataset.tema || 'dia';
      aplicarTema(temas[(temas.indexOf(actual) + 1) % temas.length]);
    });
  });

  var tamanos = ['xs', 's', 'm', 'l', 'xl'];
  function ajustarCuerpo(paso) {
    var actual = cuerpo.dataset.cuerpo || 'm';
    var indice = Math.min(tamanos.length - 1, Math.max(0, tamanos.indexOf(actual) + paso));
    cuerpo.dataset.cuerpo = tamanos[indice];
    localStorage.setItem('antologia-cuerpo', tamanos[indice]);
  }
  var mas = document.querySelector('[data-accion="cuerpo-mas"]');
  var menos = document.querySelector('[data-accion="cuerpo-menos"]');
  if (mas) mas.addEventListener('click', function () { ajustarCuerpo(1); });
  if (menos) menos.addEventListener('click', function () { ajustarCuerpo(-1); });

  var barra = document.querySelector('.progreso span');
  if (barra) {
    var actualizar = function () {
      var alto = document.documentElement.scrollHeight - window.innerHeight;
      barra.style.width = (alto > 0 ? (window.scrollY / alto) * 100 : 0) + '%';
    };
    window.addEventListener('scroll', actualizar, { passive: true });
    window.addEventListener('resize', actualizar);
    actualizar();
  }

  var rejilla = document.getElementById('rejilla');
  if (!rejilla) return;

  var fichas = Array.prototype.slice.call(rejilla.querySelectorAll('.ficha'));
  var orden = fichas.slice();
  var aviso = document.querySelector('.sin-resultados');
  var buscar = document.getElementById('buscar');
  var autor = document.getElementById('filtro-autor');
  var ordenar = document.getElementById('orden');
  var genero = 'todos';

  function normalizar(texto) {
    return texto.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  }

  function refrescar() {
    var consulta = normalizar(buscar.value.trim());
    var autorSel = autor.value;
    var visibles = 0;
    fichas.forEach(function (ficha) {
      var ok = (genero === 'todos' || ficha.dataset.genero === genero)
        && (!autorSel || ficha.dataset.autor === autorSel)
        && (!consulta || normalizar(ficha.dataset.buscar).indexOf(consulta) !== -1);
      ficha.hidden = !ok;
      if (ok) visibles++;
    });
    aviso.hidden = visibles > 0;
  }

  function reordenar() {
    var modo = ordenar.value;
    var lista = orden.slice();
    if (modo === 'corto') {
      lista.sort(function (a, b) { return a.dataset.palabras - b.dataset.palabras; });
    } else if (modo === 'largo') {
      lista.sort(function (a, b) { return b.dataset.palabras - a.dataset.palabras; });
    } else if (modo === 'anio') {
      lista.sort(function (a, b) { return a.dataset.anio - b.dataset.anio; });
    }
    lista.forEach(function (ficha) { rejilla.appendChild(ficha); });
  }

  document.querySelectorAll('.chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      document.querySelectorAll('.chip').forEach(function (c) { c.classList.remove('activo'); });
      chip.classList.add('activo');
      genero = chip.dataset.filtro;
      refrescar();
    });
  });
  buscar.addEventListener('input', refrescar);
  autor.addEventListener('change', refrescar);
  ordenar.addEventListener('change', reordenar);

  document.addEventListener('keydown', function (evento) {
    if (evento.key === '/' && document.activeElement !== buscar) {
      evento.preventDefault();
      buscar.focus();
    }
  });
})();
