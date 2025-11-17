# EVE Alert - Praktischer Test-Guide

## 🎯 Ziel: Alert-System mit Test-Bildern validieren

### Vorbereitungen

**Vorhandene Template-Bilder:**
- **Alert/Enemy Detection:** `image_1_100%.png`, `image_2_100%.png`, `image_3_100%.png`, `image_4_100%.png`
- **Faction Detection:** `faction_1.jpg`, `faction_2.jpg`, `faction_3.jpg`

### 📋 Test-Ablauf

#### **Schritt 1: EVE Alert starten**

```powershell
# In PowerShell (im Projekt-Verzeichnis)
C:/Users/Kit_User_ML.MLML-U8FNBREUV2/Documents/GitHub/EVE-Alert-Opensource/.venv/Scripts/python.exe main.py
```

#### **Schritt 2: Regionen konfigurieren**

1. **Config Mode öffnen** (Button in der GUI)
2. **F1 drücken** für Alert Region
3. **Region markieren** (z.B. oberer Teil des Bildschirms, ca. 400x200 Pixel)
4. **F2 drücken** für Faction Region  
5. **Region markieren** (z.B. unterer Teil des Bildschirms, ca. 400x200 Pixel)

**💡 Tipp:** Mache die Regionen groß genug, um Bilder hineinzuziehen (mindestens 300x150 px)

#### **Schritt 3: Settings speichern**

1. Settings-Menu öffnen
2. **Detection Scale:** 90% (gut für Tests)
3. **Cooldown Timer:** 30 Sekunden
4. **Webhook:** Optional (kannst du testen oder leer lassen)
5. **Save** klicken

#### **Schritt 4: Alert-System starten**

1. **Start Button** in der GUI klicken
2. Status sollte "Running" zeigen
3. Console zeigt: "System: EVE Alert started."

#### **Schritt 5: Test durchführen**

**Test 1: Enemy Alert**
1. Öffne `evealert/img/image_1_100%.png` in einem Bildbetrachter (Windows Fotos)
2. Ziehe das Fenster in die **Alert Region** (die du mit F1 markiert hast)
3. **Erwartetes Ergebnis:**
   - ✅ Console: "Alert: Enemy detected!"
   - ✅ Sound wird abgespielt (3x, dann Cooldown)
   - ✅ Log-Eintrag in `logs/alert.log`

**Test 2: Faction Alert**
1. Öffne `evealert/img/faction_1.jpg` in einem Bildbetrachter
2. Ziehe das Fenster in die **Faction Region** (die du mit F2 markiert hast)
3. **Erwartetes Ergebnis:**
   - ✅ Console: "Alert: Faction detected!"
   - ✅ Faction Sound wird abgespielt
   - ✅ Log-Eintrag in `logs/alert.log`

**Test 3: Vision Debug Mode**
1. Während das System läuft: **Vision Debug Button** klicken
2. Ein OpenCV-Fenster öffnet sich mit grünen Rechtecken um Detektionen
3. Bewege das Test-Bild → Du siehst live die Detection-Boxes

**Test 4: Cooldown testen**
1. Verschiebe das Enemy-Bild **4x** in die Alert Region
2. Beim 4. Mal sollte kommen: "Enemy Sound is now in cooldown for 30 seconds"
3. Warte 30 Sekunden → Sound funktioniert wieder

**Test 5: Webhook (Optional)**
1. Erstelle einen Discord Webhook (oder Test-Webhook)
2. Trage ihn in Settings ein
3. Löse Enemy Alert aus
4. Webhook-Message sollte in Discord erscheinen

### 🔍 Was zu prüfen ist

**Während der Tests beobachten:**

✅ **Console Output:**
- Startet ohne Fehler
- Zeigt Detections an
- Zeigt Cooldown-Messages

✅ **Sound:**
- Alarm-Sound spielt bei Enemy
- Faction-Sound spielt bei Faction
- Max 3x spielen, dann Cooldown

✅ **Log-Dateien:**
```powershell
# Log-Dateien prüfen
Get-Content logs/alert.log -Tail 20
Get-Content logs/main.log -Tail 20
```

✅ **Performance:**
- Keine Verzögerung beim Detection
- Vision Check läuft flüssig (alle 0.1s)
- CPU-Last moderat (unter 10%)

### 📊 Erwartete Log-Ausgaben

**Bei Enemy Detection:**
```
2025-11-17 14:30:15 [INFO    ] alert        vision_thread       :245  - Enemy detected in alert region
2025-11-17 14:30:15 [INFO    ] alert        alarm_detection     :287  - Alert: Enemy detected!
2025-11-17 14:30:15 [INFO    ] alert        play_sound          :352  - Playing alarm sound for Enemy
```

**Bei Cooldown:**
```
2025-11-17 14:30:45 [INFO    ] alert        play_sound          :330  - Enemy Sound is in cooldown period.
```

### 🐛 Problembehandlung

**Problem: Kein Sound**
- Prüfe, ob `sound/alarm.wav` und `sound/faction.wav` existieren
- Stelle sicher, dass "Mute Alarm" NICHT aktiv ist
- Prüfe Sound-Device in Windows

**Problem: Keine Detection**
- Detection Scale erhöhen (95% statt 90%)
- Region größer machen
- Vision Debug Mode aktivieren → Grüne Boxen sollten erscheinen

**Problem: "Wrong Alert Settings"**
- Regionen neu konfigurieren (F1/F2)
- Mindestgröße: 50x50 Pixel
- x1 < x2 und y1 < y2 prüfen

**Problem: Zu viele False Positives**
- Detection Scale verringern (85% statt 90%)
- Spezifischeres Template-Bild verwenden

### ✅ Test-Checkliste

Nach den Tests sollten folgende Dinge funktionieren:

- [ ] GUI startet ohne Fehler
- [ ] Regionen können mit F1/F2 markiert werden
- [ ] Settings werden gespeichert und geladen
- [ ] Alert System startet mit "Start" Button
- [ ] Enemy Detection funktioniert (Sound + Console)
- [ ] Faction Detection funktioniert (Sound + Console)
- [ ] Vision Debug Mode zeigt Detection-Boxen
- [ ] Cooldown-System greift nach 3 Triggers
- [ ] Log-Dateien werden korrekt geschrieben
- [ ] Webhook-Integration funktioniert (optional)
- [ ] Stop-Button beendet System sauber

### 📸 Alternative Test-Methode

Wenn du kein EVE Online laufen hast:

1. **Screenshot-Methode:**
   - Mache Screenshots von EVE Online Local Chat
   - Speichere sie als `test_enemy.png` und `test_faction.png`
   - Öffne diese in Bildbetrachtung
   - Ziehe sie in die Regionen

2. **Statisches Bild-Fenster:**
   - Öffne die Template-Bilder in Windows Fotos (Fullscreen)
   - Positioniere sie über der Alert/Faction Region
   - EVE Alert sollte sie erkennen

### 🎯 Erfolgs-Kriterien

**✅ Test erfolgreich, wenn:**
- Alle 5 Kern-Tests durchlaufen
- Keine Fehler in Logs
- Sound spielt korrekt
- Cooldown funktioniert
- Performance ist gut (< 10% CPU)

**❌ Test fehlgeschlagen, wenn:**
- Crashes während Detection
- Kein Sound trotz Detection
- False Positives (erkennt alles)
- False Negatives (erkennt nichts)
- Memory Leak (> 500 MB nach 5 Min)

---

**Viel Erfolg beim Testen! 🚀**

Bei Problemen: Logs in `logs/` Ordner prüfen.
