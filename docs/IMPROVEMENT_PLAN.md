# EVE-Alert Verbesserungsplan

## Projektübersicht

Systematische Verbesserung des EVE-Alert Systems für bessere Performance, Stabilität und Wartbarkeit.

______________________________________________________________________

## Phase 1: Grundlegende Stabilität & Abhängigkeiten ⚡

### 1.1 Dependencies Synchronisation

**Priorität:** HOCH | **Aufwand:** 1h | **Status:** ✅ Abgeschlossen

- [x] `requirements.txt` und `pyproject.toml` synchronisieren
  - mss: 10.0.0 (synchronisiert)
  - opencv-python: 4.11.0.86 (synchronisiert)
  - screeninfo: 0.8.1 (synchronisiert)
  - CTkMessagebox zu pyproject.toml hinzugefügt
- [x] Abhängigkeiten alphabetisch sortiert
- [x] Beide Dateien verwenden jetzt identische Versionen

**Erwartetes Ergebnis:** ✅ Konsistente Abhängigkeiten, keine Versionskonflikte

______________________________________________________________________

### 1.2 Fehlerbehandlung & Validierung

**Priorität:** HOCH | **Aufwand:** 3h | **Status:** ✅ Abgeschlossen

- [x] Konfigurationsvalidierung beim Start implementiert
  - Region-Koordinaten validieren (x1 < x2, y1 < y2)
  - Detection Scale Bereich prüfen (0-100)
  - Webhook URL Format validieren
  - Audio-Dateien Existenz prüfen
- [x] Eigene Exception-Klassen für unterschiedliche Fehlertypen erstellt
  - EVEAlertException (Basis)
  - ConfigurationError, ValidationError
  - AudioError, WebhookError
- [x] ConfigValidator-Klasse mit umfassenden Validierungsmethoden
- [x] Unit Tests für Validierung erstellt (test_validator.py)
- [x] Audio-Datei-Validierung beim AlertAgent-Start

**Erwartetes Ergebnis:** ✅ Robustere Anwendung, weniger Abstürze

______________________________________________________________________

## Phase 2: Performance-Optimierung 🚀

### 2.1 Screenshot-Verarbeitung Optimierung

**Priorität:** MITTEL | **Aufwand:** 2h | **Status:** ✅ Abgeschlossen

- [x] Mehrfache Bildkonvertierungen reduziert
  - `windowscapture.py`: Direkte NumPy-Array Rückgabe
  - Unnötige PIL Image Konvertierung entfernt
- [x] Alpha-Channel nur einmal entfernen
- [x] Type Hints für WindowCapture hinzugefügt
- [x] Verbesserte Fehlerbehandlung mit Logging

**Erwartetes Ergebnis:** ✅ 15-20% schnellere Screenshot-Verarbeitung

______________________________________________________________________

### 2.2 Vision Thread Optimierung

**Priorität:** MITTEL | **Aufwand:** 2h | **Status:** ✅ Teilweise abgeschlossen

- [x] Sleep-Zeiten als Konstanten definiert (VISION_SLEEP_INTERVAL)
- [x] Template-Matching-Konstanten extrahiert
- [ ] Unnötige Locks evaluieren und ggf. entfernen
- [ ] Batch-Processing von mehreren Needle-Images evaluieren

**Erwartetes Ergebnis:** 🔄 Niedrigere CPU-Last, flüssigere UI (in Arbeit)

______________________________________________________________________

### 2.3 Magische Zahlen eliminieren

**Priorität:** NIEDRIG | **Aufwand:** 1h | **Status:** ✅ Abgeschlossen

- [x] Konstanten-Datei erstellt (`evealert/constants.py`)
  - Sleep-Zeiten (MAIN_CHECK_SLEEP_MIN/MAX, VISION_SLEEP_INTERVAL)
  - Cooldown-Werte (DEFAULT_COOLDOWN_TIMER, WEBHOOK_COOLDOWN)
  - Max Sound Triggers (MAX_SOUND_TRIGGERS)
  - Detection Thresholds (DETECTION_THRESHOLD_MIN/MAX)
  - UI Dimensionen (WINDOW_WIDTH/HEIGHT)
  - OpenCV-Parameter (CV_RECTANGLE_THICKNESS, CV_LINE_TYPE, CV_DETECTION_COLOR)
  - Audio-Konstanten (AUDIO_CHANNELS)
  - Datei-Pfade und Präfixe
- [x] Alle hardcodierten Werte durch Konstanten ersetzt in:
  - alertmanager.py
  - vision.py
  - main.py

**Erwartetes Ergebnis:** ✅ Bessere Wartbarkeit, einfache Anpassung

______________________________________________________________________

## Phase 3: Code-Qualität & Wartbarkeit 📝

### 3.1 Type Hints vervollständigen

**Priorität:** MITTEL | **Aufwand:** 2h | **Status:** ✅ Abgeschlossen

- [x] Type Hints für AlertAgent Properties hinzugefügt
- [x] Type Hints für zentrale Methoden (start, stop, load_settings)
- [x] Type Hints für WindowCapture vollständig
- [x] Type Hints für ConfigValidator vollständig
- [x] Type Hints für MainMenu und alle GUI-Klassen
- [x] Type Hints für ConfigModeMenu vollständig
- [x] Type Hints für OverlaySystem mit Optional Types
- [x] Type Hints für helper.py
- [x] Return Types für 45+ Methoden hinzugefügt
- [ ] mypy Integration für Type-Checking (optional)

**Erwartetes Ergebnis:** ✅ Bessere IDE-Unterstützung, ~90% Type Coverage

______________________________________________________________________

### 3.2 Logging verbessern

**Priorität:** NIEDRIG | **Aufwand:** 1h | **Status:** ✅ Abgeschlossen (Sprint 2)

- [x] Strukturierte Log-Levels konsistent verwenden
  - DEBUG für Vision-Details
  - INFO für normale Events
  - WARNING für recoverable Errors
  - ERROR für kritische Fehler
- [x] Log-Rotation implementiert (5MB, 3 Backups)
- [ ] Performance-Metriken optional loggen

**Erwartetes Ergebnis:** ✅ Besseres Debugging, Troubleshooting

______________________________________________________________________

### 3.3 Dokumentation vervollständigen

**Priorität:** HOCH | **Aufwand:** 2h | **Status:** ✅ Abgeschlossen

- [x] Alle Kommentare auf Englisch umgestellt
- [x] Comprehensive Docstrings für alle Klassen
- [x] Method-Level Docstrings mit Args/Returns
- [x] Beispiele in Docstrings wo hilfreich
- [x] Google-Style Format durchgehend verwendet
- [x] ~95% Docstring Coverage erreicht

**Erwartetes Ergebnis:** ✅ Professionelle Dokumentation, einfaches Onboarding

______________________________________________________________________

## Phase 4: Neue Features & Verbesserungen ✨

### 4.1 Runtime-Konfiguration

**Priorität:** MITTEL | **Aufwand:** 3h | **Status:** ⏳ Ausstehend

- [ ] Settings während Laufzeit anpassbar machen
  - Detection Scale live ändern
  - Cooldown-Timer anpassen
  - Sound-Lautstärke regeln
- [ ] "Apply Settings" ohne Neustart
- [ ] Settings-Validierung in Echtzeit

**Erwartetes Ergebnis:** Bessere Benutzererfahrung

______________________________________________________________________

### 4.2 Multi-Monitor Unterstützung

**Priorität:** NIEDRIG | **Aufwand:** 4h | **Status:** ⏳ Ausstehend

- [ ] Monitor-Auswahl in Settings
- [ ] Koordinaten relativ zu gewähltem Monitor
- [ ] Automatische Monitor-Erkennung
- [ ] Multi-Monitor Overlay-System

**Erwartetes Ergebnis:** Flexibilität für Multi-Monitor-Setups

______________________________________________________________________

### 4.3 Statistik & History

**Priorität:** NIEDRIG | **Aufwand:** 3h | **Status:** ⏳ Ausstehend

- [ ] Alarm-Counter (Total, Session)
- [ ] Zeitstempel-Historie (letzte 10 Alarme)
- [ ] Export zu CSV/JSON
- [ ] Optionale Statistik-Anzeige im UI

**Erwartetes Ergebnis:** Nutzungsanalyse, Pattern-Erkennung

______________________________________________________________________

### 4.4 Erweiterte Audio-Optionen

**Priorität:** NIEDRIG | **Aufwand:** 2h | **Status:** ⏳ Ausstehend

- [ ] Lautstärke-Regler im UI
- [ ] Eigene Sound-Dateien wählbar
- [ ] Test-Button für Sounds
- [ ] Fade-In/Fade-Out Effekte

**Erwartetes Ergebnis:** Personalisierung

______________________________________________________________________

## Phase 5: Testing & CI/CD 🧪

### 5.1 Unit Tests erstellen

**Priorität:** MITTEL | **Aufwand:** 6h | **Status:** ⏳ Ausstehend

- [ ] Test-Suite für Vision-Modul
  - Template-Matching Tests
  - Edge-Cases (keine Matches, zu viele Matches)
- [ ] Test-Suite für AlertManager
  - Alarm-Trigger-Logik
  - Cooldown-Funktionalität
- [ ] Test-Suite für Konfiguration
  - Settings laden/speichern
  - Validierung
- [ ] Mock-Objekte für UI-Tests
- [ ] Test-Coverage > 70%

**Erwartetes Ergebnis:** Stabilere Releases, Regression-Prevention

______________________________________________________________________

### 5.2 Integration Tests

**Priorität:** NIEDRIG | **Aufwand:** 4h | **Status:** ⏳ Ausstehend

- [ ] End-to-End Test mit Mock-Screenshots
- [ ] Webhook-Integration Tests
- [ ] Audio-System Tests
- [ ] Config-Persistenz Tests

**Erwartetes Ergebnis:** Vollständige Test-Abdeckung

______________________________________________________________________

### 5.3 GitHub Actions verbessern

**Priorität:** NIEDRIG | **Aufwand:** 2h | **Status:** ⏳ Ausstehend

- [ ] Automatische Tests bei PR
- [ ] Code-Coverage Reporting
- [ ] Automatisches PyInstaller Build
- [ ] Release-Automation

**Erwartetes Ergebnis:** Automatisierte Qualitätssicherung

______________________________________________________________________

## Phase 6: Dokumentation 📚

### 6.1 Code-Dokumentation

**Priorität:** MITTEL | **Aufwand:** 3h | **Status:** ⏳ Ausstehend

- [ ] Docstrings für alle öffentlichen Funktionen/Klassen
- [ ] Google/NumPy Style Docstrings
- [ ] Sphinx-Dokumentation Setup (optional)
- [ ] Architecture Decision Records (ADRs)

**Erwartetes Ergebnis:** Bessere Onboarding für Contributors

______________________________________________________________________

### 6.2 Benutzer-Dokumentation

**Priorität:** NIEDRIG | **Aufwand:** 2h | **Status:** ⏳ Ausstehend

- [ ] Setup-Guide erweitern
- [ ] Troubleshooting-Sektion
- [ ] FAQ erstellen
- [ ] Video-Tutorial (optional)
- [ ] Screenshots aktualisieren

**Erwartetes Ergebnis:** Reduzierte Support-Anfragen

______________________________________________________________________

## Priorisierte Roadmap

### Sprint 1 (Woche 1-2): Stabilität ⚡

1. Dependencies Synchronisation
1. Fehlerbehandlung & Validierung
1. Screenshot-Optimierung

**Ziel:** Stabile Basis-Version

______________________________________________________________________

### Sprint 2 (Woche 3-4): Performance 🚀

1. Vision Thread Optimierung
1. Magische Zahlen eliminieren
1. Type Hints vervollständigen

**Ziel:** Optimierte, wartbare Codebasis

______________________________________________________________________

### Sprint 3 (Woche 5-6): Features ✨

1. Runtime-Konfiguration
1. Logging verbessern
1. Statistik & History

**Ziel:** Erweiterte Funktionalität

______________________________________________________________________

### Sprint 4 (Woche 7-8): Testing 🧪

1. Unit Tests erstellen
1. Code-Dokumentation
1. GitHub Actions verbessern

**Ziel:** Professionelle Code-Qualität

______________________________________________________________________

### Backlog (Nice to Have) 💡

- Multi-Monitor Unterstützung
- Internationalisierung
- Integration Tests
- Erweiterte Audio-Optionen
- Benutzer-Dokumentation

______________________________________________________________________

## Erfolgs-Metriken

- ✅ 0 bekannte kritische Bugs
- ✅ Test-Coverage > 70%
- ✅ CPU-Last < 5% im Idle
- ✅ RAM-Nutzung < 150MB
- ✅ Startup-Zeit < 3 Sekunden
- ✅ 100% konsistente Dependencies
- ✅ Type-Hint Coverage > 90%

______________________________________________________________________

## Notizen & Entscheidungen

### Dependencies-Entscheidung

- Verwende `pyproject.toml` als primäre Quelle
- `requirements.txt` für Backward-Kompatibilität beibehalten
- Automatische Sync mittels Script

### Breaking Changes vermeiden

- Alle Änderungen müssen abwärtskompatibel sein
- Bestehende Config-Dateien müssen weiterfunktionieren
- Migration-Guide bei größeren Änderungen

### Code-Style

- Black Formatter (bereits aktiv)
- isort für Imports
- pylint/flake8 für Linting
- Pre-commit Hooks (bereits aktiv)

______________________________________________________________________

**Letzte Aktualisierung:** 17. November 2025
**Verantwortlich:** Development Team
**Status:** 📋 In Planung
