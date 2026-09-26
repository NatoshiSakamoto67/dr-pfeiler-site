cd ~/dr-pfeiler-site; mkdir -p entwuerfe/szenen3
B=werkzeug/bild.py; S1=vorlagen/stil/ki-01-knie-reflexhammer.jpg
ARZT="Fotorealistische Aufnahme in derselben hellen, ruhigen Praxis wie im Referenzbild: derselbe Arzt (weißhaarig, um die 70, beiges kurzärmeliges Hemd), weiches Tageslicht, gedeckte Farben in Creme, Sand und Anthrazit, keine bunten Poster, keine Schrift, natürliche Menschen. Ärztliche Situation, keinesfalls Massage oder Wellness. "
job(){ eval "$B edit --qualitaet high --format quer $@" & }
job -o entwuerfe/szenen3/ekg.png $S1 "\"${ARZT}Ruhe-EKG: Ein Patient liegt auf der Liege mit Elektroden an Brust, Armen und Beinen, der Arzt betrachtet den EKG-Streifen.\""
job -o entwuerfe/szenen3/lungenfunktion.png $S1 "\"${ARZT}Ein älterer Patient bläst in ein Spirometer, der Arzt sitzt daneben und ermutigt mit erhobener Hand, Fluss-Volumen-Kurve am Bildschirm.\""
job -o entwuerfe/szenen3/gesundheitsstatus.png $S1 "\"${ARZT}Der Arzt überreicht einem Patienten eine schriftliche Zusammenfassung in einer Mappe, beide am Schreibtisch, Befunde ausgebreitet.\""
job -o entwuerfe/szenen3/gesundheitsberatung.png $S1 "\"${ARZT}Beratungsgespräch: Der Arzt und eine Patientin um die 50 sitzen sich entspannt gegenüber, auf dem Tisch ein Blatt mit drei notierten Schritten.\""
job -o entwuerfe/szenen3/reiseplanung.png $S1 "\"${ARZT}Der Arzt zeigt einer jungen Reisenden auf einer Weltkarte am Tisch die Route, daneben Impfpass und eine kleine Reiseapotheke.\""
wait
echo NACHLAUF3 FERTIG
