/* Privatpraxis Dr. med. Günter Pfeiler — Verhalten (Wand und Glas)
   Klein, ohne Abhängigkeiten, keine externe Anfrage. Bewegt werden nur
   transform, opacity und filter. Wer weniger Bewegung wünscht, bekommt
   den Endzustand sofort. */
(function () {
  'use strict';
  var ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var wurzel = document.documentElement;

  /* Hell / Dunkel */
  var knoepfe = document.querySelectorAll('.modus');
  var wandBilder = function () {
    var k = wurzel.dataset.modus === 'dunkel' ? 'dunkel' : 'hell';
    Array.prototype.forEach.call(document.querySelectorAll('.wand-bild[data-hell]'), function (img) { if (img.getAttribute('src') !== img.dataset[k]) img.src = img.dataset[k]; });
    Array.prototype.forEach.call(document.querySelectorAll('source[data-hell]'), function (so) { if (so.getAttribute('srcset') !== so.dataset[k]) so.srcset = so.dataset[k]; });
  };
  var modusZeigen = function () {
    var dunkel = wurzel.dataset.modus === 'dunkel';
    wandBilder();
    Array.prototype.forEach.call(knoepfe, function (k) { k.setAttribute('aria-pressed', dunkel ? 'true' : 'false'); });
  };
  Array.prototype.forEach.call(knoepfe, function (k) {
    k.addEventListener('click', function () {
      var neu = wurzel.dataset.modus === 'dunkel' ? 'hell' : 'dunkel';
      wurzel.dataset.modus = neu;
      try { localStorage.setItem('pfeiler-modus', neu); } catch (e) { /* ohne Speicher: gilt nur für diese Seite */ }
      modusZeigen();
    });
  });
  modusZeigen();

  /* Schriftgröße: drei Stufen, gemerkt im Browser */
  var stufen = ['normal', 'gross', 'sehr-gross'];
  var stufenText = { normal: 'Schrift: normal', gross: 'Schrift: groß', 'sehr-gross': 'Schrift: sehr groß' };
  var schriftKnoepfe = document.querySelectorAll('.schrift');
  var schriftZeigen = function () {
    var st = wurzel.dataset.schrift || 'normal';
    Array.prototype.forEach.call(document.querySelectorAll('.hilfe-stand'), function (el) { el.textContent = stufenText[st]; });
    Array.prototype.forEach.call(schriftKnoepfe, function (k) { k.setAttribute('aria-pressed', st === 'normal' ? 'false' : 'true'); });
  };
  Array.prototype.forEach.call(schriftKnoepfe, function (k) {
    k.addEventListener('click', function () {
      var i = stufen.indexOf(wurzel.dataset.schrift || 'normal');
      var neu = stufen[(i + 1) % stufen.length];
      wurzel.dataset.schrift = neu;
      try { localStorage.setItem('pfeiler-schrift', neu); } catch (e) { /* ohne Speicher: nur diese Seite */ }
      schriftZeigen();
      var h = k.closest('.hilfe');
      if (h) { h.classList.add('zeigt'); clearTimeout(h._t); h._t = setTimeout(function () { h.classList.remove('zeigt'); }, 1800); }
    });
  });
  schriftZeigen();

  /* Menü (Handy) */
  var menueKnopf = document.querySelector('.menue');
  var menueFlaeche = document.querySelector('.menue-flaeche');
  if (menueKnopf && menueFlaeche) {
    var schliesseMenue = function () { menueKnopf.setAttribute('aria-expanded', 'false'); menueFlaeche.classList.remove('offen'); };
    menueKnopf.addEventListener('click', function () {
      var offen = menueKnopf.getAttribute('aria-expanded') !== 'true';
      menueKnopf.setAttribute('aria-expanded', offen ? 'true' : 'false');
      menueFlaeche.classList.toggle('offen', offen);
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') schliesseMenue(); });
    menueFlaeche.addEventListener('click', function (e) { if (e.target.tagName === 'A') schliesseMenue(); });
  }

  /* Einblenden beim Scrollen */
  var zeig = document.querySelectorAll('.zeig');
  if (ruhig || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(zeig, function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    Array.prototype.forEach.call(zeig, function (el) { io.observe(el); });
  }

  /* Kopfzeile: beim Scrollen zur kompakten Pille zusammenfahren */
  var kopfEl = document.querySelector('.kopf');
  if (kopfEl) {
    var kompakt = false;
    var pruefeKompakt = function () {
      var y = window.scrollY || 0;
      if (!kompakt && y > 140) { kompakt = true; kopfEl.classList.add('kompakt'); }
      else if (kompakt && y < 40) { kompakt = false; kopfEl.classList.remove('kompakt'); if (menueFlaeche && window.innerWidth >= 860) { menueFlaeche.classList.remove('offen'); if (menueKnopf) menueKnopf.setAttribute('aria-expanded', 'false'); } }
    };
    window.addEventListener('scroll', pruefeKompakt, { passive: true });
    pruefeKompakt();
  }

  /* Kopfzeile: über der Wand hell, über Papier dunkel */
  var kopf = document.querySelector('.kopf');
  var waende = document.querySelectorAll('.wand');
  if (kopf && waende.length) {
    var pruefe = function () {
      var y = kopf.getBoundingClientRect().bottom - 10;
      var ueber = false;
      Array.prototype.forEach.call(waende, function (w) {
        var r = w.getBoundingClientRect();
        if (r.top <= y && r.bottom >= y) ueber = true;
      });
      kopf.classList.toggle('ueber-wand', ueber);
      if (menueFlaeche) menueFlaeche.classList.toggle('ueber-wand', ueber);
    };
    var tick = false;
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(function () { pruefe(); tick = false; }); } }, { passive: true });
    window.addEventListener('resize', pruefe);
    pruefe();
  }

  /* Bilder, die nicht ins Breitformat passen (quadratisch, hochkant): ganz zeigen,
     dahinter dasselbe Bild weich als Fond — nichts wird abgeschnitten. */
  Array.prototype.forEach.call(document.querySelectorAll('.schau-bild img, .rahmen img'), function (img) {
    var passe = function () {
      if (!img.naturalWidth || img.classList.contains('fond')) return;
      var box = img.parentElement.getBoundingClientRect();
      var bildV = img.naturalWidth / img.naturalHeight, boxV = box.width / Math.max(box.height, 1);
      if (bildV < boxV * 0.72) {
        img.parentElement.classList.add('passe');
        if (!img.parentElement.querySelector('.fond')) {
          var f = img.cloneNode(false); f.className = 'fond'; f.alt = ''; f.removeAttribute('loading');
          img.parentElement.insertBefore(f, img);
        }
      }
    };
    if (img.complete) passe(); else img.addEventListener('load', passe);
  });

  /* Slideshow */
  Array.prototype.forEach.call(document.querySelectorAll('.schau'), function (schau) {
    var bilder = [].slice.call(schau.querySelectorAll('.schau-bild'));
    var punkte = schau.querySelector('.schau-punkte');
    if (bilder.length < 2) return;
    var aktiv = 0, timer = null;
    var zeige = function (i) {
      aktiv = (i + bilder.length) % bilder.length;
      bilder.forEach(function (b, k) { b.classList.toggle('ist-aktiv', k === aktiv); });
      if (punkte) Array.prototype.forEach.call(punkte.children, function (p, k) { p.setAttribute('aria-selected', k === aktiv ? 'true' : 'false'); });
    };
    var starte = function () { if (ruhig) return; clearInterval(timer); timer = setInterval(function () { zeige(aktiv + 1); }, 8000); };
    if (punkte) bilder.forEach(function (b, k) {
      var p = document.createElement('button'); p.type = 'button'; p.setAttribute('role', 'tab'); p.setAttribute('aria-label', 'Bild ' + (k + 1));
      p.addEventListener('click', function () { zeige(k); starte(); });
      punkte.appendChild(p);
    });
    Array.prototype.forEach.call(schau.querySelectorAll('.schau-pfeil'), function (pf) {
      pf.addEventListener('click', function () { zeige(aktiv + (pf.classList.contains('links') ? -1 : 1)); starte(); });
    });
    schau.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { zeige(aktiv - 1); starte(); }
      if (e.key === 'ArrowRight') { zeige(aktiv + 1); starte(); }
    });
    zeige(0); starte();
    schau.addEventListener('pointerenter', function () { clearInterval(timer); });
    schau.addEventListener('pointerleave', starte);
  });

  /* Leistungsseite: aktiver Reiter folgt dem Scrollen */
  var reiter = document.querySelectorAll('.reiter a');
  var bereiche = document.querySelectorAll('.bereich');
  if (reiter.length && bereiche.length && 'IntersectionObserver' in window) {
    var io2 = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (!e.isIntersecting) return;
        Array.prototype.forEach.call(reiter, function (a) { a.classList.toggle('aktiv', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-40% 0px -50% 0px' });
    Array.prototype.forEach.call(bereiche, function (b) { io2.observe(b); });
  }
})();
