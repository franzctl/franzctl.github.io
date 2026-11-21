# franzctl.github.io

Meine persönliche Website: https://franzctl.github.io

## Aufbau

- `site/` enthält die Seite: reines HTML und CSS, ohne Framework, ohne JavaScript, ohne Anfragen an fremde Server.
- `projekte.json` enthält die Texte zu meinen Projekten.
- `scripts/projekte.py` baut daraus und aus meinen öffentlichen Repos die Projektliste.
- `.github/workflows/pages.yml` prüft die Seite und rollt sie aus.
- `.github/dependabot.yml` hält die verwendeten Actions aktuell.

## Rollout

1. Der Workflow startet bei jedem Push auf `main`, einmal täglich und auf Knopfdruck.
2. Der erste Job stellt die Seite zusammen und schreibt Commit und Datum in die Fußzeile. Dann holt `projekte.py` meine Repos über die GitHub-API und erzeugt die Projektliste. Zum Schluss prüft html-validate das HTML. Schlägt ein Schritt fehl, geht nichts live.
3. Der zweite Job veröffentlicht das geprüfte Ergebnis auf GitHub Pages.

## Neues Projekt

- **Nur ein neues Repo anlegen:** Beim nächsten täglichen Lauf erscheint es auf der Seite, mit seiner Beschreibung und seinen Topics von GitHub. Sofort geht es über Actions → „Website prüfen und ausrollen“ → „Run workflow“.
- **Mit eigenem Text:** einen Eintrag in `projekte.json` ergänzen. Der Name unter `repo` verknüpft den Eintrag automatisch, sobald es ein Repo mit diesem Namen gibt. Bis dahin zeigt die Seite den Status aus `status`, also `folgt` oder `arbeit`.
- Forks, archivierte Repos und das Profil-Repo erscheinen nicht.

GitHub pausiert geplante Läufe, wenn in einem Repo 60 Tage lang nichts passiert. Dann reicht ein Push oder „Run workflow“, um sie wieder zu starten.

## Sicherheit

- Die Actions sind auf Commit-Hashes festgelegt statt auf Tags, die sich nachträglich verschieben lassen.
- Jeder Job bekommt nur die Rechte, die er braucht: Bauen darf nur lesen, nur der Ausroll-Job darf auf Pages schreiben.
- Eine Content-Security-Policy erlaubt nur Inhalte von der eigenen Seite.
- Die Schrift Overpass liegt selbst gehostet im Repo (SIL Open Font License, siehe `site/fonts/OFL.txt`), dadurch gibt es keine Anfragen an Dritte.

## Lokal ansehen

```bash
python3 -m http.server --directory site 8000
```

Danach http://localhost:8000 im Browser öffnen. Direkt als Datei geöffnet, blockiert die Content-Security-Policy je nach Browser Schrift und Stylesheet. Commit, Datum und Projektliste stehen lokal als Platzhalter, sie werden erst beim Rollout eingesetzt.
