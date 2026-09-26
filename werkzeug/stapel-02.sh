#!/bin/zsh
# Stapel 2: Ottocento-Texturen (Vorlage Visitenkarte) + 21 Szenen mit Dr. Pfeiler als Ersatz für Bild 1–24.
# Ratenlimit: 5 Eingabebilder/min → Wellen à 5 Jobs mit je einer Vorlage, 70 s Pause.
cd ~/dr-pfeiler-site
B=werkzeug/bild.py
K=vorlagen/ottocento/visitenkarte-klein.jpg
S1=vorlagen/stil/ki-01-knie-reflexhammer.jpg
TEX="Fotorealistische Nahaufnahme einer Wand in Ottocento-Spachtel- und Wischtechnik, exakt im Ton und in der Struktur der Vorlage (Visitenkarte): mattes Anthrazitgrau mit hellgrauen, weich verwischten Pinsel- und Kellenbahnen, feine Papier-/Putzkörnung, leichte Wolkigkeit, Streiflicht von links oben. Vollflächig, ohne Rand, ohne Schrift, ohne Gegenstände, wie echt gestrichen. "
ARZT="Fotorealistische Aufnahme in derselben hellen, ruhigen Praxis wie im Referenzbild: derselbe Arzt (weißhaarig, um die 70, beiges kurzärmeliges Hemd), weiches Tageslicht, gedeckte Farben in Creme, Sand und Anthrazit, keine bunten Poster, keine Schrift, natürliche Menschen. Ärztliche Situation, keinesfalls Massage oder Wellness. "
job(){ eval "$B edit --qualitaet high $@" & }
welle(){ wait; echo "--- Welle fertig $(date +%H:%M:%S)"; sleep 70; }

# Welle 1: Texturen
job --format quer    -o entwuerfe/ottocento/tex-01-anthrazit-quer.png $K "\"${TEX}Gleichmäßig dunkel, Bahnen diagonal.\""
job --format hoch    -o entwuerfe/ottocento/tex-02-anthrazit-hoch.png $K "\"${TEX}Bahnen senkrecht, leicht dunkler zum unteren Rand.\""
job --format quer    -o entwuerfe/ottocento/tex-03-hell-quer.png     $K "\"${TEX}Als helle Variante: warmes Hellgrau-Beige (Papierton) statt Anthrazit, dieselbe Wischtechnik, sehr zurückhaltend.\""
job --format quadrat -o entwuerfe/ottocento/tex-04-anthrazit-kontrast.png $K "\"${TEX}Kräftigere, deutlich sichtbare Kellenbahnen mit mehr Hell-Dunkel-Kontrast, für kleine Ausschnitte.\""
job --format quer -o entwuerfe/szenen/s01-band-diagnostik.png $S1 "\"${ARZT}Breite Szene: Der Arzt nimmt einer Läuferin, die auf dem Laufband steht und kurz pausiert, einen Tropfen Blut vom Ohrläppchen für die Laktatmessung ab; rechts das Laktatmessgerät, links viel ruhige Fläche.\""
welle
# Welle 2: Feld-Intros
job --format quer -o entwuerfe/szenen/s05-sportmedizin.png $S1 "\"${ARZT}Der Arzt tastet die Achillessehne eines auf der Liege liegenden Läufers ab, konzentrierter Blick, Sportschuhe stehen am Boden.\""
job --format quer -o entwuerfe/szenen/s07-leistungsdiagnostik.png $S1 "\"${ARZT}Eine Radsportlerin tritt auf dem Ergometer, der Arzt hält ein Laktatmessgerät und liest den Wert ab; im Hintergrund ein Monitor mit Kurve.\""
job --format quer -o entwuerfe/szenen/s10-sport-reha.png $S1 "\"${ARZT}Der Arzt begleitet eine Patientin mit Knieorthese bei den ersten Schritten ohne Krücken durch den Praxisflur, eine Hand stützend am Ellenbogen.\""
job --format quer -o entwuerfe/szenen/s13-arthrosetherapie.png $S1 "\"${ARZT}Der Arzt behandelt den Ellenbogen einer sitzenden Patientin mit dem Handstück eines Stoßwellengeräts, Gel auf der Haut, Gerät auf Rollwagen daneben.\""
job --format quer -o entwuerfe/szenen/s16-trainingsplanung.png $S1 "\"${ARZT}Der Arzt sitzt mit einem Triathleten am Schreibtisch, auf dem Bildschirm eine Laktatkurve, auf dem Tisch ein ausgedruckter Wochenplan, beide zeigen darauf.\""
welle
job --format quer -o entwuerfe/szenen/s19-allgemeinmedizin.png $S1 "\"${ARZT}Der Arzt misst einem Patienten um die 60 den Blutdruck, ruhiges Gespräch, Stethoskop um den Hals.\""
job --format quer -o entwuerfe/szenen/s22-reisemedizin.png $S1 "\"${ARZT}Der Arzt berät ein Paar mittleren Alters am Schreibtisch, auf dem Tisch ein gelber Impfpass und ein aufgeschlagener Atlas, im Hintergrund ein Globus.\""
# Welle 3: Unter-Leistungen
job --format quer -o entwuerfe/szenen/s06-sv-diagnostik.png $S1 "\"${ARZT}Der Arzt untersucht die Schulter eines sitzenden Sportlers mit dem Ultraschallkopf, Monitor mit Ultraschallbild im Hintergrund.\""
job --format quer -o entwuerfe/szenen/s08-laktattest.png $S1 "\"${ARZT}Nahaufnahme: Die Hände des Arztes halten ein Laktatmessgerät mit Teststreifen an das Ohrläppchen eines Sportlers, ein kleiner Blutstropfen, im Hintergrund unscharf das Laufband.\""
job --format quer -o entwuerfe/szenen/s09-belastungs-ekg.png $S1 "\"${ARZT}Der Arzt klebt einem Patienten, der auf dem Fahrradergometer sitzt, EKG-Elektroden auf die Brust; Kabel führen zum Gerät.\""
welle
job --format quer -o entwuerfe/szenen/s11-kontrolluntersuchungen.png $S1 "\"${ARZT}Der Arzt misst mit einem Winkelmesser (Goniometer) den Beugewinkel des Knies einer liegenden Patientin, notiert den Wert.\""
job --format quer -o entwuerfe/szenen/s12-sportempfehlungen.png $S1 "\"${ARZT}Der Arzt zeigt einer Patientin um die 65 auf einem Übungsblatt gelenkschonende Übungen, beide sitzen am Tisch, freundliche Stimmung.\""
job --format quer -o entwuerfe/szenen/s14-hyaluron.png $S1 "\"${ARZT}Der Arzt mit Handschuhen setzt eine Injektion in das Knie eines sitzenden Patienten, sterile Abdeckung, Spritze mit klarer Flüssigkeit; sachlich, ruhig.\""
job --format quer -o entwuerfe/szenen/s15-acp.png $S1 "\"${ARZT}Der Arzt entnimmt ein Blutröhrchen aus einer kleinen Tischzentrifuge, daneben eine vorbereitete Spritze; Nahaufnahme der Hände, Gesicht im Hintergrund.\""
job --format quer -o entwuerfe/szenen/s17-trainingssteuerung.png $S1 "\"${ARZT}Der Arzt bespricht mit einem Radsportler die Daten von dessen Sportuhr, beide schauen auf das Display, Rennrad-Helm auf dem Tisch.\""
welle
job --format quer -o entwuerfe/szenen/s18-sportbelastungstest.png $S1 "\"${ARZT}Ein Läufer läuft auf dem Laufband mit EKG-Elektroden, der Arzt steht daneben und beobachtet Monitor und Läufer, Hand an der Notaus-Taste.\""
job --format quer -o entwuerfe/szenen/s20-checkup.png $S1 "\"${ARZT}Der Arzt hört mit dem Stethoskop das Herz eines Patienten mittleren Alters ab, der auf der Liege sitzt.\""
job --format quer -o entwuerfe/szenen/s21-sonographie.png $S1 "\"${ARZT}Bauch-Ultraschall: Der Arzt führt den Schallkopf über den Oberbauch eines liegenden Patienten, Blick zum Monitor.\""
job --format quer -o entwuerfe/szenen/s23-impfberatung.png $S1 "\"${ARZT}Der Arzt setzt einer Patientin eine Impfung in den Oberarm, auf dem Tisch ein gelber Impfpass und die Impfstoffampulle.\""
job --format quer -o entwuerfe/szenen/s24-tauchtauglichkeit.png $S1 "\"${ARZT}Der Arzt untersucht mit dem Otoskop das Ohr eines Tauchers, auf der Ablage liegen Taucherbrille und Schnorchel.\""
wait
echo "STAPEL 2 FERTIG $(date +%H:%M:%S)"
ls entwuerfe/ottocento entwuerfe/szenen
