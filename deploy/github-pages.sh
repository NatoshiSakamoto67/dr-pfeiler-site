#!/bin/zsh
# Veröffentlicht den Entwurf (nur web/, nur genutzte Bilder) als GitHub Pages.
# Öffentliches Repo nötig (Pages auf privaten Repos gibt es nur im bezahlten Plan). Seiten tragen noindex.
set -e
# Seiten und Bilder frisch aus web/ übernehmen (auch die, die nur im Stylesheet stehen, z. B. die Ottocento-Wand)
D=~/dr-pfeiler-site/deploy/github-pages
mkdir -p $D/assets/img $D/assets/css $D/assets/js $D/assets/fonts
# nur veröffentlichen, was die Seite wirklich nutzt: alte Bilder, Seiten und Schriften vorher entfernen
find $D/assets/img $D/assets/fonts -type f -delete
find $D -maxdepth 1 -name '*.html' -type f -delete
cp ~/dr-pfeiler-site/web/*.html $D/
cp ~/dr-pfeiler-site/web/assets/css/edel.css $D/assets/css/
cp ~/dr-pfeiler-site/web/assets/js/edel.js $D/assets/js/
for f in $(grep -ohE "fonts/[a-z0-9-]+\\.woff2" ~/dr-pfeiler-site/web/assets/css/edel.css | sed 's#fonts/##' | sort -u); do cp ~/dr-pfeiler-site/web/assets/fonts/$f $D/assets/fonts/; done
for f in $(grep -ohE "img/[a-z0-9-]+\.webp" ~/dr-pfeiler-site/web/*.html ~/dr-pfeiler-site/web/assets/css/edel.css | sed 's#img/##' | sort -u); do cp ~/dr-pfeiler-site/web/assets/img/$f $D/assets/img/; done
cd $D
[ -d .git ] || git init -q -b main
git add -A
git -c user.name="David Davidoff" -c user.email="9yth6grfpq@privaterelay.appleid.com" commit -q -m "Entwurf Stand $(date +%d.%m.%Y)" || true
if ! git remote get-url origin >/dev/null 2>&1; then
  gh repo create dr-pfeiler-entwurf --public --source=. --push --description "Entwurf Website Privatpraxis Dr. med. Günter Pfeiler (noindex)"
  gh api -X POST repos/NatoshiSakamoto67/dr-pfeiler-entwurf/pages -f build_type=legacy -f 'source[branch]=main' -f 'source[path]=/' >/dev/null
else
  git push -q origin main
fi
echo "Link: https://natoshisakamoto67.github.io/dr-pfeiler-entwurf/"
