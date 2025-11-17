# EVE Alert - Manuelle Test-Checkliste

## Status: Die GUI läuft bereits im Hintergrund

## ✅ Test-Checkliste

### 1. GUI Start & Erscheinungsbild
- [ ] Main Menu öffnet sich korrekt
- [ ] Dark Mode aktiviert
- [ ] ASCII Art angezeigt
- [ ] Version korrekt angezeigt

### 2. Settings Menu
- [ ] Settings-Button funktioniert
- [ ] Alle Eingabefelder sichtbar:
  - [ ] Webhook URL
  - [ ] System Name
  - [ ] Detection Scale Slider (0-100%)
  - [ ] Cooldown Timer
  - [ ] Mute Alarm Checkbox
- [ ] "Save Settings" speichert korrekt
- [ ] Ungültige Eingaben werden abgefangen (Validation)

### 3. Config Mode
- [ ] Config Mode Button öffnet Fenster
- [ ] Beschreibungstext wird angezeigt:
  - F1 für Alert Region
  - F2 für Faction Region
  - ESC zum Abbrechen
- [ ] Button färbt sich rot wenn aktiv
- [ ] F1 aktiviert Alert Region Selection
- [ ] F2 aktiviert Faction Region Selection
- [ ] ESC bricht korrekt ab
- [ ] Marquee Selection funktioniert

### 4. Alert System (funktioniert nur mit EVE Online geöffnet)
- [ ] Start Button startet Überwachung
- [ ] Status ändert sich zu "Running"
- [ ] Vision Thread läuft (Log prüfen)
- [ ] Stop Button stoppt korrekt

### 5. Logging System (NEU - Sprint 2)
- [ ] Log-Dateien werden erstellt
- [ ] Console-Output sichtbar (wenn Terminal offen)
- [ ] Log Rotation funktioniert bei 5MB
- [ ] Backup-Dateien (.1, .2, .3) werden erstellt

### 6. Audio System
- [ ] Sound-Dateien vorhanden:
  - [ ] `sound/alarm.wav`
  - [ ] `sound/faction.wav`
- [ ] Audio-Validation funktioniert beim Start

### 7. Performance (Sprint 1 Optimierungen)
- [ ] Screenshot-Capture schnell (kein Ruckeln)
- [ ] Vision-Check alle 0.1s (VISION_SLEEP_INTERVAL)
- [ ] Kein Memory-Leak über 5+ Minuten

### 8. Error Handling
- [ ] Ungültige Webhook URL → ValidationError
- [ ] Fehlende Sound-Datei → AudioError
- [ ] Falsche Region Coordinates → RegionSizeError
- [ ] Detection Scale außerhalb 0-100 → ValidationError

## 🔍 Log-Dateien Prüfen

```powershell
# Alle Log-Dateien anzeigen
Get-ChildItem -Filter "*.log" -Recurse

# Neueste Logs ansehen
Get-Content evealert_main.log -Tail 50
Get-Content evealert_alert.log -Tail 50
```

## 📊 Performance Messung

```powershell
# Memory Usage überwachen (in separatem Terminal)
while ($true) {
    $proc = Get-Process python -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "$(Get-Date -Format 'HH:mm:ss') - Memory: $([math]::Round($proc.WorkingSet64 / 1MB, 2)) MB"
    }
    Start-Sleep -Seconds 5
}
```

## 🎯 Kritische Funktionen (Kern-Features)

### MUST WORK:
1. ✅ GUI startet ohne Fehler
2. ⚠️  Alert Region Selection (F1)
3. ⚠️  Sound Playback bei Detection
4. ⚠️  Webhook Notification (optional)
5. ✅ Settings speichern/laden
6. ✅ Validation von Eingaben

### NICE TO HAVE:
- Faction Region Detection (F2)
- Console Log Output
- Statistics/History

## 📝 Test-Protokoll

**Datum:** _____________
**Tester:** _____________
**Version:** v0.7.5

**Gefundene Probleme:**
1. _____________________________________________
2. _____________________________________________
3. _____________________________________________

**Notizen:**
_____________________________________________
_____________________________________________
_____________________________________________
