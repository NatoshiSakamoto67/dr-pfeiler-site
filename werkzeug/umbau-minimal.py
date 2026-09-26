import re, pathlib
W=pathlib.Path('/Users/davidoff/dr-pfeiler-site/web')
def rd(n): return (W/n).read_text()
def wr(n,s): (W/n).write_text(s)

# ============================================================ leistungen.html
s=rd('leistungen.html')
behalten = {'sportmedizin':['sv-diagnostik','sv-therapie','sv-prophylaxe'],
            'leistungsdiagnostik':['laktattest','belastungs-ekg','echo','trainingssteuerung'],
            'sport-reha':['op-beratung','kontrolluntersuchungen'],
            'arthrosetherapie':['eswt','hyaluron','acp'],
            'allgemeinmedizin':['checkup','reiseplanung','tauchtauglichkeit']}
arts={m.group(1):m.group(0) for m in re.finditer(r'<article class="u-tafel" id="([^"]+)">.*?</article>', s, re.S)}
for fid in ['trainingsplanung','reisemedizin']:
    m=re.search(r'\s*<!-- 0\d -+ -->\s*<section class="reiter-tafel" id="%s">.*?</section>' % fid, s, re.S)
    assert m, fid
    s=s.replace(m.group(0),'')
for fid,ids in behalten.items():
    a=s.index('<section class="reiter-tafel" id="%s">' % fid)
    e=s.index('</section>', a)
    k=s.index('<div class="u-tafeln">', a, e)+len('<div class="u-tafeln">')
    z=s.rindex('</article>', a, e)+len('</article>')
    neu='\n\n              '.join(arts[i] for i in ids)
    s=s[:k]+'\n\n              '+neu+'\n\n            '+s[z:]
s=re.sub(r'\s*<a class="reiter-knopf" href="#trainingsplanung">.*?</a>','',s,flags=re.S)
s=re.sub(r'\s*<a class="reiter-knopf" href="#reisemedizin">.*?</a>','',s,flags=re.S)
s=s.replace('<span class="nr">06</span>Allgemeinmedizin','<span class="nr">05</span>Allgemein- und Reisemedizin')
s=s.replace('<h2><span class="tafel-nr">06</span>Allgemeinmedizin</h2>','<h2><span class="tafel-nr">05</span>Allgemein- und Reisemedizin</h2>')
s=s.replace('<h3>Reiseplanung</h3>','<h3>Reisemedizin</h3>').replace('<h3>Tauchtauglichkeit</h3>','<h3>Tauch- und Sprungtauglichkeit</h3>')
leads={'sportmedizin':'Wenn beim Sport etwas passiert ist, schaue ich mir das selbst an: was verletzt ist, was es braucht und wann Sie wieder loslegen können.',
 'leistungsdiagnostik':'Ich messe, statt zu schätzen. Laktat, Belastungs-EKG und Herzultraschall zeigen, wo Sie stehen und wie Sie sinnvoll trainieren.',
 'sport-reha':'Vor und nach einer Operation begleite ich Sie, auch wenn der Eingriff woanders stattfindet. Bis zur Freigabe.',
 'arthrosetherapie':'Bei Verschleiß am Gelenk gibt es mehr als Schmerzmittel oder Operation. Was im Einzelfall Sinn macht, besprechen wir vorher in Ruhe.',
 'allgemeinmedizin':'Check-up, Reisevorbereitung und die Untersuchungen, die man vor dem Tauchen oder Springen braucht. Auch wenn Sie keinen Sport machen.'}
for fid,txt in leads.items():
    s,n=re.subn(r'(<section class="reiter-tafel" id="%s">(?:(?!<section).)*?<p class="lead">)(.*?)(</p>)' % fid, lambda m: m.group(1)+txt+m.group(3), s, count=1, flags=re.S)
    assert n==1, fid
s=re.sub(r'\s*<svg class="lz".*?</svg>','',s,flags=re.S)
s=re.sub(r'\s*<!-- Suche über alle Leistungen.*?<div class="suche-band">.*?</form>\s*</div>\s*</div>','',s,flags=re.S)
s=s.replace('<h2 class="reveal">Was für Sie infrage kommt,<br>klärt der Befund.</h2>','<h2 class="reveal">Was zu Ihnen passt,<br>sehen wir zusammen.</h2>')
s=re.sub(r'Welche der Leistungen in Ihrem Fall sinnvoll ist, lässt sich\s*seriös erst nach der Untersuchung sagen\. Der Weg dorthin\s*ist ein Anruf\.','Am Telefon kann ich Ihnen noch nicht sagen, was Sie brauchen. Nach der Untersuchung schon. Rufen Sie einfach an.',s)
wr('leistungen.html',s)
print('Felder:',len(re.findall('class="reiter-tafel"',s)),'Leistungen:',len(re.findall('class="u-tafel"',s)))

# ============================================================ index.html
s=rd('index.html')
s=re.sub(r'\s*<!-- Suche über alle Leistungen.*?<div class="suche-band">.*?</form>\s*</div>\s*</div>','',s,flags=re.S)
s=s.replace('''        Beim Sport ist etwas passiert? Hier untersucht, behandelt und begleitet
        Sie ein Arzt — vom ersten Tag bis zurück auf den Platz.''',
'''        Wenn beim Sport etwas passiert ist, kümmere ich mich darum. Selbst,
        vom ersten Tag, bis Sie wieder auf dem Platz stehen.''')
s=re.sub(r'\s*<p class="pulse-cap" aria-hidden="true">.*?</p>','',s,flags=re.S)
s=re.sub(r'\s*<!-- Sehr helle Ton-in-Ton.*?<img class="hero-fond".*?>(?:<span[^>]*>\d+</span>)?','',s,flags=re.S)
s=re.sub(r'\s*<!-- Zweiter Ton-in-Ton-Fond.*?<img class="fond-bild".*?>(?:<span[^>]*>\d+</span>)?','',s,flags=re.S)
s=s.replace('<section class="sec-tint sec-fond">','<section class="sec-tint">')
s=s.replace('          <h2 class="reveal">Ein Arzt.<br>Von Anfang bis Ende.</h2>','          <h2 class="reveal">Sie sehen immer<br>denselben Arzt.</h2>')
s,n=re.subn(r'<div class="bild-platz bild-platz--hoch reveal"[^>]*><span class="bild-nr" aria-hidden="true">4</span>.*?</div>',
 '''<figure class="portraet reveal" style="--dl:200ms;margin-top:2.5rem">
            <img src="assets/img/foto-03-meisterschale.webp?v=1" width="1024" height="1536" loading="lazy" alt="Dr. med. Günter Pfeiler mit der Meisterschale in der Arena des VfL Wolfsburg"><span class="bild-nr" aria-hidden="true">4</span>
            <figcaption>Archivfoto, VfL Wolfsburg</figcaption>
          </figure>
          <p class="todo">Vorläufig: Archivfoto als Porträt. Ein aktuelles Foto im Sprechzimmer ersetzt es, sobald es da ist. Bildrechte klären.</p>''', s, count=1, flags=re.S)
assert n==1,'portraet'
s=s.replace('''            Sie werden nicht weitergereicht. Dr. Pfeiler untersucht Sie selbst,
            behandelt Sie selbst und bleibt dran, bis Sie wieder Sport machen.''',
'''            Ich untersuche Sie selbst, behandle Sie selbst und bleibe dran,
            bis Sie wieder Sport machen können. Weitergereicht wird hier niemand.''')
s=s.replace('<li><strong>Privatpraxis.</strong> Zeit für Sie, Termine ohne Wartezimmer-Marathon.</li>','<li><strong>Privatpraxis.</strong> Ich nehme mir Zeit. Termine gibt es nach Absprache, nicht nach Nummer.</li>')
s=s.replace('<li><strong>Sportverletzungen mit behandelndem Arzt.</strong> Befund, Therapie und Freigabe in einer Hand.</li>','<li><strong>Sportverletzungen.</strong> Befund, Behandlung und Freigabe aus einer Hand.</li>')
s=s.replace('<li><strong>Erfahrung aus dem Profifußball.</strong> Zwanzig Jahre Mannschaftsarzt beim VfL Wolfsburg.</li>','<li><strong>Zwanzig Jahre Profifußball.</strong> Als Mannschaftsarzt des VfL Wolfsburg habe ich fast jede Sportverletzung gesehen.</li>')
s=re.sub(r'\s*<li>Untersuchung und Befund im selben Termin — nicht über Wochen verteilt\.</li>','',s)
s,n=re.subn(r'<section class="sec-band">\s*<div class="wrap">\s*<figure class="bild-band reveal".*?</figure>\s*</div>\s*</section>',
'''<section class="sec-band">
    <div class="wrap">
      <div class="schau reveal" aria-roledescription="Bildergalerie" aria-label="Bilder aus zwanzig Jahren Sportmedizin">
        <figure class="schau-bild ist-aktiv">
          <img src="assets/img/foto-01-spielfeldrand.webp?v=1" width="1536" height="1024" loading="eager" alt="Dr. Pfeiler untersucht am Spielfeldrand die Schulter eines Spielers"><span class="bild-nr" aria-hidden="true">27</span>
          <figcaption>Am Spielfeldrand</figcaption>
        </figure>
        <figure class="schau-bild">
          <img src="assets/img/foto-02-dfb-pokal.webp?v=1" width="1536" height="1536" loading="lazy" alt="Dr. Pfeiler mit dem DFB-Pokal"><span class="bild-nr" aria-hidden="true">28</span>
          <figcaption>DFB-Pokalsieg 2015</figcaption>
        </figure>
        <figure class="schau-bild">
          <img src="assets/img/b-06-befundgespraech.webp?v=1" width="1536" height="1024" loading="lazy" alt="Befundgespräch am Kniemodell"><span class="bild-nr" aria-hidden="true">26</span>
          <figcaption>Im Sprechzimmer · Symbolbild</figcaption>
        </figure>
        <div class="schau-punkte" role="tablist" aria-label="Bild wählen"></div>
      </div>
      <p class="todo">Slideshow: vorerst zwei echte Archivfotos plus eine Symbolszene. Weitere echte Bilder (Praxis, Eingang, Sprechzimmer) hier ergänzen. Bildrechte klären.</p>
    </div>
  </section>''', s, count=1, flags=re.S)
assert n==1,'schau'
s=re.sub(r'\s*<a class="feld reveal" style="--dl:280ms" href="leistungen.html#trainingsplanung">.*?</a>','',s,flags=re.S)
s=re.sub(r'\s*<a class="feld reveal" style="--dl:420ms" href="leistungen.html#reisemedizin">.*?</a>','',s,flags=re.S)
s=s.replace('<span class="feld-nr">06</span>\n          <h3>Allgemeinmedizin</h3>','<span class="feld-nr">05</span>\n          <h3>Allgemein- und Reisemedizin</h3>')
s=s.replace('<p>Check-up mit Labor, EKG, Ultraschall und Lungenfunktion. Dazu Beratung.</p>','<p>Check-up, Impfberatung, Tauch- und Sprungtauglichkeit.</p>')
s=s.replace('<h2 class="reveal">Sieben Felder.</h2>','<h2 class="reveal">Was ich anbiete.</h2>')
s=s.replace('          Vom Sportunfall bis zur Reise. Kurz erklärt, ohne Fachchinesisch.','          Fünf Bereiche. Kurz erklärt, Einzelheiten im Gespräch.')
s=s.replace('<p>Sportverletzungen: untersuchen, behandeln, vorbeugen. Dazu Ernährungsberatung.</p>','<p>Untersuchen, behandeln, vorbeugen.</p>')
s=s.replace('<p>Laktat-Test, Belastungs-EKG, Herzultraschall, Lungenfunktion. Messen statt schätzen.</p>','<p>Laktat, Belastungs-EKG, Herzultraschall, Trainingsplan.</p>')
s=s.replace('<p>Vor und nach der OP: Beratung, Kontrollen, Reha-Steuerung, Wiedereinstieg.</p>','<p>Vor und nach der Operation, bis zur Freigabe.</p>')
s=s.replace('<p>Stoßwelle, Hyaluronsäure, Eigenblut (ACP) und Schmerztherapie.</p>','<p>Stoßwelle, Hyaluronsäure, Eigenblut.</p>')
s,n=re.subn(r'\s*<!-- ==== Ablauf =+ -->\s*<section>.*?</section>','',s,count=1,flags=re.S); assert n==1,'ablauf'
s=s.replace('<h2 class="reveal">Woher die Erfahrung kommt.</h2>','<h2 class="reveal">Woher ich komme.</h2>')
s=s.replace('''            Dr. Pfeiler ist Mannschaftsarzt im Verfahren der VBG, der
            Unfallversicherung des Profisports. Von 1998 bis 2018 war er
            Mannschaftsarzt des VfL Wolfsburg, seitdem berät er den Verein.''',
'''            Von 1998 bis 2018 war ich Mannschaftsarzt des VfL Wolfsburg,
            seitdem berate ich den Verein. Ich bin Mannschaftsarzt im
            Verfahren der VBG, der Unfallversicherung des Profisports.''')
s=re.sub(r'\s*<details>\s*<summary>Kann ich meine Beschwerden vorab per E-Mail schildern\?</summary>.*?</details>','',s,flags=re.S)
s=re.sub(r'\s*<details>\s*<summary>Behandeln Sie auch Menschen, die keinen Sport treiben\?</summary>.*?</details>','',s,flags=re.S)
s=s.replace('<h2 class="reveal">Vorab geklärt.</h2>','<h2 class="reveal">Was oft gefragt wird.</h2>')
s=s.replace('<p>Ja. Abgerechnet wird nach GOÄ. Privatversicherte reichen die Rechnung ein, gesetzlich Versicherte kommen als Selbstzahler. Was Ihre Kasse erstattet, klären Sie bitte vorab.</p>',
            '<p>Ja. Ich rechne nach der Gebührenordnung für Ärzte ab. Privatversicherte reichen die Rechnung bei ihrer Versicherung ein, gesetzlich Versicherte zahlen selbst. Fragen Sie vorher bei Ihrer Kasse nach, was sie übernimmt.</p>')
s=s.replace('<p>Telefonisch. Frische Verletzung? Sagen Sie es gleich, dafür ist kurzfristig Zeit reserviert.</p>','<p>Rufen Sie an. Wenn es eine frische Verletzung ist, sagen Sie das gleich, dann finde ich kurzfristig einen Termin.</p>')
s=s.replace('<p>Vorbefunde und Bilder (Röntgen, MRT), Medikamentenliste, bei Reisen den Impfpass. Zur Leistungsdiagnostik Sportkleidung.</p>','<p>Alte Befunde und Bilder, Ihre Medikamente, bei Reisen den Impfpass. Für Belastungstests Sportzeug.</p>')
s=s.replace('<h2 class="reveal">Sprechen wir.</h2>','<h2 class="reveal">Rufen Sie an.</h2>')
s=s.replace('''            Rufen Sie einfach an. Ein Satz zum Anlass genügt, den Rest
            klären wir im Termin.''','''            Ein Satz, worum es geht, reicht. Alles Weitere besprechen wir,
            wenn Sie da sind.''')
wr('index.html',s)

# ============================================================ übrige Seiten
for n in ['praxis.html','kontakt.html','impressum.html','datenschutz.html']:
    t=rd(n); t=re.sub(r'\s*<!-- Suche über alle Leistungen.*?<div class="suche-band">.*?</form>\s*</div>\s*</div>','',t,flags=re.S); wr(n,t)
t=rd('praxis.html')
t=t.replace('''        Facharzt für Allgemeinmedizin mit Schwerpunkt Sportverletzungen.
        Zwanzig Jahre Mannschaftsarzt beim VfL Wolfsburg, heute Privatpraxis
        in Braunschweig. Er behandelt Sie selbst — von Anfang bis Ende.''',
'''        Ich bin Facharzt für Allgemeinmedizin und habe mich auf
        Sportverletzungen konzentriert. Zwanzig Jahre war ich Mannschaftsarzt
        beim VfL Wolfsburg. Heute habe ich meine Privatpraxis in Braunschweig
        und behandle Sie selbst, von Anfang bis Ende.''')
t=t.replace('''            Dr. Pfeiler ist Mannschaftsarzt (M-Arzt) im Verfahren der VBG,
            der Unfallversicherung des Profisports.''','''            Ich bin Mannschaftsarzt (M-Arzt) im Verfahren der VBG, der
            Unfallversicherung des Profisports.''')
t=t.replace('''            Von 1998 bis 2018 betreute er die Profis des VfL Wolfsburg, seit
            2018 berät er den Verein. Diese Erfahrung kommt jetzt Ihnen zugute.''','''            Von 1998 bis 2018 habe ich die Profis des VfL Wolfsburg betreut,
            seit 2018 berate ich den Verein. Was ich dort gelernt habe, kommt
            jetzt Ihnen zugute.''')
wr('praxis.html',t)
t=rd('kontakt.html')
t=t.replace('''        Termine werden telefonisch vergeben. Sagen Sie bitte gleich dazu,
        worum es geht — bei einer frischen Verletzung wird kurzfristig
        geplant, bei einem Check-up in Ruhe.''','''        Termine gibt es bei mir telefonisch. Sagen Sie kurz, worum es geht.
        Bei einer frischen Verletzung finde ich schnell etwas, einen Check-up
        planen wir in Ruhe.''')
t=t.replace('''                <p>Die Hamburger Straße ist eine der Hauptachsen im Norden von
                Braunschweig und aus beiden Richtungen ausgeschildert.
                Ob es Parkplätze am Haus gibt, ist noch nicht bestätigt.</p>''',
'''                <p>Die Praxis liegt in der Nordstadt im ehemaligen Verlagshaus
                der Braunschweiger Zeitung. Direkt am Haus gibt es ein Parkhaus,
                Einfahrt Hamburger Straße 277. Von der A 391 über die Abfahrt
                Hamburger Straße stadteinwärts, etwa fünf Minuten.</p>
                <p><a class="btn btn--ghost btn--sm" href="https://www.google.com/maps/dir/?api=1&amp;destination=Hamburger+Stra%C3%9Fe+277%2C+38114+Braunschweig" target="_blank" rel="noopener noreferrer">Route in Google Maps öffnen</a></p>''')
t=t.replace('''                <p>Die Hamburger Straße wird von Straßenbahn und Bus bedient.
                Welche Haltestelle die nächste ist und wie weit sie zu Fuß
                entfernt liegt, wird hier ergänzt, sobald es feststeht.</p>''',
'''                <p>Mit der Stadtbahn bis zur Haltestelle an der Hamburger
                Straße, von dort sind es ein paar Minuten zu Fuß. Der
                Ringgleis-Radweg führt direkt am Gebäude vorbei.</p>''')
t=t.replace('''          <p class="todo">
            Noch zu bestätigen: Anschrift und Rufnummer stammen vom
            Praxisstempel.''','''          <p class="todo">
            Noch zu bestätigen: Haltestellenname und Linie der Stadtbahn, Fahrradbügel,
            Etage und Aufzug. Google-Maps-Link öffnet erst auf Klick, keine Einbettung,
            keine Datenweitergabe beim Seitenaufruf. Anschrift und Rufnummer stammen vom
            Praxisstempel.''')
wr('kontakt.html',t)
print('html ok')
