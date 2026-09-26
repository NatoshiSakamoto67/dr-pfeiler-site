#!/usr/bin/env python3
"""Serie v4 (26.09.): ein fester heller Raum, wechselnde Perspektiven, editorial statt Stockfoto.

Welle 1 erzeugt den leeren Raum; alle Szenen danach bekommen ihn als zweite Vorlage,
damit Raum und Einrichtung über die ganze Serie gleich bleiben.
"""
import pathlib, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

BASIS = pathlib.Path.home() / 'dr-pfeiler-site'
ZIEL = BASIS / 'entwuerfe' / 'szenen-v4'
BILD = str(BASIS / 'werkzeug' / 'bild.py')
ARZT = str(BASIS / 'vorlagen' / 'stil' / 'ki-01-knie-reflexhammer.jpg')
RAUM_BILD = ZIEL / 'v4-raum.png'

RAUM = ('Immer derselbe Behandlungsraum: hell und ruhig, warmweiß gekalkte Wände, breite helle Eichendielen, '
        'ein hohes Sprossenfenster mit leichtem Leinenvorhang, eine Behandlungsliege mit cognacfarbenem Lederpolster, '
        'ein schmaler Schreibtisch aus Eiche, darauf ein Kniemodell und ein paar Bücher, eine große Pflanze im Terrakottatopf, '
        'eine schlichte Stehleuchte aus mattem Messing. Keine Poster, keine Anatomietafeln, kein Kunststoff-Klinikmobiliar. ')
STIL = ('Editoriales Reportagefoto wie in einem hochwertigen Magazin, natürliches weiches Tageslicht, '
        'gedeckte warme Farben (Elfenbein, Sand, Cognac, Eiche, etwas Anthrazit), feine Filmkörnung, geringe Tiefenschärfe, '
        'ruhige Bildkomposition mit viel Luft. Keine Schrift, keine Logos. Ärztliche Situation, keinesfalls Massage. ')
ARZT_TXT = 'Derselbe Arzt wie im ersten Referenzbild (Gesicht, weißes Haar, Alter um 70). '
RAUM_REF = 'Der Raum sieht exakt so aus wie im zweiten Referenzbild. '

SZENEN = [
    ('v4-hero-quer', 'quer', 'dunkelblaues Hemd, Ärmel einmal umgeschlagen, sandfarbene Hose',
     'Totale des Raums. Der Arzt steht im rechten Bilddrittel am Fenster, eine Hand am Fensterrahmen, und schaut ruhig hinaus; '
     'weiches Gegenlicht, links viel ruhige Fläche mit der Liege. Kamera auf Hüfthöhe, 35 mm.'),
    ('v4-hero-hoch', 'hoch', 'dunkelblaues Hemd, Ärmel einmal umgeschlagen, sandfarbene Hose',
     'Hochformat. Der Arzt steht am Fenster und schaut ruhig hinaus, halbes Profil von rechts, weiches Gegenlicht; '
     'oben im Bild viel ruhige Wandfläche. Kamera auf Brusthöhe, 50 mm.'),
    ('v4-portraet', 'hoch', 'weißes Hemd, oberster Knopf offen, sandfarbene Hose',
     'Porträt: Der Arzt sitzt entspannt auf der Kante des Schreibtischs, Arme locker verschränkt, schaut freundlich und ruhig '
     'direkt in die Kamera. Kamera frontal auf Augenhöhe, 85 mm, Hintergrund weich unscharf.'),
    ('v4-sportmedizin', 'quer', 'hellblaues Hemd, sandfarbene Hose',
     'Über die Schulter des Patienten fotografiert: vorne links unscharf die Schulter eines jungen Läufers, der auf der Liege sitzt. '
     'Der Arzt sitzt RECHTS im Bild auf einem Hocker, frontal zur Kamera, und tastet mit beiden Händen das Knie ab, konzentrierter Blick. 50 mm.'),
    ('v4-leistungsdiagnostik', 'quer', 'weißes Hemd, sandfarbene Hose',
     'In der Raumecke steht ein Fahrradergometer. Kamera schräg von hinten hinter der Sportlerin; der Arzt steht auf der rechten Seite '
     'des Ergometers, im Profil, und hält ein kleines Laktatmessgerät. Ruhige Konzentration. 35 mm.'),
    ('v4-sport-reha', 'quer', 'dunkelblaues Hemd, sandfarbene Hose',
     'Vogelperspektive direkt von oben: die Hände des Arztes führen das Knie einer Patientin, die auf der cognacfarbenen Liege liegt, '
     'in eine vorsichtige Beugung. Man sieht Hände, Unterarme, Knie, Leder und Eichenboden; das Gesicht des Arztes nur angeschnitten am Bildrand.'),
    ('v4-arthrose', 'quer', 'hellblaues Hemd, sandfarbene Hose',
     'Nahaufnahme: ein Ultraschallkopf mit etwas Gel liegt am Knie eines sitzenden Patienten; dahinter unscharf der Arzt, der auf einen '
     'kleinen Monitor schaut. Der Arzt sitzt LINKS HINTEN, der Patient ist nur als Bein im Vordergrund zu sehen. 85 mm.'),
    ('v4-allgemein', 'quer', 'weißes Hemd, sandfarbene Hose, Stethoskop um den Hals',
     'Halbtotale von der Tür aus: der Arzt sitzt RECHTS am Eichentisch, zugewandt, im Gespräch; ein Patient um die 60 sitzt links '
     'mit dem Rücken zur Kamera, leicht unscharf. Nachmittagslicht vom Fenster. 35 mm.'),
    ('v4-befund', 'quer', 'dunkelblaues Hemd, sandfarbene Hose',
     'Frontal über den Eichentisch fotografiert: der Arzt erklärt am Kniemodell, zeigt mit einem Stift; vorne rechts unscharf die '
     'Schulter und der Hinterkopf eines jungen Patienten. Warmes Licht. 50 mm.'),
    ('v4-ultraschall', 'quer', 'weißes Hemd, sandfarbene Hose',
     'Kamera am Fußende der Liege, niedrig: im Vordergrund der Fuß eines Sportlers, der Arzt sitzt dahinter frontal und untersucht '
     'das Sprunggelenk mit dem Ultraschallkopf, Blick auf das Gerät neben ihm. 50 mm.'),
]
DETAILS = [
    ('v4-detail-tisch', 'quer',
     'Stillleben ohne Menschen: auf dem Eichentisch ein Kniemodell, ein Stethoskop, ein ledergebundenes Notizbuch und ein Füller, '
     'Morgenlicht streift von links über den Tisch. Nahaufnahme, 85 mm.'),
]


def lauf(args, ziel):
    if ziel.exists():
        print('vorhanden:', ziel.name, flush=True); return
    for versuch in range(3):
        r = subprocess.run([sys.executable, BILD] + args + ['-o', str(ziel)], capture_output=True, text=True)
        if r.returncode == 0 and ziel.exists():
            print('fertig:', ziel.name, time.strftime('%H:%M:%S'), flush=True); return
        print('Fehler (%d) %s: %s' % (versuch + 1, ziel.name, (r.stderr or r.stdout)[-300:]), flush=True)
        time.sleep(40)


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(2) as ex:
        ex.submit(lauf, ['neu', '--format', 'quer', '--qualitaet', 'high',
                         STIL + RAUM + 'Leerer Raum ohne Menschen, Morgenlicht fällt durch das Fenster auf Liege und Dielen. '
                         'Totale aus der Raumecke, 24 mm, ruhig und aufgeräumt.'], RAUM_BILD)
        for datei, fmt, szene in DETAILS:
            ex.submit(lauf, ['neu', '--format', fmt, '--qualitaet', 'high', STIL + RAUM + szene], ZIEL / (datei + '.png'))
    if not RAUM_BILD.exists():
        sys.exit('Raumbild fehlt, Abbruch.')
    with ThreadPoolExecutor(4) as ex:
        for datei, fmt, kleidung, szene in SZENEN:
            prompt = STIL + ARZT_TXT + 'Er trägt ' + kleidung + '. ' + RAUM + RAUM_REF + szene
            ex.submit(lauf, ['edit', '--format', fmt, '--qualitaet', 'high', ARZT, str(RAUM_BILD), prompt],
                      ZIEL / (datei + '.png'))
    print('--- Serie v4 fertig', time.strftime('%H:%M:%S'), flush=True)


if __name__ == '__main__':
    main()
