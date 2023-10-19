import json, os
from config import settings_file

def load_settings():
    try:
        with open(settings_file, 'r') as file:
            settings = json.load(file)
        return settings
    except FileNotFoundError:
        return {}
    
def open_settings():
    try:
        with open(settings_file, 'r') as file:
            settings = json.load(file)
        return settings
    except FileNotFoundError:
        if os.path.exists(settings_file):  # Überprüfen, ob die Datei existiert
            # Wenn die Datei existiert, lösche sie
            os.remove(settings_file)
        pass