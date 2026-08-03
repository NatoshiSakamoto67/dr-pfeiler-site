# Privatpraxis Dr. med. Günter Pfeiler — Webseite

Statische Webseite, sechs Seiten, kein Build-Schritt, keine Abhängigkeiten.
Reines HTML, ein Stilblatt, eine kleine JavaScript-Datei.

**Status: Entwurf.** Noch nicht veröffentlicht. Was fehlt, steht in
[OFFENE-PUNKTE.md](OFFENE-PUNKTE.md) und ist auf den Seiten selbst als orange
gestrichelter Kasten sichtbar markiert.

## Öffnen

```bash
python3 -m http.server 8791 --bind 127.0.0.1 --directory ~/dr-pfeiler-site/web
```

Dann im Browser: <http://localhost:8791/>

Ein Doppelklick auf `index.html` funktioniert auch, aber über den Server ist es
näher am späteren Betrieb (Schriften und `defer`-Skript verhalten sich gleich).

## Aufbau

**`web/` ist die Veröffentlichungswurzel — und nur `web/`.** Die internen
Notizen liegen bewusst eine Ebene darüber. Damit sind sie nicht „beim Hochladen
auszulassen", sondern schlicht außerhalb dessen, was der Server überhaupt
erreichen kann. Der erste Entwurf hatte sie im selben Ordner; ein Prüflauf holte
`OFFENE-PUNKTE.md` mit HTTP 200 ab — samt der Anschrift, die noch ungeklärt ist.

```
dr-pfeiler-site/
├── OFFENE-PUNKTE.md    was noch fehlt und warum — NICHT ausliefern
├── README.md           diese Datei — NICHT ausliefern
└── web/                ← alles hierin wird veröffentlicht, nichts darüber
    ├── index.html          Startseite — Hero, Arbeitsweise, 7 Leistungsfelder,
    │                       Qualifikation, Ablauf, FAQ, Kontakt
    ├── leistungen.html     alle 7 Kategorien ungekürzt, mit Sprungmarken
    ├── praxis.html         Person, M-Arzt-Verfahren, Schwerpunkte, Diagnostik
    ├── kontakt.html        Anschrift, Sprechzeiten, Anfahrt, Notfallhinweise
    ├── impressum.html      § 5 DDG + berufsrechtliche Pflichtangaben
    ├── datenschutz.html    Art. 13 DSGVO
    └── assets/
        ├── css/site.css    das gesamte Design, mit Token oben
        ├── js/site.js      Einblendungen, Menü, Kopfzeile — ohne Framework
        └── fonts/          Fraunces + Manrope (SIL OFL 1.1), lokal, ~96 KB
```

## Gestaltung

**Haltung: Wucht im Bild, Zurückhaltung im Wort.** § 27 Abs. 3 der Berufsordnung
der Ärztekammer Niedersachsen verbietet anpreisende Werbung. Die Autorität muss
deshalb aus Typografie und Ruhe kommen, nicht aus Adjektiven — was ohnehin die
bessere Wirkung ist. Superlative lesen sich billig.

**Farben:** Petrol (`#0d4a52`) als einzige Farbe, dazu warme Grautöne. Kein
Gold — das ist ein Kosmetik- und Wellness-Signal; im medizinischen Premiumsegment
kommt es praktisch nicht vor. Der warme Grauton ist das eigentliche
Luxus-Merkmal, kaltes Weiß liest sich wie eine Vorlage.

**Schriften:** Fraunces (Display, variable Achsen `opsz`/`SOFT`/`WONK`) gegen
Manrope (Fließtext). Beide liegen lokal.

**Bewegung:** ausschließlich `transform` und `opacity` — nichts, was Layout
auslöst. Die Zeilen im Hero steigen aus ihrer eigenen Zeile auf (Maske), Haarlinien
wachsen per `scaleX`, und die EKG-Linie unter dem Hero zeichnet sich **einmal**
und ruht dann. Keine Dauerschleife.

`prefers-reduced-motion` liefert den **Endzustand**, nicht eine langsamere
Fassung und keine leere Seite.

**Ohne JavaScript bleibt alles lesbar und bedienbar.** Verborgen wird nur, was
die Klasse `.js` freigibt — die setzt ein winziges Skript im `<head>`, bevor
irgendetwas gezeichnet wird. Fällt das Skript aus, bleibt die Seite sichtbar
statt weiß. Dasselbe gilt für das Menü auf dem Handy: ohne JavaScript klappt es
nicht zu, sondern steht offen im Kopf. Ein Menü, das sich nur per Skript öffnen
lässt, ist ohne Skript kein Menü.

**Auf dem Handy liegt die Rufnummer als feste Leiste am unteren Rand.** Das
Telefon ist der einzige Weg in diese Praxis — bewusst, wegen Art. 9 DSGVO. Dann
darf er nicht hinter einem Menü liegen, das erst aufgeklappt werden muss.

## Datenschutz und Sicherheit

- **Null externe Verbindungen.** Keine CDN, keine Google Fonts, keine Karte,
  keine Analyse, keine sozialen Netzwerke.
- **Keine Cookies**, kein `localStorage`, kein Banner nötig.
- **Kein Kontaktformular.** Wer sein Anliegen schreibt, schreibt über seine
  Gesundheit — Art. 9 DSGVO. Telefon ist hier das sicherere Verfahren. Die FAQ
  erklärt das statt es zu verschweigen.
- **Kein Bild-Nachladen von fremden Servern.** Das Favicon steckt als
  SVG-Daten-URI im HTML.

## Server-Einstellungen

Die Seite braucht kein PHP, keine Datenbank und keinen Node-Prozess — aber ein
paar Kopfzeilen. Für nginx:

```nginx
root /var/www/dr-pfeiler-site/web;   # nur web/, niemals eine Ebene darüber
autoindex off;                        # keine Verzeichnisauflistung

add_header Content-Security-Policy "default-src 'none'; style-src 'self'; script-src 'self' 'sha256-pfgOMgfVZwm2ODyms34QYW9h8EwicylhV77q5LHK8c0='; font-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), interest-cohort=()" always;
```

`default-src 'none'` ist hier tragbar, weil die Seite nichts nachlädt — jede
zusätzliche Quelle in der Richtlinie wäre ein Hinweis darauf, dass sich doch
etwas Fremdes eingeschlichen hat.

Der Hash gehört zu genau einem Inline-Skript, das in allen sechs Seiten
identisch steht:

```html
<script>document.documentElement.className+=" js"</script>
```

Ändert sich dieses Skript auch nur um ein Leerzeichen, muss der Hash neu
gebildet werden, sonst blockiert der Browser es — und die Seite bliebe in der
Fassung ohne JavaScript stehen (lesbar, aber ohne Einblendungen):

```bash
printf '%s' 'document.documentElement.className+=" js"' | openssl dgst -sha256 -binary | openssl base64
```

## Vor dem Livegang

```bash
cd ~/dr-pfeiler-site/web

# 1. Entwurfs-Markierungen müssen weg sein — Ausgabe muss LEER sein
grep -rn 'class="todo' *.html

# 2. noindex entfernen — Ausgabe muss LEER sein
grep -rn 'noindex' *.html

# 3. Verbotene Begriffe — Ausgabe muss LEER sein.
#    Die Wortgrenze `\<` ist nötig: ohne sie schlägt „führend“ in
#    „irreführende Werbung“ an — ausgerechnet im Satz, der davor warnt.
grep -rniE '\<(fifa|d-arzt|durchgangsarzt|sportmediziner|führend)|centre of excellence|spezialist nr' *.html

# 4. Positivkontrollen — jede Zeile MUSS etwas finden.
#    Punkt 1 und 2 sind Negativproben: sie schlagen nur an, wenn etwas Falsches
#    dasteht. Fehlt dagegen etwas Pflichtiges, schweigen sie. Die drei
#    berufsrechtlichen Befunde dieser Seite trugen keine Markierung — die
#    Freigabeprüfung hätte sie strukturell nicht finden können.
grep -l 'Ärztekammer Niedersachsen' impressum.html   # Kammer + Berufsordnung
grep -l 'Berufshaftpflicht'          impressum.html   # § 5 Abs. 1 Nr. 5 DDG
grep -l 'Verliehen in'               impressum.html   # in welchem Staat verliehen
grep -l 'Berufsordnung'              impressum.html   # berufsrechtliche Regelungen
grep -rl 'datenschutz.html'          index.html       # Art. 13 von jeder Seite
grep -l 'ruf-bar'                    index.html       # Rufnummer auf dem Handy

# 5. Belegter Nachweis statt Augenschein
node ~/xdab-next/pfeiler-pruefung.mjs        # externe Anfragen, tote Links, ohne JS, Überlauf
node ~/xdab-next/kontrast-sweep.mjs --breite=375 http://127.0.0.1:8791/index.html
```

Die vollständige Liste steht in [OFFENE-PUNKTE.md](OFFENE-PUNKTE.md), Abschnitt D.

## Nicht auf diese Seite gehört

Festgehalten, damit es nicht versehentlich doch hineinrutscht:

- **FIFA** in jeder Form — solange die Bewerbbarkeit nicht geklärt ist
- „Facharzt für Sportmedizin“ oder „Sportmedizin“ allein — geschützte
  Zusatzbezeichnung
- „VBG-Sportarzt“, „von der VBG zertifiziert“, „Durchgangsarzt“, „D-Arzt“
- „Medical Centre of Excellence“
- Erfahrungsberichte und Bewertungen — § 11 Abs. 1 Nr. 11 HWG
- Superlative jeder Art — § 27 Abs. 3 BO
