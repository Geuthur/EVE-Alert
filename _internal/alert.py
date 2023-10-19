import pyautogui, os, pygame, time, random, sys
from config import *
from functions import load_settings, open_settings


# ALERT SYSTEM
settings = open_settings()

def start_eve_alert(stop_event, system_label):
    while not stop_event.is_set():
        settings = load_settings()
        if settings:
            x1 = int(settings.get("alert_region_1", {}).get("x", None))
            y1 = int(settings.get("alert_region_1", {}).get("y", None))
            x2 = int(settings.get("alert_region_2", {}).get("x", None))
            y2 = int(settings.get("alert_region_2", {}).get("y", None))
            detection = settings.get("detectionscale", {}).get("value", None)
            detection = detection / 100
            print(detection)
        else:
            print("Bitte stelle zuerst die Einstellungen ein")
            break
        
        # Den Dateinamen des ersten Bildes angeben
        image_1_img = "img/image_1.png"
        image_2_img = "img/image_2.png"

        # Den Dateinamen des Alarmklangs angeben
        alarm_sound = "sound/alarm.mp3"

        def get_resource_path(relative_path):
            if getattr(sys, 'frozen', False):
                # Wenn das Skript mit PyInstaller kompiliert wurde
                base_path = os.path.abspath(".")
            else:
                # Wenn das Skript direkt ausgeführt wird
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        image_1 = get_resource_path(image_1_img)
        image_2 = get_resource_path(image_2_img)

        alarm_path = get_resource_path(alarm_sound)

        # Initialisieren von pygame
        pygame.mixer.init()

        # Laden des Alarmklangs
        alarm_sound = pygame.mixer.Sound(alarm_path)
        try:
            # Bilderkennung für das zweite Bild im definierten Bereich durchführen und Farbübereinstimmung berücksichtigen
            search_image_1 = pyautogui.locateOnScreen(image_1, region=(x1, y1, x2 - x1, y2 - y1), grayscale=False, confidence=detection)
            search_image_2 = pyautogui.locateOnScreen(image_2, region=(x1, y1, x2 - x1, y2 - y1), grayscale=False, confidence=detection)
        except:
            global alert_thread
            if alert_thread:
                alert_thread_stop_event.set()  # Signal zum Beenden des Alert-Threads
                alert_thread.join()  # Warten Sie, bis der Thread beendet ist
                alert_thread_stop_event.clear()  # Setzen Sie das Event zurück, um es erneut verwenden zu können
            alert_thread = None
            system_label.config(text="System: ❎ Wrong region settings.")
            return

        # Überprüfen, ob das erste Bild gefunden wurde
        if search_image_1 is not None or search_image_2 is not None:
            alarm_sound.play()
            print("Play Alarm")
        else:
            print("No Enemy detected...")

        # Zufällige Schlafzeit zwischen 2 und 3 Sekunden
        sleep_time = random.uniform(2, 3)
        print(f"Next check in {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)