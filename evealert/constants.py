"""Constants for EVE Alert application."""

# Vision & Detection
VISION_SLEEP_INTERVAL = 0.1  # Sleep between vision checks (seconds)
MAIN_CHECK_SLEEP_MIN = 2.0  # Minimum sleep between main checks (seconds)
MAIN_CHECK_SLEEP_MAX = 3.0  # Maximum sleep between main checks (seconds)
DETECTION_SCALE_MIN = 0  # Minimum detection scale percentage
DETECTION_SCALE_MAX = 100  # Maximum detection scale percentage
DETECTION_THRESHOLD_MIN = 0.1  # Minimum threshold for template matching
DETECTION_THRESHOLD_MAX = 1.0  # Maximum threshold for template matching

# Alarm & Cooldown
MAX_SOUND_TRIGGERS = 3  # Maximum sound triggers before cooldown
DEFAULT_COOLDOWN_TIMER = 60  # Default cooldown time in seconds
WEBHOOK_COOLDOWN = 5  # Webhook cooldown time in seconds

# UI
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 350
UI_UPDATE_INTERVAL = 100  # Mouse position update interval (ms)
STATUS_CHECK_INTERVAL = 1000  # Status check interval (ms)

# Audio
AUDIO_CHANNELS = 2  # Stereo output

# File Paths
IMG_FOLDER = "img"
SOUND_FOLDER = "sound"
ALARM_SOUND_FILE = "alarm.wav"
FACTION_SOUND_FILE = "faction.wav"

# Image Prefixes
ALERT_IMAGE_PREFIX = "image_"
FACTION_IMAGE_PREFIX = "faction_"

# Logging
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT_STRING = "%(asctime)s [%(levelname)-8s] %(name)-12s %(funcName)-20s:%(lineno)-4d - %(message)s"
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB per log file
LOG_BACKUP_COUNT = 3  # Keep 3 backup files
LOG_DEFAULT_LEVEL = "INFO"

# OpenCV
CV_RECTANGLE_THICKNESS = 2
CV_LINE_TYPE = 4  # cv.LINE_4
CV_DETECTION_COLOR = (0, 255, 0)  # Green for detection boxes

# Template Matching
GROUP_RECTANGLES_THRESHOLD = 1
GROUP_RECTANGLES_EPS = 0.5
