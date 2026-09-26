cd ~/dr-pfeiler-site
B=werkzeug/bild.py
K=vorlagen/ottocento/visitenkarte-klein.jpg
S1=vorlagen/stil/ki-01-knie-reflexhammer.jpg
TEX="Fotorealistische Nahaufnahme einer Wand in Ottocento-Spachtel- und Wischtechnik, exakt im Ton und in der Struktur der Vorlage (Visitenkarte): mattes Anthrazitgrau mit hellgrauen, weich verwischten Pinsel- und Kellenbahnen, feine Papier-/Putzkörnung, leichte Wolkigkeit, Streiflicht von links oben. Vollflächig, ohne Rand, ohne Schrift, ohne Gegenstände, wie echt gestrichen. "
ARZT="Fotorealistische Aufnahme in derselben hellen, ruhigen Praxis wie im Referenzbild: derselbe Arzt (weißhaarig, um die 70, beiges kurzärmeliges Hemd), weiches Tageslicht, gedeckte Farben in Creme, Sand und Anthrazit, keine bunten Poster, keine Schrift, natürliche Menschen. Ärztliche Situation, keinesfalls Massage oder Wellness. "
job(){ eval "$B edit --qualitaet high $@" & }
job --format quer -o entwuerfe/szenen/s18-sportbelastungstest.png $S1 "\"${ARZT}Ein Läufer läuft auf dem Laufband mit EKG-Elektroden, der Arzt steht daneben und beobachtet Monitor und Läufer, Hand an der Notaus-Taste.\""
job --format quer -o entwuerfe/szenen/s20-checkup.png $S1 "\"${ARZT}Der Arzt hört mit dem Stethoskop das Herz eines Patienten mittleren Alters ab, der auf der Liege sitzt.\""
job --format quer -o entwuerfe/szenen/s21-sonographie.png $S1 "\"${ARZT}Bauch-Ultraschall: Der Arzt führt den Schallkopf über den Oberbauch eines liegenden Patienten, Blick zum Monitor.\""
job --format quer -o entwuerfe/szenen/s23-impfberatung.png $S1 "\"${ARZT}Der Arzt setzt einer Patientin eine Impfung in den Oberarm, auf dem Tisch ein gelber Impfpass und die Impfstoffampulle.\""
job --format quer -o entwuerfe/szenen/s24-tauchtauglichkeit.png $S1 "\"${ARZT}Der Arzt untersucht mit dem Otoskop das Ohr eines Tauchers, auf der Ablage liegen Taucherbrille und Schnorchel.\""
wait
echo NACHLAUF FERTIG
