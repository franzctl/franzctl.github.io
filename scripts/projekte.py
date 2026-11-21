#!/usr/bin/env python3
"""Erzeugt die Projektliste der Website aus projekte.json und den öffentlichen GitHub-Repos.

Aufruf:  python3 scripts/projekte.py projekte.json _site/index.html franzctl

- Einträge aus projekte.json werden verlinkt, sobald es ein Repo mit dem Namen unter "repo" gibt.
  Gibt es das Repo noch nicht, zeigt die Seite den Status aus "status" ("folgt" oder "arbeit").
- Öffentliche Repos ohne Eintrag kommen automatisch dazu, mit ihrer Beschreibung von GitHub.
- Forks, archivierte Repos und das Profil-Repo werden übersprungen.

Zum Testen ohne Netz liest das Skript die Repo-Liste aus der Datei in REPOS_JSON.
Ist die GitHub-API nicht erreichbar, bricht es ab, damit keine halbe Liste live geht.
"""

import html
import json
import os
import sys
import urllib.error
import urllib.request

START = "<!-- PROJEKTE:START -->"
ENDE = "<!-- PROJEKTE:ENDE -->"
STATUS_TEXT = {"online": "auf GitHub", "folgt": "Repo folgt", "arbeit": "in Arbeit"}


def repos_holen(benutzer):
    """Liefert die öffentlichen Repos des Benutzers (bis 100 Stück, das reicht hier)."""
    testdatei = os.environ.get("REPOS_JSON")
    if testdatei:
        with open(testdatei, encoding="utf-8") as f:
            return json.load(f)

    url = f"https://api.github.com/users/{benutzer}/repos?per_page=100&type=owner&sort=pushed"
    anfrage = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": f"{benutzer}-website",
    })
    token = os.environ.get("GH_TOKEN")
    if token:
        anfrage.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(anfrage, timeout=30) as antwort:
            return json.load(antwort)
    except urllib.error.URLError as fehler:
        sys.exit(f"GitHub-API nicht erreichbar: {fehler}")


def eintrag_html(titel, url, status, text, technik):
    e = html.escape
    titel_html = f'<a href="{e(url)}">{e(titel)}</a>' if url else e(titel)
    zeilen = [
        '      <li class="projekt">',
        '        <div class="projekt-kopf">',
        f"          <h3>{titel_html}</h3>",
        f'          <p class="status status-{status}">{STATUS_TEXT[status]}</p>',
        "        </div>",
        '        <div class="projekt-text">',
    ]
    if text:
        zeilen.append(f"          <p>{e(text)}</p>")
    if technik:
        zeilen.append(f'          <p class="technik">{e(technik)}</p>')
    zeilen += ["        </div>", "      </li>"]
    return "\n".join(zeilen)


def main():
    if len(sys.argv) != 4:
        sys.exit("Aufruf: projekte.py <projekte.json> <index.html> <github-benutzer>")
    datei_projekte, datei_html, benutzer = sys.argv[1:]

    with open(datei_projekte, encoding="utf-8") as f:
        gepflegt = json.load(f)

    repos = {
        r["name"]: r
        for r in repos_holen(benutzer)
        if not r.get("fork") and not r.get("archived") and r["name"] != benutzer
    }

    eintraege = []
    for p in gepflegt:
        repo = repos.pop(p.get("repo", ""), None)
        if repo:
            status, url = "online", repo["html_url"]
        else:
            status, url = p.get("status", "folgt"), None
        eintraege.append(eintrag_html(p["titel"], url, status, p.get("text", ""), p.get("technik", "")))
        print(f"{STATUS_TEXT[status]:<11} {p['titel']}")

    # Neue Repos ohne Eintrag in projekte.json, das zuletzt geänderte zuerst
    for repo in sorted(repos.values(), key=lambda r: r.get("pushed_at") or "", reverse=True):
        technik = ", ".join(repo.get("topics") or []) or (repo.get("language") or "")
        eintraege.append(eintrag_html(repo["name"], repo["html_url"], "online", repo.get("description") or "", technik))
        print(f"{'neu':<11} {repo['name']}")

    with open(datei_html, encoding="utf-8") as f:
        seite = f.read()
    anfang, marke_start, rest = seite.partition(START)
    _, marke_ende, schluss = rest.partition(ENDE)
    if not marke_start or not marke_ende:
        sys.exit(f"Die Marken {START} und {ENDE} fehlen in {datei_html}")

    with open(datei_html, "w", encoding="utf-8") as f:
        f.write(anfang + START + "\n" + "\n".join(eintraege) + "\n      " + ENDE + schluss)


if __name__ == "__main__":
    main()
