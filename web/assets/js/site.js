/* =============================================================================
 *  Privatpraxis Dr. med. Günter Pfeiler — Verhalten
 *
 *  Bewusst klein und ohne Abhängigkeiten: kein Framework, kein CDN, keine
 *  externe Anfrage. Bewegt wird ausschließlich `transform` und `opacity`.
 *  Wer `prefers-reduced-motion` gesetzt hat, sieht sofort den Endzustand.
 * ========================================================================== */
(function () {
  'use strict';

  var wenigerBewegung = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Hell / Dunkel: ein Knopf, gemerkt im Browser ---- */
  (function () {
    var wurzel = document.documentElement;
    var knoepfe = document.querySelectorAll('.modus-knopf');
    var zeige = function () {
      var dunkel = wurzel.dataset.modus === 'dunkel';
      Array.prototype.forEach.call(knoepfe, function (k) { k.setAttribute('aria-pressed', dunkel ? 'true' : 'false'); });
    };
    Array.prototype.forEach.call(knoepfe, function (k) {
      k.addEventListener('click', function () {
        var neu = wurzel.dataset.modus === 'dunkel' ? 'hell' : 'dunkel';
        wurzel.dataset.modus = neu;
        try { localStorage.setItem('pfeiler-modus', neu); } catch (e) { /* privater Modus: dann eben nur für diese Seite */ }
        zeige();
      });
    });
    zeige();
  })();

  /* ---- Hero: Zeilen steigen erst auf, wenn die Schrift wirklich da ist ----
     Ohne das Warten springt der Text beim Schriftwechsel — der Ruck fällt
     ausgerechnet in der ersten Sekunde auf. */
  function heroFreigeben() {
    document.documentElement.classList.add('loaded');
  }
  if (wenigerBewegung) {
    heroFreigeben();
  } else if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(heroFreigeben);
    setTimeout(heroFreigeben, 600); // Rückfallebene: lieber ein Schriftwechsel als eine leere Überschrift
  } else {
    requestAnimationFrame(heroFreigeben);
  }

  /* ---- Alle Zeichnungs-Animationen um den Faktor 2.6 verlangsamen -----
     Statt jede Keyframe-Dauer im Stilblatt anzufassen: gemessene Dauer und
     Verzögerung jedes animierten Elements werden per Inline-Stil gestreckt.
     Verhältnisse bleiben, die Szene läuft nur gemächlicher. */
  var FAKTOR = 2.6;
  var strecke = function (wert) {
    return wert.split(',').map(function (v) {
      v = v.trim(); if (!v || v === '0s') return v;
      var ms = /ms$/.test(v); var z = parseFloat(v);
      return isNaN(z) ? v : (z * FAKTOR) + (ms ? 'ms' : 's');
    }).join(', ');
  };
  Array.prototype.forEach.call(document.querySelectorAll('.mark, .mark *'), function (el) {
    var cs = getComputedStyle(el);
    if (cs.animationName && cs.animationName !== 'none') {
      el.style.animationDuration = strecke(cs.animationDuration);
      el.style.animationDelay = strecke(cs.animationDelay);
    }
  });

  /* ---- Slideshow: langsamer Wechsel, Punkte zum Anwählen ---- */
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
    var weiter = function () { zeige(aktiv + 1); };
    var starte = function () { if (wenigerBewegung) return; clearInterval(timer); timer = setInterval(weiter, 8000); };
    if (punkte) bilder.forEach(function (b, k) {
      var p = document.createElement('button'); p.type = 'button'; p.setAttribute('role', 'tab');
      p.setAttribute('aria-label', 'Bild ' + (k + 1));
      p.addEventListener('click', function () { zeige(k); starte(); });
      punkte.appendChild(p);
    });
    zeige(0); starte();
    schau.addEventListener('mouseenter', function () { clearInterval(timer); });
    schau.addEventListener('mouseleave', starte);
  });

  /* ---- Einblenden beim Scrollen ---- */
  var zuBeobachten = document.querySelectorAll('.reveal, .rule, .pulse, .kicker, .mark, .lageplan');

  if (wenigerBewegung || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(zuBeobachten, function (el) { el.classList.add('in'); });
  } else {
    var beobachter = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in');
        beobachter.unobserve(e.target); // einmal einblenden, dann Ruhe
      });
    }, { threshold: 0.16, rootMargin: '0px 0px -5% 0px' });

    Array.prototype.forEach.call(zuBeobachten, function (el) {
      if (!el.classList.contains('in')) beobachter.observe(el);
    });
  }

  /* ---- Kopfzeile und Rufknopf: Kante und Farbseite -------------------------
     Zwei Dinge hängen an derselben Scrollposition, deshalb ein Handler.

     1. Die Kopfleiste bekommt eine Kante, sobald gescrollt wurde.
     2. Beide Glasflächen drehen die Farben um, sobald ein dunkler Abschnitt
        hinter ihnen liegt. Nötig, weil die Scheiben absichtlich sehr dünn
        getönt sind: dunkle Tinte auf durchscheinendem Petrol wäre nicht mehr
        lesbar. Statt die Scheibe wieder dicker zu machen — was den Glaseffekt
        kostet — wechselt sie über solchen Abschnitten die Seite.

     Gemessen wird gegen die tatsächlichen Kästen, nicht mit einem
     IntersectionObserver: der kennt nur „berührt sich", gebraucht wird aber
     „liegt überwiegend dahinter". Ein Streifen von wenigen Pixeln am Rand
     eines Abschnitts darf die Leiste nicht umschalten lassen. */
  var kopf = document.querySelector('.site-head');
  var pille = document.querySelector('.ruf-bar');
  var dunkleAbschnitte = [].slice.call(document.querySelectorAll('.sec-deep'));

  if (kopf || pille) {
    // Ab welchem Anteil der Scheibenhöhe der dunkle Grund die Oberhand hat.
    var SCHWELLE = 0.55;

    var liegtAufDunklem = function (el) {
      if (!el) return false;
      var k = el.getBoundingClientRect();
      if (k.height <= 0) return false; // ausgeblendet, z.B. Rufknopf am Schreibtisch
      var deckung = 0;
      for (var i = 0; i < dunkleAbschnitte.length; i++) {
        var a = dunkleAbschnitte[i].getBoundingClientRect();
        var ueberlappung = Math.min(k.bottom, a.bottom) - Math.max(k.top, a.top);
        if (ueberlappung > 0) deckung += ueberlappung;
      }
      return deckung / k.height >= SCHWELLE;
    };

    var angefordert = false;
    var pruefe = function () {
      angefordert = false;
      if (kopf) {
        kopf.classList.toggle('stuck', window.scrollY > 8);
        kopf.classList.toggle('site-head--dunkel', liegtAufDunklem(kopf));
      }
      if (pille) pille.classList.toggle('ruf-bar--dunkel', liegtAufDunklem(pille));
    };
    // Beim Scrollen fällt der Handler oft an; gerechnet wird trotzdem nur
    // einmal je Bild — sonst misst er Kästen, die der Browser gleich neu legt.
    var anstossen = function () {
      if (angefordert) return;
      angefordert = true;
      requestAnimationFrame(pruefe);
    };

    pruefe();
    window.addEventListener('scroll', anstossen, { passive: true });
    window.addEventListener('resize', anstossen, { passive: true });
    // Ein aufgeklapptes Menü macht die Leiste höher — damit steht plötzlich
    // ein anderer Abschnitt dahinter.
    window.addEventListener('click', anstossen, { passive: true });
  }

  /* ---- Menü auf kleinen Fenstern ---- */
  var schalter = document.querySelector('.nav-toggle');
  var menue = document.getElementById('hauptmenue');
  if (schalter && menue) {
    schalter.addEventListener('click', function () {
      var offen = menue.classList.toggle('offen');
      schalter.setAttribute('aria-expanded', offen ? 'true' : 'false');
      schalter.textContent = offen ? 'Schließen' : 'Menü';
    });
    // Nach einem Sprung im Dokument schließen — sonst verdeckt das Menü das Ziel.
    menue.addEventListener('click', function (e) {
      if (e.target.tagName !== 'A' || !menue.classList.contains('offen')) return;
      menue.classList.remove('offen');
      schalter.setAttribute('aria-expanded', 'false');
      schalter.textContent = 'Menü';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !menue.classList.contains('offen')) return;
      menue.classList.remove('offen');
      schalter.setAttribute('aria-expanded', 'false');
      schalter.textContent = 'Menü';
      schalter.focus();
    });
  }

  /* ---- Reiter (Leistungen) --------------------------------------------------
     Im HTML steht eine gewöhnliche Sprungmarken-Liste über sieben Abschnitten.
     Ohne JavaScript ist das eine funktionierende Seite: alle sieben Themen
     sichtbar, jeder Link springt zu seinem Abschnitt. Erst hier werden daraus
     Reiter — und nur dann, wenn wirklich jedes Sprungziel existiert. Ein
     halbverdrahteter Reiter, der Inhalte versteckt, die kein Knopf mehr
     zurückholt, wäre schlimmer als gar keiner. */
  var reiter = document.querySelector('.reiter');
  if (reiter) {
    var leiste = reiter.querySelector('.reiter-leiste');
    var knoepfe = leiste ? [].slice.call(leiste.querySelectorAll('a[href^="#"]')) : [];
    var tafeln = knoepfe.map(function (a) {
      return document.getElementById(a.getAttribute('href').slice(1));
    });

    if (knoepfe.length > 1 && tafeln.every(Boolean)) {
      leiste.setAttribute('role', 'tablist');
      leiste.setAttribute('aria-label', 'Schwerpunkte');

      knoepfe.forEach(function (knopf, i) {
        var tafel = tafeln[i];
        if (!knopf.id) knopf.id = 'reiter-knopf-' + (i + 1);
        knopf.setAttribute('role', 'tab');
        knopf.setAttribute('aria-controls', tafel.id);
        tafel.setAttribute('role', 'tabpanel');
        tafel.setAttribute('aria-labelledby', knopf.id);
        tafel.setAttribute('tabindex', '0'); // die Tafel selbst ist scrollbar, also fokussierbar
      });

      var aktiv = -1;

      var zeige = function (ziel, fokus) {
        if (ziel === aktiv) return;
        aktiv = ziel;
        knoepfe.forEach(function (knopf, i) {
          var an = i === ziel;
          knopf.setAttribute('aria-selected', an ? 'true' : 'false');
          knopf.setAttribute('tabindex', an ? '0' : '-1'); // rovendes tabindex: ein Tabstopp für die ganze Leiste
          tafeln[i].hidden = !an;
          tafeln[i].classList.toggle('frisch', an);
          // Ein Reiterwechsel zeigt das Feld wieder ganz — mit Kopf. Wer
          // eine Leistung direkt ansteuert, setzt die Klasse danach neu.
          tafeln[i].classList.remove('ohne-intro');
        });
        // Zeichnungen in einer bisher verborgenen Tafel hat der Beobachter nie
        // gesehen — sonst bliebe die Linie ungezeichnet stehen.
        Array.prototype.forEach.call(tafeln[ziel].querySelectorAll('.mark'), function (m) {
          m.classList.add('in');
        });
        if (fokus) knoepfe[ziel].focus();
      };

      knoepfe.forEach(function (knopf, i) {
        knopf.addEventListener('click', function (e) {
          e.preventDefault();
          // Auch beim Klick auf den bereits offenen Reiter kommt der Kopf
          // zurück — `zeige` kehrt dann früh um und räumte ihn nicht auf.
          tafeln[i].classList.remove('ohne-intro');
          zeige(i, false);
          // Adresszeile mitführen, damit ein Reiter teilbar bleibt — ohne Sprung.
          if (window.history && window.history.replaceState) {
            window.history.replaceState(null, '', knopf.getAttribute('href'));
          }
          // Wer im alten Reiter nach unten gescrollt war, stünde im neuen
          // sonst mitten in fremdem Inhalt — jeder Reiter beginnt oben.
          reiter.scrollIntoView({ block: 'start', behavior: wenigerBewegung ? 'auto' : 'smooth' });
        });
      });

      leiste.addEventListener('keydown', function (e) {
        var i = knoepfe.indexOf(document.activeElement);
        if (i < 0) return;
        var ziel = null;
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') ziel = (i - 1 + knoepfe.length) % knoepfe.length;
        else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') ziel = (i + 1) % knoepfe.length;
        else if (e.key === 'Home') ziel = 0;
        else if (e.key === 'End') ziel = knoepfe.length - 1;
        if (ziel === null) return;
        e.preventDefault();
        zeige(ziel, true);
      });

      // Einstieg aus der Adresszeile: wer einen Link auf ein Thema bekommt,
      // landet auf diesem Reiter. Der Link kann auch auf eine einzelne
      // Leistung tiefer zeigen — dann gehört der Reiter geöffnet, in dem
      // sie liegt; den Unter-Reiter wählt danach dessen eigene Verdrahtung.
      var ausHash = knoepfe.findIndex(function (knopf) {
        return knopf.getAttribute('href') === window.location.hash;
      });
      if (ausHash < 0 && window.location.hash.length > 1) {
        var hashZiel = document.getElementById(window.location.hash.slice(1));
        while (hashZiel && tafeln.indexOf(hashZiel) < 0) hashZiel = hashZiel.parentElement;
        if (hashZiel) ausHash = tafeln.indexOf(hashZiel);
      }
      zeige(ausHash > -1 ? ausHash : 0, false);
      if (ausHash > -1) reiter.scrollIntoView({ block: 'start' });

      // Griffe für die Schwebe-Vorschau weiter unten.
      reiter._zeige = zeige;
      reiter._knoepfe = knoepfe;
      reiter._tafeln = tafeln;
    }
  }

  /* ---- Leistungs-Karten: alle Leistungen eines Feldes liegen offen als Karten.
     Die Griffe (_zeige/_tafeln/_direkt) bleiben für Suche und Schwebe-Vorschau:
     „zeigen“ heißt hier: Karte aufklappen und hinscrollen. */
  var unterReiter = [].slice.call(document.querySelectorAll('.u-reiter'));
  unterReiter.forEach(function (bereich) {
    var uTafeln = [].slice.call(bereich.querySelectorAll('.u-tafel'));
    if (!uTafeln.length) return;
    var tafelDrumherum = bereich.closest ? bereich.closest('.reiter-tafel') : null;
    var ziel = null;
    bereich._tafeln = uTafeln;
    bereich._zeige = function (j) {
      ziel = uTafeln[j];
      uTafeln.forEach(function (t, k) {
        var d = t.querySelector('details');
        if (d) d.open = (k === j);
        t.classList.toggle('frisch', k === j);
      });
    };
    bereich._direkt = function () {
      if (tafelDrumherum) tafelDrumherum.classList.add('ohne-intro');
      (ziel || bereich).scrollIntoView({ block: 'start', behavior: wenigerBewegung ? 'auto' : 'smooth' });
    };
    // Deep-Link auf eine Leistung: Karte offen, Feld-Kopf weg.
    var hashZiel = window.location.hash && document.getElementById(window.location.hash.slice(1));
    var idx = uTafeln.indexOf(hashZiel);
    if (idx > -1) { bereich._zeige(idx); bereich._direkt(); }
  });

  /* ---- Schwebe-Vorschau über den Reitern -----------------------------------
     Nur an Geräten mit echtem Zeiger: beim Zeigen auf einen Reiter klappt
     die Liste seiner Leistungen auf, ein Klick darauf öffnet Feld und
     Leistung in einem Schritt. Am Finger gibt es kein Zeigen — dort bleibt
     der Reiter ein gewöhnlicher Reiter. */
  var reiterEl = document.querySelector('.reiter');
  var zeigerFein = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (reiterEl && reiterEl._zeige && zeigerFein) {
    var schwebe = document.createElement('div');
    schwebe.className = 'reiter-schwebe';
    document.body.appendChild(schwebe);

    var offenFuer = -1;
    var zuTimer = null;

    var schliesse = function () {
      offenFuer = -1;
      schwebe.classList.remove('offen');
    };
    var haltOffen = function () {
      if (zuTimer) { clearTimeout(zuTimer); zuTimer = null; }
    };
    var bald = function () {
      haltOffen();
      zuTimer = setTimeout(schliesse, 140);
    };

    var oeffneFuer = function (i) {
      var bereich = reiterEl._tafeln[i].querySelector('.u-reiter');
      if (!bereich || !bereich._tafeln || offenFuer === i) return;
      offenFuer = i;
      schwebe.textContent = '';
      var titel = document.createElement('b');
      titel.textContent = reiterEl._knoepfe[i].textContent.replace(/^\d+\s*/, '');
      schwebe.appendChild(titel);
      bereich._tafeln.forEach(function (uTafel, j) {
        var a = document.createElement('a');
        a.href = '#' + uTafel.id;
        var h3 = uTafel.querySelector('h3');
        a.textContent = h3 ? h3.textContent : uTafel.id;
        a.addEventListener('click', function (e) {
          e.preventDefault();
          reiterEl._zeige(i, false);
          bereich._zeige(j, false);
          if (window.history && window.history.replaceState) {
            window.history.replaceState(null, '', '#' + uTafel.id);
          }
          schliesse();
          // Direkter Sprung in eine Leistung: ohne Feld-Kopf, die Leistung oben.
          if (bereich._direkt) bereich._direkt();
          else reiterEl.scrollIntoView({ block: 'start', behavior: wenigerBewegung ? 'auto' : 'smooth' });
        });
        schwebe.appendChild(a);
      });
      // `position:fixed` rechnet im selben Koordinatensystem wie die
      // gemessenen Kästen — die Leiste klebt, also stimmt die Lage.
      var k = reiterEl._knoepfe[i].getBoundingClientRect();
      schwebe.style.left = Math.max(8, Math.min(k.left, window.innerWidth - schwebe.offsetWidth - 12)) + 'px';
      schwebe.style.top = (k.bottom + 4) + 'px';
      schwebe.classList.add('offen');
    };

    reiterEl._knoepfe.forEach(function (knopf, i) {
      var zeigen = function () { haltOffen(); oeffneFuer(i); };
      knopf.addEventListener('mouseenter', zeigen);
      knopf.addEventListener('focus', zeigen);
      knopf.addEventListener('mouseleave', bald);
      knopf.addEventListener('blur', bald);
      knopf.addEventListener('click', schliesse);
    });
    schwebe.addEventListener('mouseenter', haltOffen);
    schwebe.addEventListener('mouseleave', bald);
    // Beim Scrollen stimmt die gemessene Position nicht mehr — dann zu.
    window.addEventListener('scroll', schliesse, { passive: true });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') schliesse();
    });
  }

  /* ---- Leistungs-Suche ------------------------------------------------------
     Der Index entsteht aus dem Katalog selbst: auf der Leistungsseite aus dem
     DOM, überall sonst per einmaligem fetch von leistungen.html — so kann die
     Suche nie veralten. Treffer springen als tiefe Links in den richtigen
     Reiter; auf der Leistungsseite ohne Neuladen über die Reiter-Griffe. */
  [].slice.call(document.querySelectorAll('.suche')).forEach(function (form) {
    var feld = form.querySelector('.suche-feld');
    var liste = form.querySelector('.suche-liste');
    if (!feld || !liste) return;
    var hiesig = !!document.querySelector('.reiter'); // auf der Leistungsseite?
    var index = null, laden = null, aktiv = -1, sichtbar = [];

    var falte = function (t) {
      return t.toLowerCase().replace(/ß/g, 'ss')
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    };

    var baueIndex = function (doc) {
      var arr = [];
      [].forEach.call(doc.querySelectorAll('.reiter-tafel'), function (tafel) {
        var h2 = tafel.querySelector('h2');
        var feldName = h2 ? h2.textContent.replace(/^\s*\d+\s*/, '').trim() : '';
        if (tafel.id) arr.push({ id: tafel.id, titel: feldName, wo: 'Schwerpunkt', text: '' });
        [].forEach.call(tafel.querySelectorAll('.u-tafel'), function (u) {
          var h3 = u.querySelector('h3');
          if (!u.id || !h3) return;
          var teaser = u.querySelector('.u-teaser');
          arr.push({
            id: u.id, titel: h3.textContent.trim(), wo: feldName,
            text: falte(teaser ? teaser.textContent : '')
          });
        });
      });
      arr.forEach(function (e) { e.such = falte(e.titel); });
      return arr;
    };

    var holeIndex = function () {
      if (index) return Promise.resolve(index);
      if (!laden) {
        laden = (hiesig
          ? Promise.resolve(baueIndex(document))
          : fetch('leistungen.html')
              .then(function (r) { return r.text(); })
              .then(function (html) { return baueIndex(new DOMParser().parseFromString(html, 'text/html')); })
        ).then(function (arr) { index = arr; return arr; });
      }
      return laden;
    };

    var zu = function () {
      liste.hidden = true;
      liste.textContent = '';
      feld.setAttribute('aria-expanded', 'false');
      aktiv = -1; sichtbar = [];
    };

    // Auf der Leistungsseite ohne Neuladen: Reiter und Unterreiter über die
    // vorhandenen Griffe schalten — derselbe Weg wie die Schwebe-Vorschau.
    var springeZu = function (id) {
      var reiterEl = document.querySelector('.reiter');
      var ziel = document.getElementById(id);
      if (!reiterEl || !reiterEl._zeige || !ziel) { window.location.href = 'leistungen.html#' + id; return; }
      var tafel = ziel;
      while (tafel && reiterEl._tafeln.indexOf(tafel) < 0) tafel = tafel.parentElement;
      if (!tafel) return;
      reiterEl._zeige(reiterEl._tafeln.indexOf(tafel), false);
      var bereich = tafel.querySelector('.u-reiter');
      var j = (ziel !== tafel && bereich && bereich._tafeln) ? bereich._tafeln.indexOf(ziel) : -1;
      if (j > -1 && bereich._zeige) {
        bereich._zeige(j, false);
        if (bereich._direkt) bereich._direkt();
      } else {
        reiterEl.scrollIntoView({ block: 'start', behavior: wenigerBewegung ? 'auto' : 'smooth' });
      }
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, '', '#' + id);
      }
    };

    var zeige = function (treffer) {
      liste.textContent = '';
      aktiv = -1; sichtbar = treffer;
      if (!treffer.length) {
        var leer = document.createElement('li');
        leer.className = 'leer';
        leer.textContent = 'Keine Leistung gefunden.';
        liste.appendChild(leer);
      }
      treffer.forEach(function (e, i) {
        var li = document.createElement('li');
        li.id = 'suche-treffer-' + i;
        li.setAttribute('role', 'option');
        var a = document.createElement('a');
        a.href = 'leistungen.html#' + e.id;
        a.textContent = e.titel;
        var wo = document.createElement('span');
        wo.className = 'wo';
        wo.textContent = e.wo;
        a.appendChild(wo);
        a.addEventListener('mousedown', function (ev) { ev.preventDefault(); }); // blur nicht vor dem Klick
        a.addEventListener('click', function (ev) {
          if (!hiesig) return; // gewöhnlicher Link mit tiefem Ziel
          ev.preventDefault();
          zu(); feld.blur();
          springeZu(e.id);
        });
        li.appendChild(a);
        liste.appendChild(li);
      });
      liste.hidden = false;
      feld.setAttribute('aria-expanded', 'true');
    };

    var suche = function () {
      var q = falte(feld.value.trim());
      if (q.length < 2) { zu(); return; }
      holeIndex().then(function (arr) {
        var treffer = arr.map(function (e) {
          var rang = e.such.indexOf(q) === 0 ? 0
                   : e.such.indexOf(q) > -1 ? 1
                   : e.text.indexOf(q) > -1 ? 2 : -1;
          return { e: e, rang: rang };
        }).filter(function (t) { return t.rang > -1; });
        treffer.sort(function (a, b) { return a.rang - b.rang; });
        zeige(treffer.slice(0, 8).map(function (t) { return t.e; }));
      });
    };

    var markiere = function () {
      [].forEach.call(liste.children, function (li, i) {
        li.classList.toggle('aktiv', i === aktiv);
      });
      feld.setAttribute('aria-activedescendant', aktiv > -1 ? 'suche-treffer-' + aktiv : '');
    };

    feld.addEventListener('input', suche);
    feld.addEventListener('focus', function () { holeIndex(); if (feld.value.trim().length > 1) suche(); });
    feld.addEventListener('keydown', function (e) {
      if (liste.hidden) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); aktiv = Math.min(aktiv + 1, sichtbar.length - 1); markiere(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); aktiv = Math.max(aktiv - 1, 0); markiere(); }
      else if (e.key === 'Enter') {
        if (aktiv < 0 && sichtbar.length) aktiv = 0;
        if (aktiv > -1 && sichtbar[aktiv]) {
          e.preventDefault();
          var ziel = sichtbar[aktiv];
          if (hiesig) { zu(); feld.blur(); springeZu(ziel.id); }
          else window.location.href = 'leistungen.html#' + ziel.id;
        }
      }
      else if (e.key === 'Escape') { zu(); }
    });
    feld.addEventListener('blur', function () { setTimeout(zu, 120); });
    form.addEventListener('submit', function (e) { e.preventDefault(); });
  });

})();
