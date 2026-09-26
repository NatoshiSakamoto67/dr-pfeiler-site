#!/usr/bin/env python3
"""Serie v6 (26.09.): Davids Raum ohne Poster, aber aus allen Richtungen fotografiert.

Der Raum ist einmal fest beschrieben (vier Wände), damit jede Blickrichtung zusammenpasst.
Jede Szene legt Blickrichtung, Lichtseite, Kamerahöhe, Bildausschnitt und eine kleine Unregelmäßigkeit fest.
"""
import pathlib, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

B = pathlib.Path.home() / 'dr-pfeiler-site'
Z = B / 'entwuerfe' / 'szenen-v6'
GESICHT = str(B / 'vorlagen' / 'stil' / 'pfeiler-gesicht.png')
RAUM = str(B / 'vorlagen' / 'stil' / 'raum-ohne-poster.png')

RAUMPLAN = '''THE ROOM (always the same room, image 2 shows only ONE of its walls):
- Window wall: wide window with white horizontal blinds, radiator below, potted plant on the sill.
- Door wall (opposite the window): plain white wooden door with a brushed steel handle, a coat hook with a dark jacket next to it, a light switch, a small white sink with a soap dispenser and a paper towel holder.
- Couch wall: grey-white open shelf with folded white towels and green dumbbells, grey treatment couch with paper roll in front of it.
- Desk wall (opposite the couch): simple white desk with a computer monitor, keyboard, a few folders, a desk lamp, an office chair, a grey filing cabinet.
Walls are plain white with NO posters, NO pictures, NO charts. Light grey vinyl floor.
'''
FOTO = '''PHOTO STYLE: photorealistic candid photo taken during a real appointment by a practice assistant, not a professional shoot, not an advertisement, not stock photography.
Nobody looks at the camera. Real textures: skin pores, wrinkles, age spots, creased fabric, slightly messy desk, a used paper towel, a coffee mug.
Built-in imperfections: horizon tilted by about 2 degrees, composition slightly off-centre, one part of the frame slightly out of focus, mild sensor noise, no retouching, no colour grading, ordinary white balance.
The doctor is the same man as in image 1: same face, white hair, age around 70. Do not change his face. No text, no logos.
'''

# (datei, format, szene)
SZENEN = [
    ('v6-tuer', 'quer', 'LOOKING TOWARDS THE DOOR WALL: the door, coat hook and sink fill the background. The doctor, in a navy shirt, stands in the doorway half-turned, shaking hands with a young woman in a sports jacket who is just arriving. Window is behind the camera, so soft light falls on their faces from the front. Camera at chest height, 35mm, both people small in frame, lots of room visible.'),
    ('v6-schulter', 'quer', 'ONLY THE DOCTOR\'S SHOULDER AND HAND in the blurred foreground on the left edge (light blue shirt), his face is NOT visible. Sharp focus on the knee of a teenage football player sitting on the couch, the doctor\'s hand bending the knee. Background: the shelf with towels. Light from the RIGHT (window on the right side of the frame). Camera slightly from above, 50mm, shallow depth of field.'),
    ('v6-von-unten', 'quer', 'LOW ANGLE from knee height: the doctor, in a white shirt, stands and holds a patient\'s arm, testing the shoulder of a man in his 40s who sits on the couch. Behind them the DESK WALL with computer monitor and filing cabinet. Window light from the LEFT, hard light with visible shadows on the wall. 28mm, doctor appears tall and large in frame.'),
    ('v6-von-oben', 'quer', 'HIGH ANGLE, camera held above head height looking down: the doctor, in a navy shirt, kneels on the floor and tapes the ankle of a female runner who sits on the couch. Grey vinyl floor, a sports bag and running shoes on the floor. Window light from the RIGHT. 35mm, doctor medium size.'),
    ('v6-schreibtisch', 'quer', 'LOOKING TOWARDS THE DESK WALL: the doctor, in a white shirt, sits at his desk and shows an older couple something on the computer monitor, pointing with a pen. Seen from behind the couple, their backs and heads partly in the frame. Window on the LEFT side, afternoon light. Eye level, 35mm, doctor small-medium in frame, a coffee mug and folders on the desk.'),
    ('v6-ultraschall', 'quer', 'Ultrasound of the knee: the doctor, in a light blue shirt, sits on a stool on the RIGHT, holding the probe on the knee of a woman lying on the couch; the ultrasound machine on a cart stands between camera and couch, partly blocking the view and slightly out of focus in the foreground. Window light from the RIGHT. 50mm, eye level.'),
    ('v6-waschbecken', 'quer', 'LOOKING TOWARDS THE DOOR WALL: the doctor, in a white shirt with sleeves rolled up, washes his hands at the small sink while talking over his shoulder to a patient who sits on the couch in the foreground, blurred. Light from the window behind the camera. 35mm, doctor in the middle distance, seen from behind at three-quarter angle.'),
    ('v6-fenster-gegenlicht', 'quer', 'LOOKING TOWARDS THE WINDOW WALL, BACKLIGHT: the doctor, in a navy shirt, stands at the window and listens to the chest of a seated young man with a stethoscope; bright window behind them, faces slightly darker, blinds half open with stripes of light on the floor. Camera at seated height, 50mm, window slightly overexposed.'),
    ('v6-portraet-hoch', 'hoch', 'Informal portrait, vertical: the doctor, in a white shirt, leans with one hip against the edge of the desk, arms loosely crossed, looking slightly past the camera with a calm, friendly expression. Behind him the DOOR WALL with the door slightly open. Light from the window on the LEFT. 85mm, chest-up, not symmetrical.'),
    ('v6-hero-hoch', 'hoch', 'Vertical: the doctor, in a navy shirt, walks through the door into the room, holding a patient file, seen from inside the room at a slight low angle. The door frame and the coat hook with the jacket are visible. Light from the window on the RIGHT falling across his face. 35mm, full figure, doctor fairly small in the upper part of the frame, lots of floor.'),
    ('v6-hero-quer', 'quer', 'Wide establishing shot from the corner between window wall and desk wall: the doctor, in a navy shirt, stands next to the treatment couch and talks with a middle-aged male patient who sits on it; the door and sink are visible at the far end of the room. Window light from the LEFT. 24mm, both people small in the frame, lots of room, slight wide-angle distortion at the edges.'),
    ('v6-leistung', 'quer', 'Performance test: a female cyclist on a stationary ergometer bike placed in front of the SHELF with dumbbells; the doctor, in a white shirt, stands on the RIGHT and pricks her earlobe for a lactate drop, a small lactate meter in his other hand. Camera slightly from below, 35mm, window light from the LEFT, the doctor partly cut off by the right frame edge.'),
]


def lauf(name, fmt, szene):
    ziel = Z / (name + '.png')
    if ziel.exists():
        return
    prompt = ('MAIN ACTION AND CAMERA (most important, must be followed exactly):\n' + szene + '\n\n' + RAUMPLAN + '\n' + FOTO +
              '\nImage 1 is only a reference for the doctor\'s face, image 2 only for the room\'s furniture and colours. '
              'Create a NEW photograph with this camera direction; do NOT copy the composition of image 2.\n'
              'Repeat, the photo must show: ' + szene)
    for versuch in range(4):
        r = subprocess.run([sys.executable, str(B / 'werkzeug' / 'bild.py'), 'edit', '--format', fmt, '--qualitaet', 'high',
                            GESICHT, RAUM, prompt, '-o', str(ziel)], capture_output=True, text=True)
        if ziel.exists():
            print('fertig:', name, time.strftime('%H:%M:%S'), flush=True); return
        print('Fehler', name, (r.stderr or r.stdout)[-200:], flush=True)
        time.sleep(45)


Z.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(2) as ex:
    for n, f, s in SZENEN:
        ex.submit(lauf, n, f, s)
print('--- Serie v6 fertig', time.strftime('%H:%M:%S'), flush=True)
