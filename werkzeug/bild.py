#!/usr/bin/env python3
"""Bilder für die Pfeiler-Seite über die OpenAI-Bild-API (Key aus ~/.config/openai/key).

  bild.py neu  "Prompt"            -o ziel.png [--format quer|hoch|quadrat] [--modell M] [--stil]
  bild.py edit vorlage.jpg "Prompt" -o ziel.png [--format ...]   # Foto als Grundlage, gleiches Motiv
  bild.py webp ziel.png            # -> ziel.webp (Breite 1536)
"""
import argparse, base64, json, pathlib, subprocess, sys, urllib.request

KEY = pathlib.Path.home().joinpath('.config/openai/key').read_text().strip()
MODELL = 'gpt-image-2.5-flare'
GROESSE = {'quer': '1536x1024', 'hoch': '1024x1536', 'quadrat': '1024x1024'}
STIL = ('Ruhiges Stillleben im Stil der bestehenden Praxis-Illustrationen: warmes, cremefarbenes Papier als Hintergrund, '
        'weiches Tageslicht, matte Objekte in Elfenbein, Sand und Anthrazit (kein Petrol, kein Blau, kein Gold), '
        'leichter Ottocento-Anklang wie eine Kupferstich-Vorlage des 19. Jahrhunderts, aber fotorealistisch gerendert. '
        'Keine Menschen, keine Schrift, keine Logos. ')

def anfrage(url, data=None, felder=None, dateien=None):
    """Über curl statt urllib: die python.org-Installation kennt die System-Zertifikate nicht."""
    cmd = ['curl', '-sS', '--max-time', '300', url, '-H', 'Authorization: Bearer ' + KEY]
    if dateien:
        for k, v in felder.items():
            cmd += ['-F', '%s=%s' % (k, v)]
        for k, pfad in dateien:
            cmd += ['-F', '%s=@%s' % (k, pfad)]
    else:
        cmd += ['-H', 'Content-Type: application/json', '-d', json.dumps(data)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit('curl-Fehler: ' + r.stderr[:400])
    antwort = json.loads(r.stdout)
    if 'error' in antwort:
        sys.exit('API-Fehler: ' + json.dumps(antwort['error'])[:600])
    return antwort

def speichern(antwort, ziel):
    b64 = antwort['data'][0]['b64_json']
    pathlib.Path(ziel).write_bytes(base64.b64decode(b64))
    print('geschrieben:', ziel)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('befehl', choices=['neu', 'edit', 'webp'])
    ap.add_argument('args', nargs='*')
    ap.add_argument('-o', '--out')
    ap.add_argument('--format', default='quer', choices=GROESSE)
    ap.add_argument('--modell', default=MODELL)
    ap.add_argument('--qualitaet', default='high', choices=['low', 'medium', 'high'])
    ap.add_argument('--treue', action='store_true', help='input_fidelity=high: Gesicht der Vorlage fester halten')
    ap.add_argument('--stil', action='store_true', help='Stil-Vorspann der Praxis vor den Prompt setzen')
    a = ap.parse_args()

    if a.befehl == 'webp':
        for src in a.args:
            ziel = str(pathlib.Path(src).with_suffix('.webp'))
            subprocess.run(['cwebp', '-q', '82', '-resize', '1536', '0', src, '-o', ziel], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('geschrieben:', ziel)
        return
    if a.befehl == 'neu':
        prompt = (STIL if a.stil else '') + a.args[0]
        antwort = anfrage('https://api.openai.com/v1/images/generations',
                          {'model': a.modell, 'prompt': prompt, 'size': GROESSE[a.format], 'quality': a.qualitaet, 'n': 1})
    else:
        # edit: alle Argumente bis auf das letzte sind Vorlagen (Bild 1 = Hauptvorlage), das letzte ist der Prompt
        vorlagen, prompt = a.args[:-1], (STIL if a.stil else '') + a.args[-1]
        antwort = anfrage('https://api.openai.com/v1/images/edits',
                          felder={'model': a.modell, 'prompt': prompt, 'size': GROESSE[a.format],
                                  'quality': a.qualitaet, **({'input_fidelity': 'high'} if a.treue else {})},
                          dateien=[('image[]', v) for v in vorlagen])
    speichern(antwort, a.out or 'bild.png')
    if 'usage' in antwort: print('Tokens:', antwort['usage'].get('total_tokens'))

if __name__ == '__main__':
    main()
