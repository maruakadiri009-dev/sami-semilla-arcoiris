# Configuración centralizada del proyecto
import os
from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"
SCENES_DIR = ASSETS_DIR / "scenes"
MUSIC_DIR = ASSETS_DIR / "music"
SFX_DIR = ASSETS_DIR / "sfx"
CHARACTERS_DIR = ASSETS_DIR / "characters"

# Crear directorios si no existen
for directory in [ASSETS_DIR, OUTPUT_DIR, TEMP_DIR, SCENES_DIR, MUSIC_DIR, SFX_DIR, CHARACTERS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Video
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30
TOTAL_DURATION = 120  # 2 minutos en segundos
CLIP_DURATION = 15  # Cada escena dura 15 segundos
NUM_SCENES = 8
CODEC = 'libx264'
BITRATE = '8000k'

# Audio
AUDIO_BITRATE = '192k'
AUDIO_CHANNELS = 2
AUDIO_SAMPLE_RATE = 44100
NARRATION_VOICE = "es-ES-StandardF"  # Voz femenina cálida en español
MUSIC_VOLUME = 0.35  # 35% cuando no hay narración
DUCKING_LEVEL = 0.15  # 15% cuando hay narración
NARRATION_VOLUME = 0.9  # 90% para narración

# Movimientos
ZOOM_RANGE = (1.0, 1.3)  # Zoom suave entre 1.0 y 1.3
PAN_SPEED = 20  # píxeles por segundo
BOUNCE_HEIGHT = 30  # píxeles para efecto rebote

# Efectos y transiciones
FADE_DURATION = 0.5  # segundos
TRANSITION_TYPE = 'fade'  # fade, zoom, slide

# Archivos de salida
OUTPUT_VIDEO = OUTPUT_DIR / "sami_semilla_arcoiris.mp4"
TEMP_AUDIO = TEMP_DIR / "combined_audio.wav"
TEMP_NARRATION = TEMP_DIR / "narration.wav"
TEMP_MUSIC = TEMP_DIR / "music.wav"

# Narraciones por escena (en español)
NARRATIONS = [
    "En la Granja Arcoíris, Sami encontró una semilla que brillaba como una estrella.",
    "La plantaron con mucho cuidado, pero aquella semilla mágica tenía cosquillas.",
    "De pronto, el viento travieso se llevó el brote. ¡Había que alcanzarlo!",
    "La vaca Canela quería ayudar, aunque mirar su propia espalda no era nada fácil.",
    "Con paciencia y la ayuda de tres patitos, cruzaron el riachuelo paso a paso.",
    "Cuando todos ayudaron, el pequeño brote descubrió su verdadera magia.",
    "Del suelo nació el árbol más maravilloso que la granja había visto jamás.",
    "Sami comprendió que, cuando compartimos y trabajamos juntos, la magia crece. Pero aquella aventura todavía no había terminado."
]

# Escenas (nombres de archivos esperados)
SCENE_FILES = [
    "seed_falling.png",
    "planting.png",
    "wind_blast.png",
    "cow_canela.png",
    "crossing_stream.png",
    "animals_help.png",
    "rainbow_tree.png",
    "sharing_fruits.png"
]

# Efectos de sonido
SFX_FILES = {
    "birds": SFX_DIR / "birds.wav",
    "wind": SFX_DIR / "wind.wav",
    "water": SFX_DIR / "water.wav",
    "magic": SFX_DIR / "magic.wav",
    "animals": SFX_DIR / "animals.wav"
}

# Música
MUSIC_FILES = [
    MUSIC_DIR / "background_music.mp3",
    MUSIC_DIR / "background_music.wav"
]

# Personajes
CHARACTER_FILES = {
    "sami": CHARACTERS_DIR / "sami.png",
    "lulu": CHARACTERS_DIR / "lulu.png"
}

# Colores para placeholders (temática infantil)
COLORS = {
    "sky_blue": (135, 206, 235),
    "grass_green": (34, 139, 34),
    "sunny_yellow": (255, 215, 0),
    "rainbow_red": (255, 0, 0),
    "rainbow_orange": (255, 165, 0),
    "rainbow_yellow": (255, 255, 0),
    "rainbow_green": (0, 128, 0),
    "rainbow_blue": (0, 0, 255),
    "rainbow_indigo": (75, 0, 130),
    "rainbow_violet": (148, 0, 211),
    "cotton_white": (240, 248, 255),
    "gentle_pink": (255, 192, 203)
}

# Validación
MIN_DURATION = 119  # 119 segundos
MAX_DURATION = 121  # 121 segundos
EXPECTED_WIDTH = 1920
EXPECTED_HEIGHT = 1080
EXPECTED_ASPECT_RATIO = 16 / 9
TOLERANCE_ASPECT = 0.01  # 1% de tolerancia
