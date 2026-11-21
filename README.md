# franzctl.github.io

Meine persönliche Website: https://franzctl.github.io

## Aufbau

- `site/` enthält die Seite: reines HTML und CSS, ohne Framework, ohne JavaScript, ohne Anfragen an fremde Server.
- `.github/workflows/pages.yml` prüft die Seite und rollt sie bei jedem Push auf `main` aus.
- `.github/dependabot.yml` hält die verwendeten Actions aktuell.

## Rollout

1. Ein Push auf `main` startet den Workflow.
2. Der erste Job stellt die Seite zusammen, schreibt Commit und Datum in die Fußzeile und prüft das HTML mit html-validate. Schlägt die Prüfung fehl, geht nichts live.
3. Der zweite Job veröffentlicht das geprüfte Ergebnis auf GitHub Pages.

## Sicherheit

- Die Actions sind auf Commit-Hashes festgelegt statt auf Tags, die sich nachträglich verschieben lassen.
- Jeder Job bekommt nur die Rechte, die er braucht: Bauen darf nur lesen, nur der Ausroll-Job darf auf Pages schreiben.
- Eine Content-Security-Policy erlaubt nur Inhalte von der eigenen Seite.
- Die Schrift Overpass liegt selbst gehostet im Repo (SIL Open Font License, siehe `site/fonts/OFL.txt`), dadurch gibt es keine Anfragen an Dritte.

## Lokal ansehen

```bash
python3 -m http.server --directory site 8000
```

Danach http://localhost:8000 im Browser öffnen. Direkt als Datei geöffnet, blockiert die Content-Security-Policy je nach Browser Schrift und Stylesheet. Commit und Datum stehen lokal als Platzhalter, sie werden erst beim Rollout eingesetzt.
