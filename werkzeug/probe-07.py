#!/usr/bin/env python3
"""Probe v5 (26.09.): Raum = Davids Referenzbild ohne Poster; realistische Fotosprache statt Magazin-Stil."""
import pathlib, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

B = pathlib.Path.home() / 'dr-pfeiler-site'
Z = B / 'entwuerfe' / 'szenen-v5c'
GESICHT = str(B / 'vorlagen' / 'stil' / 'pfeiler-gesicht.png')
RAUM = str(B / 'vorlagen' / 'stil' / 'raum-ohne-poster.png')

FEST = '''Create a NEW photograph with a completely different camera position, composition and action than the reference images. Do NOT reproduce the reference composition, the reflex hammer or the patient in the grey T-shirt.
Image 1 is only a reference for the doctor's face. Image 2 is only a reference for the room and its furniture.
Photorealistic candid photograph taken during a real appointment in a small German private medical practice.
Same doctor as in image 1: same face, facial features, white hair, age around 70, same build. Do not change his face or identity.
Same room as in image 2: white walls, window with white horizontal blinds, grey-white shelf with folded towels and green dumbbells, simple desk, grey treatment couch, potted plant. No posters or anatomy charts: the walls are plain and empty.
Natural, unstaged moment; nobody looks at the camera. Ordinary daylight from the window mixed with ceiling light, neutral colour balance, no colour grading.
Real textures: visible skin pores and wrinkles, slight redness, creased shirt fabric, a few everyday objects in the room. Slight imperfections, not polished, not an advertisement, not stock photography.
Shot on a full-frame camera, 35mm lens, f/2.8, eye level unless stated otherwise. No text, no logos.
'''
SZENEN = [
    ('p1-raum-rechts', 'The doctor, wearing a light blue shirt with sleeves rolled up and beige trousers, sits on a stool on the RIGHT side of the frame, facing left, and presses gently on the outer knee of a young female runner who sits on the couch on the left. Camera from the window side, so the room is seen from the opposite angle to the reference.'),
    ('p2-ultraschall', 'The doctor, wearing a white shirt, holds an ultrasound probe on the ankle of a man lying on the couch; he looks at the small ultrasound screen on a cart. Camera placed low near the foot end of the couch, doctor seen from the front in the middle of the frame.'),
    ('p3-gespraech', 'Over-the-shoulder shot from behind a middle-aged female patient sitting at the desk: the doctor, wearing a dark navy shirt, sits opposite her and explains something, one hand slightly raised. His face is sharp, her shoulder and hair are blurred in the foreground left.'),
    ('p4-stethoskop', 'Close-up, 50mm: the doctor, wearing a white shirt and a stethoscope, listens to the back of a seated older man. The doctor stands behind the patient on the left, head tilted, eyes lowered, concentrating. Shallow depth of field.'),
]

def lauf(name, szene):
    ziel = Z / (name + '.png')
    if ziel.exists(): return
    r = subprocess.run([sys.executable, str(B / 'werkzeug' / 'bild.py'), 'edit', '--format', 'quer', '--qualitaet', 'high',
                        GESICHT, RAUM, 'MAIN ACTION (most important, must be clearly visible): ' + szene + '\n\n' + FEST + '\nRepeat: the image must show exactly this action: ' + szene, '-o', str(ziel)], capture_output=True, text=True)
    print(name, 'ok' if ziel.exists() else 'FEHLER ' + (r.stderr or r.stdout)[-400:], flush=True)

Z.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(4) as ex:
    for n, s in SZENEN: ex.submit(lauf, n, s)
