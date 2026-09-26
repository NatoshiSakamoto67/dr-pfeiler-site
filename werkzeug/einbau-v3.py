#!/usr/bin/env python3
"""Szenen aus entwuerfe/szenen-v3 an die Stelle der bisherigen Dateien setzen (gleiche Nummern), ?v hochzählen."""
import re, pathlib, subprocess
R = pathlib.Path.home()/'dr-pfeiler-site'; W = R/'web'
alt = {'s01':'band-diagnostik','s05':'leistung-sportmedizin','s07':'leistung-leistungsdiagnostik','s10':'leistung-sport-reha',
 's13':'leistung-arthrosetherapie','s16':'leistung-trainingsplanung','s19':'leistung-allgemeinmedizin','s22':'leistung-reisemedizin',
 's06':'u-sv-diagnostik','s08':'u-laktattest','s09':'u-belastungs-ekg','s11':'u-kontrolluntersuchungen','s12':'u-sportempfehlungen',
 's14':'u-hyaluron','s15':'u-acp','s17':'u-trainingssteuerung','s18':'u-sportbelastungstest','s20':'u-checkup','s21':'u-sonographie',
 's23':'u-impfberatung','s24':'u-tauchtauglichkeit'}
n=0; fehlt=[]
for png in sorted((R/'entwuerfe/szenen-v3').glob('*.png')):
    stem = png.stem
    ziel = alt.get(stem[:3]) if stem[:3] in alt else 'u-'+stem
    subprocess.run(['cwebp','-q','82','-resize','1536','0',str(png),'-o',str(W/'assets/img'/(ziel+'.webp'))],capture_output=True); n+=1
erwartet = set(alt.values()) | {'u-'+x for x in ['sv-therapie','sv-prophylaxe','ernaehrung','fitness-status','ld-blut','ld-lufu','echo','stress-echo','op-beratung','reha-steuerung','eswt','schmerztherapie','trainingsstatus','verletzungsprophylaxe','blutuntersuchung','ekg','lungenfunktion','gesundheitsstatus','gesundheitsberatung','reiseplanung','reisekrankheiten','reise-prophylaxe','fallschirm']}
vorhanden = {p.stem for p in (R/'entwuerfe/szenen-v3').glob('*.png')}
for f in ['index.html','leistungen.html']:
    t=(W/f).read_text()
    t=re.sub(r'(assets/img/(?:band-diagnostik|leistung-[a-z-]+|u-[a-z-]+)\.webp\?v=)(\d+)', lambda m: m.group(1)+str(int(m.group(2))+1), t)
    (W/f).write_text(t)
print('umgewandelt', n)
