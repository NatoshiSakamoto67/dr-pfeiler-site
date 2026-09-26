# Recherche Mobil-Design (26.09.2026)

Kernaussagen mit Zahlen; Quellen siehe Links.

## Header (oben)
- 56–64 px hoch, nicht mehr (Material 3, iOS 44 pt). https://m3.material.io/components/app-bars/guidelines
- Nur Praxisname, Telefon-Icon, Menü. Anruf bleibt Kanal Nr. 1.
- Sticky, aber auto-hide beim Runterscrollen, sofort zurück beim Hochscrollen (NN/g). https://www.nngroup.com/articles/sticky-headers/
- Opak sobald gescrollt; transparent nur über dem Hero mit dunklem Verlauf.
- Höhe in px, nicht rem/vh; mit 200 % Zoom testen.

## Untere Leiste
- Thumb Zone: 75 % bedienen mit dem Daumen → Primär-CTAs unten. https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/
- Sticky-CTA unten gewinnt in 36 % der Tests, oben nur 13 % (Online Dialogue, 33 Tests). Auf Startseiten nur mit genau zwei Aktionen. https://www.onlinedialogue.nl/en/blogs/sticky-cta-guaranteed-conversion-uplift/
- Buttons ≥ 44×44 px (Apple), ≥ 1 cm (NN/g). padding-bottom: max(12px, env(safe-area-inset-bottom)); viewport-fit=cover; 100dvh statt 100vh.
- Erscheint erst, wenn der Hero-CTA aus dem Bild ist; verschwindet am Kontaktblock.
- Premium: schwebende Pille, inset 12–16 px, Radius ≥ 24 px, blur 16–20 px, aber ≥ 85 % Deckung für 50+ (Kontrast).

## Typografie 50+
- Fließtext ≥ 18 px (GOV.UK 19 px, NHS 19 px), nie unter 16. https://design-system.service.gov.uk/styles/paragraphs
- Zeilenhöhe 1,5–1,6; Zeilenlänge mobil 35–45 Zeichen ist korrekt.
- Kontrast ≥ 7:1 für Fließtext; kein Hellgrau auf Weiß. https://www.nngroup.com/articles/usability-for-senior-citizens/
- Sans für Fließtext; Serif nur für Überschriften ≥ 28 px (ab 14 pt kein Unterschied, darunter lesen Ältere Serifen langsamer).

## Schriftgrößen-Schalter
- Kein Anti-Pattern, aber zweite Wahl. GOV.UK/NHS haben keinen; Charité hat einen.
- Empfehlung: alles in rem, kein user-scalable=no; optional EIN Schalter „Große Schrift“ (html 100 → 125 %) im Menü, nicht im Header.

## Dark Mode
- Forschung: Light Mode gewinnt bei Lesbarkeit in allen Altersgruppen (Piepenbrock 2013), Astigmatismus verschlechtert Dunkel. https://www.nngroup.com/articles/dark-mode/
- Empfehlung Praxis 50+: kein Dark Mode, kein Schalter; warmes Off-White statt Reinweiß.

## Konversion
- 94 % suchen Kontakt/Zeiten/Anfahrt, 90 % Leistungen, 78 % Vorstellung des Arztes (DE, n=1000). https://www.flemming-dental.de/presse/der-erste-eindruck-zaehlt-worauf-patienten-bei-einer-praxiswebsite-wert-legen/
- 65+: 91 % wollen, dass Telefon bleibt (Doctolib/YouGov 2024).
- Vertrauensblock: Foto + Name + Facharzt + Qualifikationen. Notfallzeile 112 / 116 117. Kosten-Transparenz (BÄK GOÄ-Ratgeber).
- Hero ≤ 65 vh, kein Vollbild; Headline ≤ 2 Zeilen, 1 Satz, 2 Buttons im ersten Screen. https://www.nngroup.com/articles/scrolling-and-attention/

## Referenzen
Lanserhof, The London Clinic (Telefon im Header, Trust-Leiste), Pyramide Zürich, Hirslanden (Notfallnummer), Aleris (Ablauf „So werden Sie Patient“), Cleveland Clinic (Anruf + Termin als Doppel-CTA).
