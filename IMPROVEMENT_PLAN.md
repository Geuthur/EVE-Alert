# EVE-Alert Verbesserungsplan

## Projektübersicht
Systematische Verbesserung des EVE-Alert Systems für bessere Performance, Stabilität und Wartbarkeit.

---

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

---

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

---

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

---

### 2.2 Vision Thread Optimierung
**Priorität:** MITTEL | **Aufwand:** 2h | **Status:** ✅ Teilweise abgeschlossen

- [x] Sleep-Zeiten als Konstanten definiert (VISION_SLEEP_INTERVAL)
- [x] Template-Matching-Konstanten extrahiert
- [ ] Unnötige Locks evaluieren und ggf. entfernen
- [ ] Batch-Processing von mehreren Needle-Images evaluieren

**Erwartetes Ergebnis:** 🔄 Niedrigere CPU-Last, flüssigere UI (in Arbeit)

---

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

---

## Phase 3: Code-Qualität & Wartbarkeit 📝

### 3.1 Type Hints vervollständigen
**Priorität:** MITTEL | **Aufwand:** 2h | **Status:** ✅ Teilweise abgeschlossen

- [x] Type Hints für AlertAgent Properties hinzugefügt
- [x] Type Hints für zentrale Methoden (start, stop, load_settings)
- [x] Type Hints für WindowCapture vollständig
- [x] Type Hints für ConfigValidator vollständig
- [ ] Return Types für alle verbleibenden Funktionen
- [ ] mypy Integration für Type-Checking

**Erwartetes Ergebnis:** 🔄 Bessere IDE-Unterstützung, weniger Runtime-Fehler

---

### 3.2 Logging verbessern
**Priorität:** NIEDRIG | **Aufwand:** 1h | **Status:** ⏳ Ausstehend

- [ ] Strukturierte Log-Levels konsistent verwenden
  - DEBUG für Vision-Details
  - INFO für normale Events
  - WARNING für recoverable Errors
  - ERROR für kritische Fehler
- [ ] Log-Rotation implementieren
- [ ] Performance-Metriken optional loggen

**Erwartetes Ergebnis:** Besseres Debugging, Troubleshooting

---

### 3.3 Internationalisierung vorbereiten
**Priorität:** NIEDRIG | **Aufwand:** 3h | **Status:** ⏳ Ausstehend

- [ ] Deutsche Kommentare auf Englisch umstellen
- [ ] UI-Texte externalisieren (Basis für i18n)
- [ ] Fehlermeldungen in Konstanten auslagern
- [ ] Optional: i18n-Framework integrieren (gettext)

**Erwartetes Ergebnis:** Internationale Nutzbarkeit

---

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

---

### 4.2 Multi-Monitor Unterstützung
**Priorität:** NIEDRIG | **Aufwand:** 4h | **Status:** ⏳ Ausstehend

- [ ] Monitor-Auswahl in Settings
- [ ] Koordinaten relativ zu gewähltem Monitor
- [ ] Automatische Monitor-Erkennung
- [ ] Multi-Monitor Overlay-System

**Erwartetes Ergebnis:** Flexibilität für Multi-Monitor-Setups

---

### 4.3 Statistik & History
**Priorität:** NIEDRIG | **Aufwand:** 3h | **Status:** ⏳ Ausstehend

- [ ] Alarm-Counter (Total, Session)
- [ ] Zeitstempel-Historie (letzte 10 Alarme)
- [ ] Export zu CSV/JSON
- [ ] Optionale Statistik-Anzeige im UI

**Erwartetes Ergebnis:** Nutzungsanalyse, Pattern-Erkennung

---

### 4.4 Erweiterte Audio-Optionen
**Priorität:** NIEDRIG | **Aufwand:** 2h | **Status:** ⏳ Ausstehend

- [ ] Lautstärke-Regler im UI
- [ ] Eigene Sound-Dateien wählbar
- [ ] Test-Button für Sounds
- [ ] Fade-In/Fade-Out Effekte

**Erwartetes Ergebnis:** Personalisierung

---

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

---

### 5.2 Integration Tests
**Priorität:** NIEDRIG | **Aufwand:** 4h | **Status:** ⏳ Ausstehend

- [ ] End-to-End Test mit Mock-Screenshots
- [ ] Webhook-Integration Tests
- [ ] Audio-System Tests
- [ ] Config-Persistenz Tests

**Erwartetes Ergebnis:** Vollständige Test-Abdeckung

---

### 5.3 GitHub Actions verbessern
**Priorität:** NIEDRIG | **Aufwand:** 2h | **Status:** ⏳ Ausstehend

- [ ] Automatische Tests bei PR
- [ ] Code-Coverage Reporting
- [ ] Automatisches PyInstaller Build
- [ ] Release-Automation

**Erwartetes Ergebnis:** Automatisierte Qualitätssicherung

---

## Phase 6: Dokumentation 📚

### 6.1 Code-Dokumentation
**Priorität:** MITTEL | **Aufwand:** 3h | **Status:** ⏳ Ausstehend

- [ ] Docstrings für alle öffentlichen Funktionen/Klassen
- [ ] Google/NumPy Style Docstrings
- [ ] Sphinx-Dokumentation Setup (optional)
- [ ] Architecture Decision Records (ADRs)

**Erwartetes Ergebnis:** Bessere Onboarding für Contributors

---

### 6.2 Benutzer-Dokumentation
**Priorität:** NIEDRIG | **Aufwand:** 2h | **Status:** ⏳ Ausstehend

- [ ] Setup-Guide erweitern
- [ ] Troubleshooting-Sektion
- [ ] FAQ erstellen
- [ ] Video-Tutorial (optional)
- [ ] Screenshots aktualisieren

**Erwartetes Ergebnis:** Reduzierte Support-Anfragen

---

## Priorisierte Roadmap

### Sprint 1 (Woche 1-2): Stabilität ⚡
1. Dependencies Synchronisation
2. Fehlerbehandlung & Validierung
3. Screenshot-Optimierung

**Ziel:** Stabile Basis-Version

---

### Sprint 2 (Woche 3-4): Performance 🚀
1. Vision Thread Optimierung
2. Magische Zahlen eliminieren
3. Type Hints vervollständigen

**Ziel:** Optimierte, wartbare Codebasis

---

### Sprint 3 (Woche 5-6): Features ✨
1. Runtime-Konfiguration
2. Logging verbessern
3. Statistik & History

**Ziel:** Erweiterte Funktionalität

---

### Sprint 4 (Woche 7-8): Testing 🧪
1. Unit Tests erstellen
2. Code-Dokumentation
3. GitHub Actions verbessern

**Ziel:** Professionelle Code-Qualität

---

### Backlog (Nice to Have) 💡
- Multi-Monitor Unterstützung
- Internationalisierung
- Integration Tests
- Erweiterte Audio-Optionen
- Benutzer-Dokumentation

---

## Erfolgs-Metriken

- ✅ 0 bekannte kritische Bugs
- ✅ Test-Coverage > 70%
- ✅ CPU-Last < 5% im Idle
- ✅ RAM-Nutzung < 150MB
- ✅ Startup-Zeit < 3 Sekunden
- ✅ 100% konsistente Dependencies
- ✅ Type-Hint Coverage > 90%

---

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

---

**Letzte Aktualisierung:** 17. November 2025
**Verantwortlich:** Development Team
**Status:** 📋 In Planung
