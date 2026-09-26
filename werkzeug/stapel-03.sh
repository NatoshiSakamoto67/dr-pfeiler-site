#!/bin/zsh
# Stapel 3: Bilder für die 23 Leistungen ohne Bild (werden Nr. 35–57).
cd ~/dr-pfeiler-site; mkdir -p entwuerfe/szenen3
B=werkzeug/bild.py; S1=vorlagen/stil/ki-01-knie-reflexhammer.jpg
ARZT="Fotorealistische Aufnahme in derselben hellen, ruhigen Praxis wie im Referenzbild: derselbe Arzt (weißhaarig, um die 70, beiges kurzärmeliges Hemd), weiches Tageslicht, gedeckte Farben in Creme, Sand und Anthrazit, keine bunten Poster, keine Schrift, natürliche Menschen. Ärztliche Situation, keinesfalls Massage oder Wellness. "
job(){ eval "$B edit --qualitaet high --format quer $@" & }
welle(){ wait; echo "--- Welle fertig $(date +%H:%M:%S)"; sleep 70; }
job -o entwuerfe/szenen3/sv-therapie.png $S1 "\"${ARZT}Der Arzt legt einem sitzenden Sportler eine Kniebandage an und erklärt den Stufenplan, daneben ein Ausdruck mit Wochenplan.\""
job -o entwuerfe/szenen3/sv-prophylaxe.png $S1 "\"${ARZT}Eine junge Sportlerin steht im Einbeinstand auf einer Matte, der Arzt beobachtet die Beinachse und notiert auf einem Klemmbrett.\""
job -o entwuerfe/szenen3/ernaehrung.png $S1 "\"${ARZT}Der Arzt sitzt mit einer Läuferin am Tisch, vor ihnen ein Ernährungsprotokoll und ein Laborausdruck, eine Wasserflasche und Obst auf dem Tisch.\""
job -o entwuerfe/szenen3/fitness-status.png $S1 "\"${ARZT}Ein Patient mittleren Alters steht auf einer Körperanalysewaage, der Arzt liest die Werte ab und misst den Taillenumfang mit einem Maßband.\""
job -o entwuerfe/szenen3/ld-blut.png $S1 "\"${ARZT}Der Arzt nimmt einem Sportler in der Armbeuge Blut ab, Röhrchen mit farbigen Kappen im Ständer daneben.\""
welle
job -o entwuerfe/szenen3/ld-lufu.png $S1 "\"${ARZT}Eine Sportlerin atmet kräftig in ein Spirometer mit Mundstück und Nasenklemme, der Arzt hält das Gerät und schaut auf die Kurve am Bildschirm.\""
job -o entwuerfe/szenen3/echo.png $S1 "\"${ARZT}Herzultraschall: Der Patient liegt in Linksseitenlage, der Arzt hält den Schallkopf an den Brustkorb, auf dem Monitor ein schlagendes Herz im Ultraschallbild.\""
job -o entwuerfe/szenen3/stress-echo.png $S1 "\"${ARZT}Ein Patient tritt auf einem halb liegenden Ergometer, der Arzt führt gleichzeitig den Ultraschallkopf am Brustkorb, Monitor mit Herzbild daneben.\""
job -o entwuerfe/szenen3/op-beratung.png $S1 "\"${ARZT}Der Arzt zeigt einem Patienten am Bildschirm eine MRT-Aufnahme des Knies und erklärt, beide sitzen am Schreibtisch, OP-Bericht auf dem Tisch.\""
job -o entwuerfe/szenen3/reha-steuerung.png $S1 "\"${ARZT}Der Arzt telefoniert am Schreibtisch mit Blick auf einen Kalender und Physiotherapie-Berichte, im Hintergrund ein Patient mit Krücken, der wartet.\""
welle
job -o entwuerfe/szenen3/eswt.png $S1 "\"${ARZT}Stoßwellentherapie an der Ferse: Die Patientin liegt auf dem Bauch, der Arzt setzt das Handstück des Stoßwellengeräts an die Fußsohle, Gel sichtbar.\""
job -o entwuerfe/szenen3/schmerztherapie.png $S1 "\"${ARZT}Der Arzt bespricht mit einer Patientin um die 60 einen Schmerzverlaufsbogen, ruhiges Gespräch am Tisch, Medikamentenliste daneben.\""
job -o entwuerfe/szenen3/trainingsstatus.png $S1 "\"${ARZT}Der Arzt und ein Läufer schauen auf ein Tablet mit Trainingsdaten (Wochenumfang als Balken), Laufschuhe auf dem Tisch.\""
job -o entwuerfe/szenen3/verletzungsprophylaxe.png $S1 "\"${ARZT}Ein Jugendlicher macht einen Sprung-Landetest von einer kleinen Box, der Arzt beobachtet in der Hocke die Knieposition.\""
job -o entwuerfe/szenen3/blutuntersuchung.png $S1 "\"${ARZT}Nahaufnahme: Blutröhrchen im Ständer und ein Laborausdruck, die Hand des Arztes zeigt mit dem Stift auf einen Wert, Patient unscharf im Hintergrund.\""
welle
job -o entwuerfe/szenen3/ekg.png $S1 "\"${ARZT}Ruhe-EKG: Ein Patient liegt auf der Liege mit Elektroden an Brust, Armen und Beinen, der Arzt betrachtet den EKG-Streifen.\""
job -o entwuerfe/szenen3/lungenfunktion.png $S1 "\"${ARZT}Ein älterer Patient bläst in ein Spirometer, der Arzt sitzt daneben und ermutigt mit erhobener Hand, Fluss-Volumen-Kurve am Bildschirm.\""
job -o entwuerfe/szenen3/gesundheitsstatus.png $S1 "\"${ARZT}Der Arzt überreicht einem Patienten eine schriftliche Zusammenfassung in einer Mappe, beide am Schreibtisch, Befunde ausgebreitet.\""
job -o entwuerfe/szenen3/gesundheitsberatung.png $S1 "\"${ARZT}Beratungsgespräch: Der Arzt und eine Patientin um die 50 sitzen sich entspannt gegenüber, auf dem Tisch ein Blatt mit drei notierten Schritten.\""
job -o entwuerfe/szenen3/reiseplanung.png $S1 "\"${ARZT}Der Arzt zeigt einer jungen Reisenden auf einer Weltkarte am Tisch die Route, daneben Impfpass und eine kleine Reiseapotheke.\""
welle
job -o entwuerfe/szenen3/reisekrankheiten.png $S1 "\"${ARZT}Der Arzt tastet den Bauch eines Patienten ab, der nach einer Reise Beschwerden hat, ein Koffer-Anhänger und Reisepass liegen auf dem Beistelltisch.\""
job -o entwuerfe/szenen3/reise-prophylaxe.png $S1 "\"${ARZT}Der Arzt hält eine Packung Malaria-Tabletten und ein Moskitonetz-Muster, erklärt einer Patientin die Einnahme, Impfpass auf dem Tisch.\""
job -o entwuerfe/szenen3/fallschirm.png $S1 "\"${ARZT}Der Arzt prüft bei einem sportlichen Mann Blutdruck und Gleichgewicht (Romberg-Stand), auf der Ablage liegt ein Fallschirm-Helm.\""
wait; echo "STAPEL 3 FERTIG $(date +%H:%M:%S)"; ls entwuerfe/szenen3 | wc -l
