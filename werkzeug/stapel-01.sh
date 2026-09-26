#!/bin/zsh
# Stapel 1: Foto-Restaurierungen + neue Behandlungsszenen. Läuft parallel (4 gleichzeitig).
cd ~/dr-pfeiler-site
B=werkzeug/bild.py
REST="Restauriere dieses abfotografierte Papierfoto zu einem sauberen, hochwertigen Foto: exakt dasselbe Motiv, dieselben Personen mit unveränderten Gesichtern, Körperhaltungen, Kleidung und Logos. Entferne Spiegelungen, Glanz, Moiré, Bildschirm- und Druckraster, Schrägstellung und den umgebenden Seitenrand; richte das Bild gerade aus und beschneide auf das eigentliche Foto. Natürliche Farben, feines Filmkorn, weiche Schärfe. Nichts hinzuerfinden."
ARZT="Fotorealistische Aufnahme in einer hellen, ruhigen Arztpraxis wie in den Referenzbildern: derselbe Arzt (weißhaarig, um die 70, beiges kurzärmeliges Hemd) wie auf den Referenzbildern, gleicher Bildstil, weiches Tageslicht, gedeckte Farben in Creme, Sand und Anthrazit, keine bunten Poster, keine Schrift. Konzentrierte, ärztliche Untersuchungssituation — keinesfalls Massage oder Wellness. "
S1=vorlagen/stil/ki-01-knie-reflexhammer.jpg
S2=vorlagen/stil/ki-02-ultraschall.jpg
eval "$B edit --qualitaet high --format quer  -o entwuerfe/fotos/foto-01-spielfeldrand.png vorlagen/fotos/foto-01-spielfeldrand.jpg \"$REST\"" &
eval "$B edit --qualitaet high --format quadrat -o entwuerfe/fotos/foto-02-dfb-pokal.png vorlagen/fotos/foto-02-dfb-pokal.jpg \"$REST\"" &
eval "$B edit --qualitaet high --format hoch  -o entwuerfe/fotos/foto-03-meisterschale.png vorlagen/fotos/foto-03-meisterschale.jpg \"$REST\"" &
eval "$B edit --qualitaet high --format quer -o entwuerfe/behandlung/b-01-sprunggelenk-ultraschall.png $S2 $S1 \"${ARZT}Der Arzt sitzt am Fußende der Liege und untersucht das Sprunggelenk eines Sportlers in Sportshorts mit dem Ultraschallkopf; das Ultraschallgerät steht seitlich, der Sportler sitzt aufrecht und schaut zum Monitor.\"" &
eval "$B edit --qualitaet high --format quer -o entwuerfe/behandlung/b-02-knie-stabilitaetstest.png $S1 $S2 \"${ARZT}Der Arzt prüft mit beiden Händen die Bandstabilität des Knies eines sitzenden Sportlers (Schublade-Test), Blick konzentriert auf das Gelenk; der Sportler trägt Sportshorts und ein graues Shirt.\"" &
eval "$B edit --qualitaet high --format quer -o entwuerfe/behandlung/b-03-schulter-untersuchung.png $S1 $S2 \"${ARZT}Der Arzt steht seitlich neben einem sitzenden Sportler und führt dessen Arm zur Prüfung der Schulterbeweglichkeit nach oben; eine Hand am Schulterblatt, die andere am Ellenbogen. Sachlich, orthopädische Funktionsprüfung.\"" &
eval "$B edit --qualitaet high --format quer -o entwuerfe/behandlung/b-04-belastungs-ekg.png $S2 $S1 \"${ARZT}Ein Sportler tritt auf einem Fahrradergometer mit EKG-Elektroden auf der Brust und Blutdruckmanschette am Arm; der Arzt steht daneben und liest die EKG-Kurve auf dem Monitor. Leistungsdiagnostik.\"" &
eval "$B edit --qualitaet high --format quer -o entwuerfe/behandlung/b-05-tape-sprunggelenk.png $S1 $S2 \"${ARZT}Der Arzt legt einem sitzenden Sportler ein stabilisierendes Tape um das Sprunggelenk an, weißes Sporttape, präzise Handhaltung, der Fuß ruht auf der Liege.\"" &
eval "$B edit --qualitaet high --format quer -o entwuerfe/behandlung/b-06-befundgespraech.png $S1 $S2 \"${ARZT}Der Arzt sitzt mit einem Sportler am Schreibtisch und erklärt ihm an einem anatomischen Kniemodell den Befund; beide schauen auf das Modell, freundliche, ruhige Gesprächssituation.\"" &
wait

eval "STAPEL FERTIG" &
ls -la entwuerfe/fotos entwuerfe/behandlung
