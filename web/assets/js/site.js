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

  /* ---- Einblenden beim Scrollen ---- */
  var zuBeobachten = document.querySelectorAll('.reveal, .rule, .pulse, .kicker');

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

  /* ---- Kopfzeile bekommt eine Kante, sobald gescrollt wurde ---- */
  var kopf = document.querySelector('.site-head');
  if (kopf) {
    var setzeKante = function () {
      kopf.classList.toggle('stuck', window.scrollY > 8);
    };
    setzeKante();
    window.addEventListener('scroll', setzeKante, { passive: true });
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
})();
