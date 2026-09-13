# 🌈 Sami y la Semilla Arcoíris - Generador de Video Infantil

Generador completo de vídeos infantiles usando Python, MoviePy y herramientas de código abierto. Crea un episodio de 2 minutos en formato MP4 (1920×1080, 16:9, 30fps) sin marcas de agua.

## 📋 Características

- ✅ Generación automática de vídeos infantiles en MP4
- ✅ Narración en español con Edge TTS (voz femenina cálida)
- ✅ Música infantil sin copyright con ducking automático (15% al narrar)
- ✅ Efectos de sonido: pájaros, viento, agua, animales, sonidos mágicos
- ✅ Movimientos suaves: zoom, desplazamiento, rebote, transiciones
- ✅ Validación automática: duración, resolución, sonido, sincronización
- ✅ Protagonistas consistentes: Sami y Lulu
- ✅ Formato YouTube Ready: 1920×1080, 16:9, 30fps
- ✅ Sin dependencias de pago, sin claves privadas

## 📁 Estructura del Proyecto

```
sami-semilla-arcoiris/
├── README.md
├── requirements.txt
├── generate_video.py          # Script principal
├── scene_builder.py           # Gestor de escenas
├── audio_processor.py         # Procesa audio y narración
├── video_validator.py         # Valida salida final
├── config.py                  # Configuración centralizada
├── assets/
│   ├── scenes/               # Clips e imágenes de escenas
│   ├── music/                # Música infantil (local)
│   ├── sfx/                  # Efectos de sonido
│   │   ├── birds.wav
│   │   ├── wind.wav
│   │   ├── water.wav
│   │   ├── magic.wav
│   │   └── animals.wav
│   └── characters/           # Imágenes de Sami y Lulu
├── output/                   # Video final
│   └── sami_semilla_arcoiris.mp4
└── temp/                     # Archivos temporales (se limpia automáticamente)
```

## 🚀 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/maruakadiri009-dev/sami-semilla-arcoiris.git
cd sami-semilla-arcoiris
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota**: La primera ejecución descargará modelos de ffmpeg automáticamente (~300MB).

### 4. Preparar assets

#### a) Imágenes y Clips de Escenas
Coloca tus archivos en `assets/scenes/`:
- Scene 1: `seed_falling.png` o `seed_falling.mp4` (semilla cayendo)
- Scene 2: `planting.png` o `planting.mp4` (Sami y Lulu plantando)
- Scene 3: `wind_blast.png` o `wind_blast.mp4` (viento llevándose el brote)
- Scene 4: `cow_canela.png` (vaca Canela)
- Scene 5: `crossing_stream.png` o `crossing_stream.mp4` (cruzando riachuelo)
- Scene 6: `animals_help.png` o `animals_help.mp4` (animales ayudando)
- Scene 7: `rainbow_tree.png` o `rainbow_tree.mp4` (árbol arcoíris creciendo)
- Scene 8: `sharing_fruits.png` (Sami repartiendo frutas)

**Si no tienes archivos**, el script genera placeholders automáticamente con:
- Fondos de color con gradientes infantiles
- Texto de descripción de escena
- Animaciones suaves

#### b) Música Infantil
Coloca un archivo en `assets/music/`:
- `background_music.mp3` o `background_music.wav`

**Si no tienes música**, el script descarga automáticamente un track infantil sin copyright de Pixabay.

#### c) Efectos de Sonido (SFX)
Ya incluidos en `assets/sfx/`:
- `birds.wav` - Cantos de pájaros
- `wind.wav` - Sonido de viento
- `water.wav` - Sonido de agua/riachuelo
- `magic.wav` - Sonido mágico (twinkle)
- `animals.wav` - Sonidos de animales

Si no existen, se generarán automáticamente con tonos sintetizados.

#### d) Imágenes de Personajes
Coloca en `assets/characters/`:
- `sami.png` - Sami (niño con sudadera amarilla)
- `lulu.png` - Lulu (pollito amarillo con pañuelo rojo)

**Si no existen**, el script crea versiones placeholder coloreadas.

### 5. Ejecutar el generador

```bash
python generate_video.py
```

El script:
1. ✅ Verifica assets y crea placeholders si falta algo
2. ✅ Genera narración en español con Edge TTS
3. ✅ Sincroniza música y efectos de sonido
4. ✅ Aplica movimientos suaves a imágenes
5. ✅ Compone 8 escenas de 15 segundos cada una
6. ✅ Valida duración, resolución y audio
7. ✅ Genera `output/sami_semilla_arcoiris.mp4`

### 6. Resultado

El video final está en: **`output/sami_semilla_arcoiris.mp4`**

Especificaciones garantizadas:
- Duración: 120 segundos (exactamente 2 minutos)
- Resolución: 1920×1080
- Relación de aspecto: 16:9
- FPS: 30
- Codec: H.264
- Audio: 192 kbps, estéreo
- Sin marcas de agua

## 📝 Cuadro de Diálogos (Narración Automática)

| Tiempo | Escena | Narración |
|--------|--------|-----------|
| 0:00–0:15 | Semilla cayendo | "En la Granja Arcoíris, Sami encontró una semilla que brillaba como una estrella." |
| 0:15–0:30 | Plantando | "La plantaron con mucho cuidado, pero aquella semilla mágica tenía cosquillas." |
| 0:30–0:45 | Viento | "De pronto, el viento travieso se llevó el brote. ¡Había que alcanzarlo!" |
| 0:45–1:00 | Vaca Canela | "La vaca Canela quería ayudar, aunque mirar su propia espalda no era nada fácil." |
| 1:00–1:15 | Riachuelo | "Con paciencia y la ayuda de tres patitos, cruzaron el riachuelo paso a paso." |
| 1:15–1:30 | Todos ayudan | "Cuando todos ayudaron, el pequeño brote descubrió su verdadera magia." |
| 1:30–1:45 | Árbol arcoíris | "Del suelo nació el árbol más maravilloso que la granja había visto jamás." |
| 1:45–2:00 | Compartiendo | "Sami comprendió que, cuando compartimos y trabajamos juntos, la magia crece. Pero aquella aventura todavía no había terminado." |

## 🔧 Configuración Avanzada

Edita `config.py` para personalizar:

```python
# Resolución y formato
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30
TOTAL_DURATION = 120  # segundos

# Audio
NARRATION_VOICE = "es-ES-StandardF"  # Voz Edge TTS (femenina cálida)
MUSIC_VOLUME = 0.35  # 35% en silencio, 15% durante narración
DUCKING_LEVEL = 0.15

# Movimientos
ZOOM_RANGE = (1.0, 1.3)  # Zoom suave
PAN_SPEED = 20  # Píxeles por segundo
```

## 🎨 Personalizar Personajes

Sami:
- Edad: 3 años
- Piel: Morena clara
- Ojos: Grandes ojos marrones
- Cabello: Rizo oscuro
- Ropa: Sudadera amarilla, pantalones cortos turquesa, zapatillas blancas

Lulu:
- Especie: Pollito
- Color: Amarillo esponjoso
- Accesorio: Pañuelo rojo

Para cambiar, reemplaza las imágenes en `assets/characters/` o edita las funciones de generación en `scene_builder.py`.

## 📊 Validación Automática

El script verifica:
- ✅ Duración exacta: 120 segundos
- ✅ Resolución: 1920×1080
- ✅ Relación de aspecto: 16:9
- ✅ FPS: 30
- ✅ Audio: Presente, estéreo, sincronizado
- ✅ Sincronización: Narración y música

Si hay errores, el script reporta qué corregir.

## 🐛 Solución de Problemas

| Problema | Solución |
|----------|----------|
| "ffmpeg not found" | Instala ffmpeg: `pip install ffmpeg-python` o descárgalo de ffmpeg.org |
| "Edge TTS error" | Verifica conexión a internet. Edge TTS requiere conexión. |
| "No audio in output" | Comprueba que `assets/music/` tiene un archivo de música válido. |
| "Video muy lento" | Reduce tamaño de imágenes a 1920×1080 máximo. |
| "Error de memoria" | Reduce CLIP_DURATION en config.py o usa imágenes más pequeñas. |

## 📦 Dependencias Principales

- **moviepy** - Edición de video
- **edge-tts** - Síntesis de voz IA (español)
- **soundfile** - Procesamiento de audio
- **numpy** - Operaciones numéricas
- **scipy** - Procesamiento de señales
- **pillow** - Manipulación de imágenes
- **ffmpeg** - Codec de video/audio

Todas son gratuitas y de código abierto.

## 📄 Licencia

Este proyecto es de código abierto y libre para uso educativo y comercial.

## 🤝 Contribuciones

¿Ideas? ¿Mejoras? ¡Abre un issue o haz un pull request!

## 📞 Soporte

Para errores o preguntas, abre un issue en GitHub.

---

**Hecho con ❤️ para la comunidad creativa. ¡Disfruta creando historias infantiles mágicas!**
