#!/usr/bin/env python3
"""Erzeugt die sieben Seiten im Stil „Edel“, Fassung 2 (26.09.2026, nach Recherche).

Kopf, Menü, untere Leiste und Fuß stehen hier genau einmal und in derselben Reihenfolge
(WCAG 3.2.6). Impressum und Datenschutz behalten ihren <main>-Inhalt aus der Datei.
"""
import pathlib, re

WEB = pathlib.Path.home() / 'dr-pfeiler-site' / 'web'
V = '29'
TEL, TEL_HREF = '0160 5728656', 'tel:+491605728656'
MAIL = 'praxis@dr-pfeiler.de'
LAT, LON = '52.27784', '10.52268'
ROUTE_G = f'https://www.google.com/maps/dir/?api=1&amp;destination={LAT}%2C{LON}&amp;travelmode=driving'
ROUTE_A = 'https://maps.apple.com/?daddr=Hamburger+Stra%C3%9Fe+277%2C+38114+Braunschweig&amp;dirflg=d'
EMBED = f'https://www.google.com/maps/embed?origin=mfe&amp;pb=!1m3!2m1!1s{LAT},{LON}!6i17!3m1!1sde!5m1!1sde'
SEITEN = [('index', 'Start'), ('leistungen', 'Leistungen'), ('praxis', 'Praxis'), ('kontakt', 'Kontakt')]
RECHT = [('impressum', 'Impressum'), ('datenschutz', 'Datenschutz'), ('barrierefreiheit', 'Barrierefreiheit')]

ICON = {
    'pfeil': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16m-6-6 6 6-6 6"/></svg>',
    'tel': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>',
    'route': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-6-5.3-6-11a6 6 0 0 1 12 0c0 5.7-6 11-6 11Z"/><circle cx="12" cy="10" r="2.2"/></svg>',
    'haken': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.5 2.5 4.5-5"/></svg>',
}
PFEIL = ICON['pfeil']

# Signet: Mittelkreis mit Anstoßpunkt und Mittellinie (20 Jahre Profifußball)
def signet(klasse='signet'):
    return (f'<svg class="{klasse}" viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
            '<circle cx="20" cy="20" r="13" fill="none" stroke="currentColor" stroke-width="1.6"/>'
            '<path d="M20 2v36" stroke="currentColor" stroke-width="1.6"/>'
            '<circle cx="20" cy="20" r="2.4" fill="currentColor"/></svg>')

# Spielfeld-Linien auf der Ottocento-Wand, je Abschnitt ein anderes Stück
FELD = {
    'mitte': ('<svg class="feld feld--mitte" viewBox="0 0 400 800" aria-hidden="true" focusable="false">'
              '<path pathLength="1" d="M200 0V800"/><circle pathLength="1" cx="200" cy="400" r="150"/>'
              '<circle class="punkt" cx="200" cy="400" r="5"/></svg>'),
    'strafraum': ('<svg class="feld feld--strafraum" viewBox="0 0 800 420" aria-hidden="true" focusable="false">'
                  '<path pathLength="1" d="M0 420H800"/><path pathLength="1" d="M140 420V170H660V420"/>'
                  '<path pathLength="1" d="M290 420V330H510V420"/><path pathLength="1" d="M300 170A140 140 0 0 1 500 170"/>'
                  '<circle class="punkt" cx="400" cy="250" r="5"/></svg>'),
    'ecke': ('<svg class="feld feld--ecke" viewBox="0 0 400 400" aria-hidden="true" focusable="false">'
             '<path pathLength="1" d="M0 0H400"/><path pathLength="1" d="M400 0V400"/>'
             '<path pathLength="1" d="M345 0A55 55 0 0 0 400 55"/><path pathLength="1" d="M60 0V120H400"/></svg>'),
}

JSONLD = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Physician","@id":"https://dr-pfeiler.de/#praxis","name":"Privatpraxis Dr. med. Günter Pfeiler",
 "medicalSpecialty":["SportsMedicine","PrimaryCare"],
 "address":{{"@type":"PostalAddress","streetAddress":"Hamburger Straße 277","postalCode":"38114","addressLocality":"Braunschweig","addressCountry":"DE"}},
 "geo":{{"@type":"GeoCoordinates","latitude":{LAT},"longitude":{LON}}},
 "telephone":"+49 160 5728656","email":"{MAIL}","url":"https://dr-pfeiler.de/","isAccessibleForFree":false,
 "founder":{{"@type":"Person","name":"Dr. med. Günter Pfeiler","honorificPrefix":"Dr. med.","jobTitle":"Facharzt für Allgemeinmedizin"}}}}
</script>'''


def todo(text):
    return f'<details class="todo"><summary>Intern</summary><p>{text}</p></details>'


def rahmen(datei, titel, beschreibung, inhalt, auf_bild=False, extra_kopf=''):
    def nav():
        return '\n'.join('<a href="%s.html"%s>%s</a>' % (n, ' aria-current="page"' if n == datei else '', t) for n, t in SEITEN)
    def rechtnav():
        return '\n'.join('<a href="%s.html"%s>%s</a>' % (n, ' aria-current="page"' if n == datei else '', t) for n, t in RECHT)
    preload = '<link rel="preload" as="image" href="assets/img/leistung-sport-reha.webp" fetchpriority="high">\n' if auf_bild else ''
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titel}</title>
<meta name="description" content="{beschreibung}">
<meta name="robots" content="noindex, nofollow"><!-- ENTWURF: vor dem Livegang entfernen -->
<meta name="theme-color" content="#f5f1ea">
<link rel="preload" href="assets/fonts/source-serif-4.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="assets/css/edel.css?v={V}">
<script>document.documentElement.className+=" js";try{{if(localStorage.getItem("pfeiler-gross")==="1")document.documentElement.classList.add("gross")}}catch(e){{}}</script>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%231d2124'/%3E%3Ctext x='16' y='22' font-family='Georgia,serif' font-size='17' fill='%23f5f1ea' text-anchor='middle'%3EP%3C/text%3E%3C/svg%3E">
{extra_kopf}</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>

<header class="kopf{' kopf--auf-bild' if auf_bild else ''}">
  <div class="wrap">
    <a class="marke" href="index.html"><span class="marke-text"><span class="titel-kurz">Dr. med. </span>Günter Pfeiler<small>Privatpraxis · Braunschweig</small></span></a>
    <nav class="nav" aria-label="Hauptmenü">
{nav()}
<a class="nav-tel" href="{TEL_HREF}">{TEL}</a>
    </nav>
    <a class="kopf-tel" href="{TEL_HREF}" aria-label="Anrufen: {TEL}">{ICON['tel']}</a>
    <button class="menue" type="button" aria-expanded="false" aria-controls="menue">Menü <i aria-hidden="true"></i></button>
  </div>
</header>
<nav class="menue-flaeche" id="menue" aria-label="Menü">
{nav()}
<a class="menue-tel" href="{TEL_HREF}">{ICON['tel']} Termin: {TEL}</a>
  <div class="menue-fuss">
    <button class="schrift" type="button" aria-pressed="false"><span class="a1" aria-hidden="true">A</span><span class="a2" aria-hidden="true">A</span> Große Schrift</button>
{rechtnav()}
  </div>
</nav>

<main id="inhalt" tabindex="-1">
{inhalt}
</main>

<footer class="fuss" data-ruf-ende>
  <div class="wrap">
    <p class="gross">Privatpraxis<br>Dr. med. Günter Pfeiler</p>
    <div class="fuss-raster">
      <div><small>Praxis</small><address>Hamburger Straße 277<br>38114 Braunschweig<br>Erdgeschoss, barrierefrei</address></div>
      <div><small>Termine</small><a href="{TEL_HREF}">{TEL}</a><br>nach Vereinbarung<br><a href="mailto:{MAIL}">{MAIL}</a></div>
      <div><small>Seiten</small><nav aria-label="Fußzeile">
{nav()}
{rechtnav()}
      </nav></div>
    </div>
    <div class="zeile">
      <span>© 2026 Privatpraxis Dr. med. Günter Pfeiler</span>
      <span>Keine Cookies. Behandlungsszenen sind mit KI erzeugte Symbolbilder.</span>
    </div>
  </div>
</footer>

<nav class="ruf" aria-label="Schnellkontakt">
  <a class="primaer" href="{TEL_HREF}">{ICON['tel']} Anrufen</a>
  <a href="{ROUTE_G}" target="_blank" rel="noopener noreferrer">{ICON['route']} Route <span class="sr-only">(öffnet Google Maps)</span></a>
</nav>

<script src="assets/js/edel.js?v={V}" defer></script>
</body>
</html>
'''


def bild(datei, alt, nr, klasse='bild--breit', laden='lazy', symbol=True, w=1536, h=1024):
    unter = '<figcaption class="bildunterschrift"><span class="symbol">Symbolbild</span></figcaption>' if symbol else ''
    return (f'<figure class="bild-spalte"><div class="bild {klasse}"><img src="assets/img/{datei}.webp" width="{w}" height="{h}" '
            f'loading="{laden}" decoding="async" alt="{alt}"><span class="bild-nr" aria-hidden="true">{nr}</span></div>{unter}</figure>')


# ---------------------------------------------------------------- Bausteine
LEISTUNGEN = [
    ('sportmedizin', 'Sportmedizin', 'Untersuchen, behandeln, vorbeugen. Ultraschall in der Praxis.'),
    ('leistungsdiagnostik', 'Leistungsdiagnostik', 'Laktat-Stufentest, Belastungs-EKG, Herzultraschall.'),
    ('sport-reha', 'Sport-Reha', 'Vor und nach der Operation, bis zur Sportfreigabe.'),
    ('arthrosetherapie', 'Arthrosetherapie', 'Stoßwelle, Hyaluronsäure, Eigenblut.'),
    ('allgemeinmedizin', 'Allgemein- und Reisemedizin', 'Check-up, Impfberatung, Tauglichkeit.'),
]


def liste():
    zeilen = ''.join(f'<li><a class="zeig" style="--dl:{i*60}ms" href="leistungen.html#{a}"><span class="nr">0{i+1}</span>'
                     f'<h3>{t}</h3><p>{s}</p>{PFEIL}</a></li>' for i, (a, t, s) in enumerate(LEISTUNGEN))
    return f'<ul class="liste">{zeilen}</ul>'


VERTRAUEN = f'''
  <div class="band-vertrauen" aria-label="Auf einen Blick">
    <ul class="wrap">
      <li>{ICON['haken']}<div><b>Facharzt für Allgemeinmedizin</b>Sportmedizin, Leistungsdiagnostik, Reisemedizin</div></li>
      <li>{ICON['haken']}<div><b>20 Jahre Mannschaftsarzt</b>VfL Wolfsburg, 1998 bis 2018, seitdem beratend</div></li>
      <li>{ICON['haken']}<div><b>Erdgeschoss, barrierefrei</b>Hamburger Straße 277, Parkplatz mit Parkscheibe direkt am Haus</div></li>
    </ul>
  </div>'''

SITUATIONEN = f'''
  <section class="nacht abschnitt" aria-labelledby="situation-t">
    {FELD['mitte']}
    <div class="wrap">
      <p class="kicker zeig">Womit kommen Sie?</p>
      <h2 id="situation-t" class="zeig" style="--dl:80ms">Vier Wege in die Praxis.</h2>
      <ul class="situationen situationen--glas">
        <li><a class="zeig" href="leistungen.html#sportmedizin"><h3>Frisch verletzt</h3><p>Umgeknickt, Muskel gezerrt, Knie verdreht. Kurzfristiger Termin, Untersuchung und Ultraschall am selben Tag.</p><span>Sportmedizin {PFEIL}</span></a></li>
        <li><a class="zeig" style="--dl:60ms" href="leistungen.html#arthrosetherapie"><h3>Schmerzen, die bleiben</h3><p>Arthrose, gereizte Sehnen, Fersensporn. Stoßwelle, Hyaluronsäure oder Eigenblut, sachlich beraten.</p><span>Arthrosetherapie {PFEIL}</span></a></li>
        <li><a class="zeig" style="--dl:120ms" href="leistungen.html#leistungsdiagnostik"><h3>Leistung messen</h3><p>Laktat-Stufentest, Belastungs-EKG, Herzultraschall. Aus den Werten ein Trainingsplan.</p><span>Leistungsdiagnostik {PFEIL}</span></a></li>
        <li><a class="zeig" style="--dl:180ms" href="leistungen.html#sport-reha"><h3>Vor oder nach der OP</h3><p>Zweite Meinung vor dem Eingriff, Nachsorge und Kontrollen bis zur Sportfreigabe. Auch bei Operationen in anderen Häusern.</p><span>Sport-Reha {PFEIL}</span></a></li>
      </ul>
      <div class="aktionen zeig"><a class="link" href="leistungen.html">Alle Leistungen {PFEIL}</a></div>
    </div>
  </section>'''

CHRONIK = f'''
  <section class="nacht abschnitt" aria-labelledby="chronik-titel">
    {FELD['strafraum']}
    <div class="wrap">
      <p class="kicker zeig">Woher ich komme</p>
      <h2 id="chronik-titel" class="zeig" style="--dl:80ms;max-width:12em">Zwanzig Jahre Profifußball.</h2>
      <div class="chronik">
        <div class="zeig">
          <p class="lead">Von 1998 bis 2018 Mannschaftsarzt des VfL Wolfsburg, seitdem beratend. Mannschaftsarzt (M-Arzt) im Verfahren der VBG, der gesetzlichen Unfallversicherung des Profisports.</p>
          <div class="glas" style="margin-top:2rem;padding-block:.3rem"><ol class="zeitleiste">
            <li><b>1998</b><span>Beginn als Mannschaftsarzt des VfL Wolfsburg</span></li>
            <li><b>2009</b><span>Deutsche Meisterschaft</span></li>
            <li><b>2015</b><span>DFB-Pokalsieg</span></li>
            <li><b>2018</b><span>Seitdem beratend; eigene Privatpraxis in Braunschweig</span></li>
          </ol></div>
          {todo('Jahreszahlen und Vereinsnennung mit Dr. Pfeiler bestätigen. Bildrechte (Fotograf, Verein) und Einwilligung der abgebildeten Spieler klären.')}
        </div>
        <div class="archiv zeig" style="--dl:120ms">
          <figure class="bild a1"><img src="assets/img/foto-01-spielfeldrand.webp" width="1536" height="1024" loading="lazy" alt="Dr. Pfeiler untersucht am Spielfeldrand die Schulter eines Spielers"><figcaption>Am Spielfeldrand</figcaption><span class="bild-nr" aria-hidden="true">27</span></figure>
          <figure class="bild a2"><img src="assets/img/foto-02-dfb-pokal.webp" width="1536" height="1536" loading="lazy" alt="Dr. Pfeiler mit dem DFB-Pokal"><figcaption>DFB-Pokal 2015</figcaption><span class="bild-nr" aria-hidden="true">28</span></figure>
        </div>
      </div>
    </div>
  </section>'''

ERSTER_TERMIN = f'''
  <section class="abschnitt" aria-labelledby="termin-titel">
    <div class="wrap">
      <div class="zweispalt">
        <p class="kicker zeig">Ihr erster Termin</p>
        <h2 id="termin-titel" class="zeig" style="--dl:80ms">So läuft es ab.</h2>
      </div>
      <ol class="schritte">
        <li class="zeig"><h3>Anrufen</h3><p>Sie rufen an und schildern kurz, worum es geht. Bei einer frischen Verletzung sagen Sie das gleich; dann gibt es kurzfristig einen Termin.</p></li>
        <li class="zeig" style="--dl:80ms"><h3>Untersuchung</h3><p>Gespräch, körperliche Untersuchung und, wenn nötig, Ultraschall in der Praxis. Bringen Sie alte Befunde und Bilder mit.</p></li>
        <li class="zeig" style="--dl:160ms"><h3>Plan</h3><p>Sie gehen mit einem klaren Befund und einem Plan nach Hause: Behandlung, Belastung, nächster Kontrolltermin.</p></li>
      </ol>
      <div class="kosten zeig" id="kosten">
        <div><p class="kicker">Kosten</p><h3 style="margin-top:.8rem">Privatpraxis, offen gerechnet.</h3></div>
        <div>
          <p>Abgerechnet wird nach der Gebührenordnung für Ärzte (GOÄ).</p>
          <ul>
            <li>Privatversicherte und Beihilfeberechtigte reichen die Rechnung bei ihrer Versicherung oder Beihilfestelle ein.</li>
            <li>Gesetzlich Versicherte sind als Selbstzahler willkommen. Fragen Sie vorher bei Ihrer Kasse nach, was sie übernimmt.</li>
            <li>Stoßwelle, Hyaluronsäure und Eigenblut sind Selbstzahlerleistungen. Die Kosten werden vorher schriftlich vereinbart.</li>
          </ul>
          {todo('Abrechnungsangaben (GOÄ-Faktor, Erstattung, Beihilfe, Preisrahmen Erstgespräch) vor dem Livegang mit dem Arzt klären. Keine Praxis in Braunschweig nennt Kosten; ein Preisrahmen wäre ein Alleinstellungsmerkmal.')}
        </div>
      </div>
    </div>
  </section>'''

NOTFALL = '<p class="notfall"><b>Im Notfall:</b> Rettungsdienst <a href="tel:112">112</a>. Außerhalb der Sprechzeiten: ärztlicher Bereitschaftsdienst <a href="tel:116117">116 117</a>.</p>'

KARTE = f'''<figure class="karte zeig">
          <div class="bild" id="karte-bild">
            <img src="assets/img/lageplan.webp" width="1600" height="1200" loading="lazy" decoding="async" alt="Stadtplan Braunschweig-Nordstadt: die Praxis liegt an der Hamburger Straße 277 am Ringgleis, nahe Haltestelle Ludwigstraße">
            <span class="bild-nr" aria-hidden="true">58</span>
            <div class="karte-laden">
              <button class="knopf" type="button" id="karte-laden" data-src="{EMBED}">{ICON['route']} Google-Karte anzeigen</button>
              <p>Dabei werden Daten an Google übermittelt. <a href="datenschutz.html#google-maps">Datenschutz</a></p>
            </div>
          </div>
          <figcaption><span>Hamburger Straße 277, Nordstadt</span><span>Karte: © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap-Mitwirkende</a></span></figcaption>
          <p class="sr-only" aria-live="polite" id="karte-status"></p>
        </figure>'''

ROUTEN_GROSS = f'''<p class="kicker">Route mit einem Klick</p><p style="margin-top:.6rem">Öffnet die Navigation direkt in Ihrer Karten-App.</p><div class="wege-knoepfe"><a class="knopf" href="{ROUTE_G}" target="_blank" rel="noopener noreferrer">{ICON['route']} Route in Google Maps</a><a class="knopf knopf--glas" href="{ROUTE_A}" target="_blank" rel="noopener noreferrer" hidden data-apple>Route in Apple Karten</a></div>'''
ROUTEN = f'''<div class="wege-knoepfe"><a class="knopf" href="{ROUTE_G}" target="_blank" rel="noopener noreferrer">{ICON['route']} Route in Google Maps</a><a class="knopf knopf--glas" href="{ROUTE_A}" target="_blank" rel="noopener noreferrer" hidden data-apple>Route in Apple Karten</a></div>'''

WEGE = f'''<dl class="punkte">
            <div><dt>Mit dem Auto</dt><dd>Im ehemaligen Verlagshaus der Braunschweiger Zeitung. Parken direkt am Haus auf dem Parkplatz, den sich die Praxis mit dem Edeka teilt; bitte Parkscheibe auslegen. Von der A 391 über die Abfahrt Hamburger Straße stadteinwärts.</dd></div>
            <div><dt>Mit Bahn und Rad</dt><dd>Stadtbahn Linie 1 oder 2 bis zur Haltestelle Ludwigstraße, von dort wenige Minuten zu Fuß. Der Ringgleis-Radweg führt am Gebäude vorbei.</dd></div>
            <div><dt>Zugang</dt><dd>Die Praxis liegt im Erdgeschoss und ist barrierefrei erreichbar, ohne Stufen und ohne Aufzug.</dd></div>
          </dl>'''

# ---------------------------------------------------------------- Start
INDEX = f'''
  <section class="titel">
    <img src="assets/img/leistung-sport-reha.webp" width="1536" height="1024" alt="" fetchpriority="high"><span class="bild-nr" aria-hidden="true">10</span>
    <div class="wrap">
      <h1 id="titel">Privatpraxis<br>für <em>Sportmedizin</em></h1>
      <div class="aktionen">
        <a class="knopf knopf--hell" href="{TEL_HREF}">{ICON['tel']} {TEL}</a>
        <a class="knopf knopf--rand-hell" href="leistungen.html">Leistungen</a>
      </div>
    </div>
  </section>
{VERTRAUEN}

  <section class="abschnitt" aria-labelledby="praxis-titel">
    <div class="wrap zweispalt">
      <p class="kicker zeig" id="praxis-titel">Die Praxis</p>
      <div>
        <p class="aussage zeig">Zwanzig Jahre habe ich Profis nach Verletzungen zurück auf den Platz gebracht. Heute nehme ich mir diese Zeit für <em>Sie</em>, ob Sie Marathon laufen, Tennis spielen oder einfach schmerzfrei gehen wollen.</p>
        <div class="aktionen zeig" style="--dl:160ms"><a class="link" href="praxis.html">Zur Person {PFEIL}</a></div>
      </div>
    </div>
  </section>
{SITUATIONEN}

{CHRONIK}

  <section class="abschnitt" aria-labelledby="person-titel">
    <div class="wrap person">
      <figure class="zeig" style="margin:0">
        <div class="bild bild--hoch"><img src="assets/img/foto-03-meisterschale.webp" width="1024" height="1536" loading="lazy" decoding="async" alt="Dr. med. Günter Pfeiler mit der Meisterschale in der Arena des VfL Wolfsburg"><span class="bild-nr" aria-hidden="true">4</span></div>
        <figcaption class="bildunterschrift"><span class="symbol">Archivfoto</span></figcaption>
      </figure>
      <div class="zeig" style="--dl:120ms">
        <p class="kicker">Zur Person</p>
        <h2 id="person-titel">Dr. med. Günter Pfeiler</h2>
        <dl class="fakten">
          <div><dt>Facharzt</dt><dd>Allgemeinmedizin</dd></div>
          <div><dt>1998 – 2018</dt><dd>Mannschaftsarzt VfL Wolfsburg, seitdem beratend</dd></div>
          <div><dt>Verfahren</dt><dd>Mannschaftsarzt (M-Arzt) der VBG</dd></div>
          <div><dt>Praxis</dt><dd>Hamburger Straße 277, Braunschweig</dd></div>
        </dl>
        {todo('Porträt ist vorläufig das Archivfoto. Für den Livegang ein aktuelles Foto im Sprechzimmer machen lassen; alle 40 recherchierten Vorbilder nutzen eigene Fotografie.')}
      </div>
    </div>
  </section>
{ERSTER_TERMIN}

  <section class="nacht abschnitt" aria-labelledby="kontakt-titel" data-ruf-ende>
    {FELD['ecke']}
    <div class="wrap">
      <div class="kontaktblock">
        <div class="zeig">
          <p class="kicker">Kontakt</p>
          <h2 id="kontakt-titel">Rufen Sie an.</h2>
          <a class="tel" href="{TEL_HREF}">{TEL}</a>
          {NOTFALL}
        </div>
        <div class="glas zeig" style="--dl:120ms">
          <dl class="angaben">
            <div><dt>Praxis</dt><dd><address class="adresse">Hamburger Straße 277<br>38114 Braunschweig</address></dd></div>
            <div><dt>Termine</dt><dd>Nach Vereinbarung</dd></div>
            <div><dt>Anfahrt</dt><dd>Parkplatz direkt am Haus, mit Parkscheibe. Stadtbahn 1 und 2, Haltestelle Ludwigstraße.</dd></div>
            <div><dt>Zugang</dt><dd>Erdgeschoss, barrierefrei</dd></div>
          </dl>
          <div class="aktionen" style="margin-top:1.2rem"><a class="knopf" href="{ROUTE_G}" target="_blank" rel="noopener noreferrer">{ICON['route']} Route</a><a class="link" href="kontakt.html">Anfahrt und Sprechzeiten {PFEIL}</a></div>
        </div>
      </div>
      <div style="margin-top:2rem">{KARTE}</div>
    </div>
  </section>'''

# ---------------------------------------------------------------- Leistungen
BEREICHE = [
    ('sportmedizin', 'Sportmedizin', 'Diagnostik, Behandlung und Vorbeugung von Sportverletzungen. Klinische Untersuchung und Ultraschall in der Praxis.',
     ('leistung-sportmedizin', 'Dr. Pfeiler tastet die Achillessehne eines Läufers ab', 5),
     [('Diagnostik', 'Klinische Untersuchung und Ultraschall von Muskeln, Sehnen und Gelenken.'),
      ('Behandlung', 'Konservative Behandlung nach Stufenplan bis zur vollen Belastung.'),
      ('Vorbeugung', 'Screening von Kraft, Beweglichkeit und Seitenunterschieden. Übungsprogramm.')], ''),
    ('leistungsdiagnostik', 'Leistungsdiagnostik', 'Laktat-Stufentest, Belastungs-EKG, Herzultraschall. Aus den Werten ein Trainingsplan.',
     None,
     [('Laktat-Test', 'Stufentest mit Laktatmessung. Trainingsbereiche für Puls, Tempo, Watt.'),
      ('Belastungs-EKG', 'Ergometrie mit EKG und Blutdruck unter steigender Belastung.'),
      ('Herzultraschall', 'Ultraschall des Herzens: Kammern, Klappen, Pumpfunktion.'),
      ('Trainingsplan', 'Trainingsbereiche und Wochenstruktur aus der Diagnostik. Kontrolltermine.')],
     'Noch zu klären: welche Untersuchungen in der Praxis selbst stattfinden und welche in Kooperation.'),
    ('sport-reha', 'Sport-Reha', 'Beratung vor der Operation, Nachsorge und Kontrollen bis zur Sportfreigabe. Auch bei Eingriffen in anderen Häusern.',
     None,
     [('Vor und nach der OP', 'Befund und Bildgebung vor dem Eingriff, Nachbehandlungsplan danach.'),
      ('Zweite Meinung', 'Einschätzung, ob eine Operation nötig ist oder eine konservative Behandlung ausreicht.'),
      ('Kontrollen', 'Verlaufskontrollen mit Messwerten bis zur Sportfreigabe.')], ''),
    ('arthrosetherapie', 'Arthrosetherapie', 'Stoßwelle, Hyaluronsäure und Eigenblut bei Arthrose und Sehnenreizungen. Selbstzahlerleistungen, Kosten vorab schriftlich.',
     None,
     [('Stoßwelle', 'Extrakorporale Stoßwellentherapie bei Fersensporn, Kalkschulter, Tennisarm.'),
      ('Hyaluronsäure', 'Injektion in das Gelenk, einmalig oder als Serie.'),
      ('Eigenblut (ACP)', 'Plättchenreiches Plasma aus Eigenblut, Injektion in Gelenk oder Sehne.')],
     'Selbstzahlerleistungen; Kosten werden vorher schriftlich vereinbart. Evidenzhinweise (S3-Leitlinie) gehören ins Aufklärungsgespräch, nicht auf die Seite.'),
    ('allgemeinmedizin', 'Allgemein- und Reisemedizin', 'Check-up, reisemedizinische Beratung und Impfungen, Tauglichkeitsuntersuchungen für Tauchen und Fallschirmsprung.',
     None,
     [('Check-up', 'Anamnese, körperliche Untersuchung, Labor, EKG, Ultraschall.'),
      ('Reisemedizin', 'Impfberatung, Malariaprophylaxe, Reiseapotheke. Termin 6 bis 8 Wochen vor Abreise.'),
      ('Tauch- und Sprungtauglichkeit', 'Untersuchung und Bescheinigung für Tauchkurs und Fallschirmsprung.')],
     'Abrechnungsangaben (GOÄ, Erstattung, Beihilfe) vor dem Livegang mit dem Arzt klären; die Redaktionstexte nannten teils Kassenleistungen.'),
]


def bereich(i, a, t, lead, b, punkte, hinweis):
    pk = ''.join(f'<div><dt>{x}</dt><dd>{y}</dd></div>' for x, y in punkte)
    return f'''
  <section class="bereich" id="{a}" aria-labelledby="{a}-t">
    <div class="wrap">
      <div class="bereich-kopf zeig"><span class="nr" aria-hidden="true">0{i+1}</span><div><h2 id="{a}-t">{t}</h2><p class="lead" style="margin-top:1rem">{lead}</p></div></div>
      <div class="bereich-raster">
        {'<div class="zeig">' + bild(b[0], b[1] + ' (Symbolbild)', b[2]) + '</div>' if b else ''}
        <div class="zeig" style="--dl:100ms"><dl class="punkte">{pk}</dl>{todo(hinweis) if hinweis else ''}</div>
      </div>
    </div>
  </section>'''


SPRUNG = ''.join(f'<a href="#{a}"><i>0{i+1}</i>{t.replace("Allgemein- und Reisemedizin", "Allgemein &amp; Reise")}</a>' for i, (a, t, *_r) in enumerate(BEREICHE))
AUFRUF = f'''
  <section class="nacht abschnitt aufruf" aria-labelledby="aufruf-t" data-ruf-ende>
    {FELD['mitte']}
    <div class="wrap zweispalt">
      <p class="kicker zeig">Nächster Schritt</p>
      <div class="zeig" style="--dl:80ms">
        <h2 id="aufruf-t">Termin telefonisch.</h2>
        <a class="tel" href="{TEL_HREF}">{TEL}</a>
        <div class="aktionen"><a class="link" href="kontakt.html">Anfahrt und Sprechzeiten {PFEIL}</a><a class="link" href="index.html#kosten">Kosten {PFEIL}</a></div>
        {NOTFALL}
      </div>
    </div>
  </section>'''

LEISTUNGEN_SEITE = f'''
  <section class="seitenkopf">
    <div class="wrap">
      <p class="kicker zeig">Leistungen</p>
      <h1 class="zeig" style="--dl:60ms">Fünf Bereiche, ein Arzt.</h1>
      <p class="lead zeig" style="--dl:120ms">Von der frischen Verletzung bis zum Reise-Check. Untersucht, erklärt und behandelt von Dr. Pfeiler selbst.</p>
    </div>
  </section>
  <nav class="sprung" aria-label="Bereiche"><div class="wrap">{SPRUNG}</div></nav>
{''.join(bereich(i, *b) for i, b in enumerate(BEREICHE))}
{AUFRUF}'''

# ---------------------------------------------------------------- Praxis
PRAXIS = f'''
  <section class="seitenkopf">
    <div class="wrap person">
      <div>
        <p class="kicker zeig">Praxis</p>
        <h1 class="zeig" style="--dl:60ms">Dr. med. Günter Pfeiler</h1>
        <p class="lead zeig" style="--dl:120ms">Facharzt für Allgemeinmedizin. 1998 bis 2018 Mannschaftsarzt des VfL Wolfsburg, seitdem beratend. Privatpraxis für Sportverletzungen, Leistungsdiagnostik und Reisemedizin in Braunschweig.</p>
        {todo('Zu bestätigen: Facharztbezeichnung, VfL-Zeitraum 1998–2018 (seitdem beratend), frühere Oberarzt-Tätigkeit am HEH Braunschweig. Quellen öffentlich, nicht vom Arzt bestätigt. Porträt vorläufig Archivfoto.')}
      </div>
      <figure class="zeig" style="--dl:160ms;margin:0">
        <div class="bild bild--hoch"><img src="assets/img/foto-03-meisterschale.webp" width="1024" height="1536" loading="eager" alt="Dr. med. Günter Pfeiler mit der Meisterschale in der Arena des VfL Wolfsburg"><span class="bild-nr" aria-hidden="true">4</span></div>
        <figcaption class="bildunterschrift"><span class="symbol">Archivfoto</span></figcaption>
      </figure>
    </div>
  </section>


    <p class="bildunterschrift"><span>Ultraschall am Sprunggelenk</span><span class="symbol">Symbolbild</span></p>
  </div>
{CHRONIK}

  <section class="abschnitt" aria-labelledby="schwer-t" data-ruf-ende>
    <div class="wrap zweispalt">
      <p class="kicker zeig">Schwerpunkte</p>
      <div>
        <h2 id="schwer-t" class="zeig">Worauf ich mich konzentriere.</h2>
        <dl class="fakten zeig" style="--dl:100ms">
          <div><dt>01</dt><dd>Sportverletzungen und Sporttraumatologie</dd></div>
          <div><dt>02</dt><dd>Leistungsdiagnostik</dd></div>
          <div><dt>03</dt><dd>Allgemein- und Reisemedizin</dd></div>
        </dl>
        <p class="gedaempft zeig" style="margin-top:1.2rem;font-size:var(--t-klein)">„M-Arzt“ ist eine Beteiligung im Verfahren der VBG, keine Facharzt- oder Zusatzbezeichnung.</p>
        <div class="aktionen zeig"><a class="knopf" href="{TEL_HREF}">{ICON['tel']} {TEL}</a><a class="link" href="kontakt.html">Anfahrt und Sprechzeiten {PFEIL}</a></div>
      </div>
    </div>
  </section>'''

# ---------------------------------------------------------------- Kontakt
KONTAKT = f'''
  <section class="seitenkopf">
    <div class="wrap kontaktblock">
      <div>
        <p class="kicker zeig">Kontakt</p>
        <h1 class="zeig" style="--dl:60ms">Ein Anruf genügt.</h1>
        <p class="lead zeig" style="--dl:120ms">Termine telefonisch. Frische Verletzungen kurzfristig.</p>
        <a class="tel zeig" style="--dl:160ms" href="{TEL_HREF}">{TEL}</a>
      </div>
      <dl class="angaben zeig" style="--dl:160ms;align-self:end">
        <div><dt>Praxis</dt><dd><address class="adresse">Privatpraxis Dr. med. Günter Pfeiler<br>Hamburger Straße 277<br>38114 Braunschweig</address></dd></div>
        <div><dt>Termine</dt><dd>Nach Vereinbarung</dd></div>
        <div><dt>E-Mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a><br><span class="gedaempft" style="font-size:var(--t-klein)">Für Terminanfragen bitte anrufen. Keine Befunde per E-Mail.</span></dd></div>
      </dl>
    </div>
  </section>

  <section class="nacht abschnitt" id="anfahrt" aria-labelledby="anfahrt-t">
    {FELD['ecke']}
    <div class="wrap">
      <p class="kicker zeig">Anfahrt</p>
      <h2 id="anfahrt-t" class="zeig">So finden Sie hin.</h2>
      {KARTE}
      <div class="anfahrt">
        <div class="glas zeig" style="--dl:120ms">
          {ROUTEN_GROSS}
        </div>
        <div class="glas zeig" style="--dl:180ms">
          {WEGE}
          {todo('Haltestelle (Ludwigstraße, Linie 1 und 2), Erdgeschoss und Barrierefreiheit von David am 26.09. bestätigt. Karte: fest eingebettetes OSM-Bild; Google-Karte nur nach Klick (Zwei-Klick). Google-Unternehmensprofil zeigt noch Steinweg 20, muss von Dr. Pfeiler auf Hamburger Straße 277 umgezogen werden. Foto vom Praxiseingang fehlt.')}
        </div>
      </div>
    </div>
  </section>

  <section class="abschnitt" aria-labelledby="zeiten-t">
    <div class="wrap kontaktblock">
      <div class="zeig">
        <p class="kicker">Sprechzeiten</p>
        <h2 id="zeiten-t">Wann ich da bin.</h2>
        <table class="zeiten">
          <tbody>
            <tr><th scope="row">Montag</th><td>noch offen</td></tr>
            <tr><th scope="row">Dienstag</th><td>noch offen</td></tr>
            <tr><th scope="row">Mittwoch</th><td>noch offen</td></tr>
            <tr><th scope="row">Donnerstag</th><td>noch offen</td></tr>
            <tr><th scope="row">Freitag</th><td>noch offen</td></tr>
          </tbody>
        </table>
        {NOTFALL}
        {todo('Sprechzeiten eintragen. Anschrift und E-Mail sind per Visitenkarte bestätigt.')}
      </div>
      <div class="zeig" style="--dl:120ms">
        <p class="kicker">Termin</p>
        <h2>Telefonisch.</h2>
        <p class="lead" style="margin-top:1rem">Frische Verletzungen bekommen kurzfristig einen Termin. Sagen Sie es gleich am Telefon.</p>
        <div class="aktionen"><a class="knopf" href="{TEL_HREF}">{ICON['tel']} {TEL} anrufen</a></div>
      </div>
    </div>
  </section>

  <section class="abschnitt" style="padding-top:0" aria-labelledby="fragen-t" data-ruf-ende>
    <div class="wrap kontaktblock">
      <div class="zeig"><p class="kicker">Häufige Fragen</p><h2 id="fragen-t">Was oft gefragt wird.</h2></div>
      <div class="fragen zeig" style="--dl:120ms">
        <details><summary>Ist das eine Privatpraxis?</summary><p>Ja. Ich rechne nach der Gebührenordnung für Ärzte ab. Privatversicherte reichen die Rechnung bei ihrer Versicherung ein, gesetzlich Versicherte zahlen selbst. Fragen Sie vorher bei Ihrer Kasse nach, was sie übernimmt.</p></details>
        <details><summary>Brauche ich eine Überweisung?</summary><p>Nein. Sie können direkt anrufen und einen Termin vereinbaren.</p></details>
        <details><summary>Wie bekomme ich einen Termin?</summary><p>Rufen Sie an. Wenn es eine frische Verletzung ist, sagen Sie das gleich, dann finde ich kurzfristig einen Termin.</p></details>
        <details><summary>Was soll ich mitbringen?</summary><p>Alte Befunde und Bilder, Ihre Medikamente, bei Reisen den Impfpass. Für Belastungstests Sportzeug.</p></details>
        <details><summary>Ist die Praxis barrierefrei?</summary><p>Ja. Die Praxis liegt im Erdgeschoss, ohne Stufen. Geparkt wird direkt am Haus, mit Parkscheibe.</p></details>
      </div>
    </div>
  </section>'''

# ---------------------------------------------------------------- Barrierefreiheit
BARRIEREFREIHEIT = '''
  <section class="seitenkopf">
    <div class="wrap text">
      <p class="kicker">Rechtliches</p>
      <h1>Barrierefreiheit</h1>
      <p class="lead">Diese Seite soll für alle gut nutzbar sein, auch mit Tastatur, Bildschirmleser oder großer Schrift. Hier steht, was wir dafür tun und wo noch Grenzen sind.</p>
    </div>
  </section>
  <section class="abschnitt abschnitt--klein">
    <div class="wrap text">
      <div class="sachtext">
        <h2>Anspruch</h2>
        <p>Die Seite ist nach den Web Content Accessibility Guidelines (WCAG) 2.2, Stufe AA, gebaut. Als reine Informationsseite ohne Online-Terminbuchung fällt sie nicht unter das Barrierefreiheitsstärkungsgesetz (BFSG); wir halten die Anforderungen freiwillig ein.</p>
        <h2>Was umgesetzt ist</h2>
        <ul>
          <li>Alle Funktionen sind mit der Tastatur erreichbar; der Fokus ist immer sichtbar und wird nicht von Kopf- oder Fußleiste verdeckt.</li>
          <li>Fließtext in 18 Pixel mit hohem Kontrast; im Menü lässt sich „Große Schrift“ einschalten. Die Seite lässt sich bis 400 Prozent vergrößern.</li>
          <li>Alle Schaltflächen sind mindestens 44 Pixel groß.</li>
          <li>Bilder haben Textalternativen; Behandlungsszenen sind als Symbolbilder gekennzeichnet.</li>
          <li>Bewegungen werden abgeschaltet, wenn das Betriebssystem „Bewegung reduzieren“ meldet.</li>
          <li>Kontakt und Telefon stehen auf jeder Seite an derselben Stelle.</li>
        </ul>
        <h2>Bekannte Grenzen</h2>
        <ul>
          <li>Die optionale Google-Karte ist ein Angebot von Google; ihre Bedienung können wir nicht beeinflussen. Adresse, Wegbeschreibung und Routenlinks stehen deshalb immer als Text daneben.</li>
          <li>Die Archivfotos vom VfL Wolfsburg tragen kurze Beschreibungen, keine ausführlichen Bildbeschreibungen.</li>
        </ul>
        <h2>Die Praxis selbst</h2>
        <p>Die Praxis liegt im Erdgeschoss und ist ohne Stufen erreichbar. Der Parkplatz liegt direkt am Haus.</p>
        <h2>Rückmeldung</h2>
        <p>Wenn Ihnen etwas auffällt, das nicht barrierefrei ist, schreiben Sie an <a href="mailto:praxis@dr-pfeiler.de">praxis@dr-pfeiler.de</a> oder rufen Sie an: <a href="tel:+491605728656">0160 5728656</a>. Wir bessern nach.</p>
        <h2>Stand</h2>
        <p>Diese Erklärung wurde am 26. September 2026 erstellt.</p>
      </div>
    </div>
  </section>'''


def rechtstext(datei):
    alt = (WEB / f'{datei}.html').read_text(encoding='utf-8')
    main = re.search(r'<main id="inhalt"[^>]*>(.*?)</main>', alt, re.S).group(1)
    main = re.sub(r'<h1><span class="line"><span class="line-in">(.*?)</span></span></h1>', r'<h1>\1</h1>', main)
    main = re.sub(r'<h1>\s*<span class="line"><span class="line-in">(.*?)</span></span>\s*</h1>', r'<h1>\1</h1>', main, flags=re.S)
    main = main.replace('style="padding-top:calc(6.5rem + env(safe-area-inset-top))"', 'class="seitenkopf"', 1)
    main = main.replace('<section style="padding-top:0">', '<section class="abschnitt abschnitt--klein">', 1)
    main = main.replace('class="lead zeig" style="--dl:300ms"', 'class="lead"')
    return main


def main():
    impressum, datenschutz = rechtstext('impressum'), rechtstext('datenschutz')
    ausgabe = {
        'index': rahmen('index', 'Dr. med. Günter Pfeiler — Privatpraxis für Sportmedizin, Braunschweig',
                        'Privatpraxis für Sportmedizin, Leistungsdiagnostik und Allgemeinmedizin in Braunschweig. Dr. med. Günter Pfeiler, zwanzig Jahre Mannschaftsarzt im Profifußball.',
                        INDEX, auf_bild=True, extra_kopf=JSONLD + '\n'),
        'leistungen': rahmen('leistungen', 'Leistungen — Dr. med. Günter Pfeiler, Braunschweig',
                             'Sportmedizin, Leistungsdiagnostik, Sport-Reha, Arthrosetherapie, Allgemein- und Reisemedizin.', LEISTUNGEN_SEITE),
        'praxis': rahmen('praxis', 'Praxis — Dr. med. Günter Pfeiler, Braunschweig',
                         'Dr. med. Günter Pfeiler: Facharzt für Allgemeinmedizin, 1998 bis 2018 Mannschaftsarzt des VfL Wolfsburg.', PRAXIS),
        'kontakt': rahmen('kontakt', 'Kontakt und Anfahrt — Dr. med. Günter Pfeiler, Braunschweig',
                          'Termine telefonisch unter 0160 5728656. Hamburger Straße 277, 38114 Braunschweig, Erdgeschoss, barrierefrei.', KONTAKT),
        'impressum': rahmen('impressum', 'Impressum — Dr. med. Günter Pfeiler', 'Impressum der Privatpraxis Dr. med. Günter Pfeiler.', impressum),
        'datenschutz': rahmen('datenschutz', 'Datenschutz — Dr. med. Günter Pfeiler', 'Datenschutzerklärung der Privatpraxis Dr. med. Günter Pfeiler.', datenschutz),
        'barrierefreiheit': rahmen('barrierefreiheit', 'Barrierefreiheit — Dr. med. Günter Pfeiler', 'Erklärung zur Barrierefreiheit der Website der Privatpraxis Dr. med. Günter Pfeiler.', BARRIEREFREIHEIT),
    }
    for name, html in ausgabe.items():
        (WEB / f'{name}.html').write_text(html, encoding='utf-8')
        print('geschrieben:', name, len(html))


if __name__ == '__main__':
    main()
