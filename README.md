# NEON TETRIS – PWA

Das bestehende Tetris-Spiel als installierbare, offline nutzbare Progressive Web App
mit Steuerung über einen per Bluetooth verbundenen Gamecontroller.

## Dateien

| Datei | Zweck |
| --- | --- |
| `index.html` | Spiel, Gamepad-Logik, Installationshinweise, SW-Registrierung |
| `manifest.webmanifest` | App-Name, Icons, `display: standalone`, Start-URL |
| `sw.js` | Service Worker – hält die komplette App-Shell offline bereit |
| `icons/` | PNG-Icons (192/512/maskable/Apple Touch) und SVG-Favicon |
| `tools/generate-icons.py` | Erzeugt die PNG-Icons neu (`python3 tools/generate-icons.py`, benötigt Pillow) |

## Starten

Service Worker benötigen einen **sicheren Kontext**: HTTPS oder `localhost`.

Nur lokal testen:

```bash
cd /home/pb/Work/pwa-neo-tetris
python3 -m http.server 8080
# http://localhost:8080
```

Für das iPhone muss die Seite über **HTTPS** erreichbar sein (z. B. GitHub Pages,
Netlify, Cloudflare Pages, ein eigener Webserver mit TLS). `file://` funktioniert
nicht.

## Auf dem iPhone installieren

1. Die Seite in **Safari** öffnen (nicht im PWA-Fenster selbst).
2. Teilen-Button antippen (□ mit Pfeil nach oben).
3. **„Zum Home-Bildschirm“** → **„Hinzufügen“**.
4. App vom Home-Bildschirm starten. Sie läuft ohne Browserleiste und nach dem
   ersten Laden auch offline.

Der Button **„⤓ INSTALLIEREN“** in der App zeigt diese Anleitung an; unter
Android/Chrome löst er – sofern unterstützt – direkt die Installationsabfrage aus.
In der installierten Web App ist er ausgeblendet (der Share-Sheet ist dort nicht
erreichbar). Seit iOS 26 öffnet jeder per „Zum Home-Bildschirm“ hinzugefügte Link
automatisch als Web App, auch ohne Manifest.

## Ansicht auf dem iPhone

Der **Tunnel nimmt den verfügbaren Bildschirm ein**; alles andere ist auf Mini-
Anzeigen reduziert:

- **Portrait:** Eine schmale Mini-Leiste oben mit Score, Level, Linien, Bestwert
  sowie verkleinerten HOLD-/NEXT-Vorschauen; darunter das Board, darunter eine
  einzelne Reihe Touch-Buttons. Die Zellgröße berechnet sich aus Breite *und*
  Höhe des Viewports (inkl. Safe Area), sodass auch auf dem iPhone SE alles
  ohne Scrollen passt.
- **Landscape:** Das Board nutzt fast die komplette Höhe, die Mini-Anzeigen und
  Touch-Buttons stehen in einer schmalen Spalte rechts daneben. Titel und
  Statusleiste entfallen.
- Statusleiste, Notch und Home-Indikator werden über `viewport-fit=cover` und
  `env(safe-area-inset-*)` berücksichtigt. Wischen auf dem Board löst kein
  Scrollen/Zoomen aus; die App pausiert beim Verlassen der Seite.

## Gamecontroller

Die Steuerung nutzt die **Gamepad API** (`navigator.getGamepads()`). Es wird keine
Web-Bluetooth-Verbindung aus dem Browser aufgebaut: Der Controller wird ganz normal
in den Bluetooth-Einstellungen des Geräts gekoppelt; iOS/iPadOS reicht unterstützte
Controller (u. a. Xbox, PlayStation, Switch Pro, MFi) an die Webseite durch.
Andere, vom Apple Game Controller Framework nicht erkannte Controller erscheinen
nicht – Tastatur und Touch-Buttons bleiben immer als Fallback nutzbar.

Falls ein bereits gekoppelter Controller nicht sofort erkannt wird: **eine Taste
drücken** (weckt die Verbindung). Der Status oben in der App wechselt dann auf grün
und zeigt den Namen.

| Controller | Aktion |
| --- | --- |
| D-Pad links/rechts oder linker Stick | Stein bewegen (mit Wiederholung) |
| D-Pad runter oder linker Stick runter | Soft Drop |
| **A / Kreuz** | Hard Drop |
| **B / Kreis** (oder RB, D-Pad hoch) | Drehen ↻ |
| **Y / Dreieck** (oder LB) | Drehen ↺ |
| **X / Viereck** (oder LT) | Hold |
| **Start / Options** (oder Select/Share) | Start / Pause |

Getestet wird der Controller in `requestAnimationFrame` – auch während Pause und
Game Over, damit sich das Spiel jederzeit mit Start fortsetzen lässt.

## Offline & Aktualisieren

Beim ersten Online-Aufruf legt der Service Worker `index.html`, Manifest, Icons und
sich selbst im Cache `neon-tetris-v3` ab. Danach funktioniert das Spiel ohne Netz.
Nach Änderungen am Spiel die Versionsnummer `CACHE` in `sw.js` erhöhen; alte Caches
werden beim Aktivieren automatisch entfernt.
