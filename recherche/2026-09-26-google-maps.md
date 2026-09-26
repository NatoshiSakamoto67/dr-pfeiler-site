# Recherche Google Maps DSGVO (26.09.2026) — keine Rechtsberatung

## Rechtslage
- Google-Maps-iframe ohne Einwilligung: unzulässig. Beim Laden fließen IP, Browserdaten, Referrer an Google und das NID-Cookie wird gesetzt (§ 25 Abs. 1 TDDDG, Art. 6 Abs. 1 lit. a DSGVO).
- LG München I, 20.01.2022, 3 O 17493/20 (Google Fonts) gilt als Analogie. DSK-Orientierungshilfe Telemedien nennt Kartendienste ausdrücklich. LfDI Baden-Württemberg empfiehlt die Zwei-Klick-Lösung.
- Es gibt KEINEN cookiefreien Embed-Modus (anders als youtube-nocookie). DPF-Zertifizierung löst nur das Drittland-Problem, nicht die Einwilligung.
- Ein oft zitiertes „LG Frankfurt 2-03 O 15/22“ war nicht verifizierbar; nicht darauf stützen.

## Empfehlung
Statisches, selbst gehostetes Kartenbild (OSM mit Attribution) + Routen-Buttons ohne Datenfluss, darunter Zwei-Klick „Interaktive Google-Karte laden“. Einwilligung standardmäßig NICHT in localStorage merken, damit „keine Cookies, kein Storage“ wahr bleibt.

## URLs
- Route (kein Key nötig): https://www.google.com/maps/dir/?api=1&destination=52.27784%2C10.52268&travelmode=driving — öffnet auf dem Handy die Google-Maps-App. https://developers.google.com/maps/documentation/urls/get-started
- Apple: https://maps.apple.com/?daddr=Hamburger+Stra%C3%9Fe+277%2C+38114+Braunschweig&dirflg=d — Adresse als Text, nicht Koordinaten.
- Embed API (kostenlos, unbegrenzt, aber Cloud-Rechnungskonto nötig, Key per HTTP-Referrer beschränken): https://www.google.com/maps/embed/v1/place?key=KEY&q=Hamburger+Stra%C3%9Fe+277%2C+38114+Braunschweig&zoom=16&language=de&region=DE
- Ohne Konto: „Teilen > Karte einbetten“ liefert eine pb=…-URL, nicht parametrisierbar, kann brechen.
- iframe: title Pflicht, referrerpolicy="strict-origin-when-cross-origin", kein sandbox. Kein Farbfilter über das Embed (Google Geo-Richtlinien); abgerundete Ecken sind ok.

## WICHTIG: Google-Eintrag der Praxis
Alle Verzeichnisse (arzt-auskunft.de, diebestenderstadt.de, 11880) führen die Praxis noch unter Steinweg 20, 38100 Braunschweig, Tel. 0531 12944633. Unter Hamburger Straße 277 gibt es keinen Pfeiler-Eintrag. → Google-Unternehmensprofil auf die neue Adresse umziehen (business.google.com). Bis dahin keine destination_place_id verwenden, sonst führt die Route zum alten Standort.

## Datenschutz-Absatz (Muster, paraphrasiert nach eRecht24/AdSimple)
Google Maps (Zwei-Klick-Einbindung): Anbieter Google Ireland Limited, Gordon House, Barrow Street, Dublin 4. Beim Seitenaufruf keine Übermittlung; erst der Klick auf „Karte laden“ ist die Einwilligung (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG); dabei IP, Browserdaten, aufgerufene Seite an Google, Cookies (NID) möglich; Übermittlung an Google LLC/USA, zertifiziert nach EU-US Data Privacy Framework (Angemessenheitsbeschluss 10.07.2023), ergänzend Standardvertragsklauseln. Widerruf durch Neuladen/„Karte ausblenden“. Links: https://policies.google.com/privacy , https://www.google.com/intl/de/help/terms_maps/ . Routen-Links führen auf externe Angebote.

## Quellen
https://www.e-recht24.de/dsg/12664-google-maps.html · https://www.it-recht-kanzlei.de/google-maps-cookies-einwilligungspflicht.html · https://www.dr-datenschutz.de/wie-kann-google-maps-dsgvo-konform-eingebunden-werden/ · https://www.baden-wuerttemberg.datenschutz.de/faq-zu-cookies-und-tracking-2/ · https://www.datenschutzkonferenz-online.de/media/oh/20211220_oh_telemedien.pdf · https://developers.google.com/maps/documentation/embed/usage-and-billing · https://developers.google.com/maps/api-security-best-practices · https://about.google/brand-resource-center/products-and-services/geo-guidelines/
