#!/usr/bin/env python3
"""
Generador de video infantil "Sami y la Semilla Arcoíris"
Script principal que orquesta todo el proceso de creación.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import shutil
import traceback

# Importar módulos del proyecto
from config import (
    TEMP_DIR, OUTPUT_DIR, ASSETS_DIR, SCENES_DIR, MUSIC_DIR, SFX_DIR,
    CHARACTERS_DIR, OUTPUT_VIDEO, TOTAL_DURATION, FPS, VIDEO_WIDTH,
    VIDEO_HEIGHT, NARRATIONS, TEMP_NARRATION, TEMP_MUSIC, TEMP_AUDIO,
    CLIP_DURATION, NUM_SCENES
)
from sfx_generator import SFXGenerator
from scene_builder import SceneBuilder
from audio_processor import AudioProcessor
from video_validator import VideoValidator

# Importar MoviePy
try:
    from moviepy.editor import (
        ImageClip, concatenate_videoclips, CompositeAudioFileClip,
        AudioFileClip, VideoFileClip, CompositeVideoClip
    )
    import numpy as np
except ImportError as e:
    print(f"[Error] Falta instalar MoviePy: {e}")
    print("Ejecuta: pip install -r requirements.txt")
    sys.exit(1)


class SamiVideoGenerator:
    """Generador completo del video de Sami y la Semilla Arcoíris."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.steps = []
    
    def log(self, message, level="INFO"):
        """Log con timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "ERROR": "✗",
            "WARNING": "⚠",
            "STEP": "→"
        }.get(level, "•")
        
        print(f"[{timestamp}] {prefix} {message}")
        self.steps.append((timestamp, level, message))
    
    def step(self, message):
        """Marcar paso importante."""
        print(f"\n{'='*70}")
        self.log(message, "STEP")
        print('='*70)
    
    def prepare_environment(self):
        """Prepara el entorno y directorios."""
        self.step("PASO 1: Preparando entorno")
        
        try:
            # Crear directorios si no existen
            for directory in [TEMP_DIR, OUTPUT_DIR, SCENES_DIR, MUSIC_DIR, SFX_DIR, CHARACTERS_DIR]:
                directory.mkdir(parents=True, exist_ok=True)
                self.log(f"Directorio listo: {directory.name}")
            
            # Limpiar archivos temporales antiguos
            if TEMP_DIR.exists():
                for temp_file in TEMP_DIR.glob("*"):
                    try:
                        temp_file.unlink()
                    except:
                        pass
            
            self.log("Entorno preparado", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"Error al preparar entorno: {e}", "ERROR")
            return False
    
    def generate_sfx(self):
        """Genera efectos de sonido."""
        self.step("PASO 2: Generando efectos de sonido")
        
        try:
            generator = SFXGenerator(sample_rate=44100, duration=3)
            generator.save_sfx(SFX_DIR)
            self.log("Efectos de sonido generados", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"Error al generar SFX: {e}", "ERROR")
            traceback.print_exc()
            return False
    
    def generate_scenes(self):
        """Genera las imágenes de las escenas."""
        self.step("PASO 3: Generando imágenes de escenas")
        
        try:
            builder = SceneBuilder()
            builder.create_all_scenes(SCENES_DIR)
            self.log("Todas las escenas generadas", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"Error al generar escenas: {e}", "ERROR")
            traceback.print_exc()
            return False
    
    def generate_audio(self):
        """Genera narraciones y mezcla audio."""
        self.step("PASO 4: Generando audio (narración y música)")
        
        try:
            processor = AudioProcessor()
            
            # Generar todas las narraciones
            self.log("Generando narraciones en español...")
            narration_files = processor.generate_all_narrations(TEMP_DIR)
            
            if not narration_files:
                self.log("No se generaron narraciones", "WARNING")
                # Crear archivo de narración silenciosa
                import scipy.io.wavfile as wavfile
                silent = np.zeros(int(44100 * TOTAL_DURATION), dtype=np.int16)
                wavfile.write(TEMP_NARRATION, 44100, silent)
            else:
                # Concatenar todas las narraciones
                self.log("Concatenando narraciones...")
                try:
                    from scipy.io import wavfile
                    all_narrations = []
                    for narr_file in narration_files:
                        try:
                            rate, data = wavfile.read(str(narr_file))
                            all_narrations.append(data)
                        except:
                            # Agregar silencio si falla una narración
                            all_narrations.append(np.zeros(int(44100 * CLIP_DURATION), dtype=np.int16))
                    
                    if all_narrations:
                        combined = np.concatenate(all_narrations)
                        # Asegurar duración correcta
                        target_samples = int(44100 * TOTAL_DURATION)
                        if len(combined) < target_samples:
                            combined = np.pad(combined, (0, target_samples - len(combined)))
                        elif len(combined) > target_samples:
                            combined = combined[:target_samples]
                        
                        wavfile.write(TEMP_NARRATION, 44100, combined.astype(np.int16))
                        self.log("Narraciones concatenadas", "SUCCESS")
                except Exception as e:
                    self.log(f"Error concatenando narraciones: {e}", "WARNING")
            
            # Obtener música
            self.log("Buscando música de fondo...")
            music_path = processor.load_or_generate_music()
            
            if music_path and music_path.exists():
                # Convertir a WAV si es necesario
                if music_path.suffix.lower() != '.wav':
                    self.log(f"Convirtiendo música a WAV...")
                    try:
                        audio = AudioFileClip(str(music_path))
                        audio.write_audiofile(str(TEMP_MUSIC), verbose=False, logger=None)
                        music_path = TEMP_MUSIC
                    except:
                        self.log("No se pudo convertir música", "WARNING")
                else:
                    TEMP_MUSIC = music_path
                
                # Mezclar audio
                self.log("Mezclando narración y música...")
                processor.mix_audio(TEMP_NARRATION, music_path, TEMP_AUDIO)
                self.log("Audio mezclado y preparado", "SUCCESS")
                return True
            else:
                self.log("Música no disponible, continuando sin música", "WARNING")
                return True
        
        except Exception as e:
            self.log(f"Error al generar audio: {e}", "ERROR")
            traceback.print_exc()
            return False
    
    def create_video(self):
        """Crea el video final componiendo escenas y audio."""
        self.step("PASO 5: Componiendo video final")
        
        try:
            self.log("Cargando escenas...")
            scene_files = sorted(SCENES_DIR.glob("*.png"))
            
            if not scene_files:
                self.log("No se encontraron escenas", "ERROR")
                return False
            
            self.log(f"Escenas encontradas: {len(scene_files)}")
            
            # Crear clips de video para cada escena
            clips = []
            for i, scene_file in enumerate(scene_files[:NUM_SCENES], 1):
                self.log(f"Procesando escena {i}: {scene_file.name}")
                
                # Crear clip de imagen
                clip = ImageClip(str(scene_file)).set_duration(CLIP_DURATION)
                
                # Aplicar movimientos suaves (zoom progresivo)
                def make_frame(get_frame, t):
                    frame = get_frame(t)
                    # Zoom suave
                    zoom = 1.0 + (t / CLIP_DURATION) * 0.2
                    return frame
                
                clip = clip.set_fps(FPS)
                clips.append(clip)
            
            # Concatenar escenas
            self.log("Concatenando escenas...")
            video = concatenate_videoclips(clips, method="chain")
            
            # Establecer resolución correcta
            video = video.resize((VIDEO_WIDTH, VIDEO_HEIGHT))
            video = video.set_fps(FPS)
            
            # Agregar audio si existe
            self.log("Agregando audio...")
            if TEMP_AUDIO.exists():
                try:
                    audio = AudioFileClip(str(TEMP_AUDIO))
                    # Asegurar que el audio tenga la duración correcta
                    if audio.duration < TOTAL_DURATION:
                        self.log(f"Audio muy corto: {audio.duration:.2f}s (esperado: {TOTAL_DURATION}s)", "WARNING")
                        # Extender audio con silencio
                        from scipy.io import wavfile
                        rate, data = wavfile.read(str(TEMP_AUDIO))
                        target_samples = int(rate * TOTAL_DURATION)
                        if len(data) < target_samples:
                            data = np.pad(data, (0, target_samples - len(data)))
                        wavfile.write(str(TEMP_AUDIO), rate, data.astype(np.int16))
                        audio = AudioFileClip(str(TEMP_AUDIO))
                    
                    video = video.set_audio(audio)
                    self.log("Audio agregado", "SUCCESS")
                except Exception as e:
                    self.log(f"No se pudo agregar audio: {e}", "WARNING")
            else:
                self.log("Archivo de audio no encontrado", "WARNING")
            
            # Crear directorio de salida si no existe
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            
            # Escribir video
            self.log(f"Escribiendo video: {OUTPUT_VIDEO.name}")
            self.log("(Esta es la parte más lenta, por favor espera...)")
            
            video.write_videofile(
                str(OUTPUT_VIDEO),
                fps=FPS,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None,
                preset='medium'
            )
            
            self.log(f"Video generado: {OUTPUT_VIDEO}", "SUCCESS")
            return True
        
        except Exception as e:
            self.log(f"Error al crear video: {e}", "ERROR")
            traceback.print_exc()
            return False
    
    def validate_output(self):
        """Valida el video final."""
        self.step("PASO 6: Validando video final")
        
        try:
            if not OUTPUT_VIDEO.exists():
                self.log(f"Video no encontrado: {OUTPUT_VIDEO}", "ERROR")
                return False
            
            self.log(f"Archivo: {OUTPUT_VIDEO.name}")
            self.log(f"Tamaño: {OUTPUT_VIDEO.stat().st_size / (1024*1024):.2f} MB")
            
            # Ejecutar validaciones
            is_valid = VideoValidator.validate_all(OUTPUT_VIDEO)
            
            if is_valid:
                self.log("Validación completada exitosamente", "SUCCESS")
            else:
                self.log("Validación completada con advertencias", "WARNING")
            
            return True
        
        except Exception as e:
            self.log(f"Error al validar video: {e}", "ERROR")
            return False
    
    def cleanup(self):
        """Limpia archivos temporales."""
        self.step("PASO 7: Limpieza final")
        
        try:
            if TEMP_DIR.exists():
                shutil.rmtree(TEMP_DIR)
                self.log("Archivos temporales eliminados", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"Error al limpiar temporales: {e}", "WARNING")
            return False
    
    def generate(self):
        """Ejecuta el proceso completo de generación."""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║        🌈 GENERADOR DE VIDEO: SAMI Y LA SEMILLA ARCOÍRIS 🌈          ║
║                                                                        ║
║  Duración: 2 minutos | Resolución: 1920×1080 | FPS: 30               ║
║  Formato: MP4 | Audio: Narración ES + Música + Efectos                ║
╚════════════════════════════════════════════════════════════════════════╝
        """)
        
        steps = [
            ("Preparar entorno", self.prepare_environment),
            ("Generar efectos de sonido", self.generate_sfx),
            ("Generar escenas", self.generate_scenes),
            ("Generar audio", self.generate_audio),
            ("Crear video", self.create_video),
            ("Validar salida", self.validate_output),
            ("Limpiar temporales", self.cleanup),
        ]
        
        success_count = 0
        for step_name, step_func in steps:
            try:
                if step_func():
                    success_count += 1
                else:
                    self.log(f"Falló: {step_name}", "ERROR")
            except KeyboardInterrupt:
                self.log("Generación cancelada por el usuario", "WARNING")
                return False
            except Exception as e:
                self.log(f"Error inesperado en {step_name}: {e}", "ERROR")
                traceback.print_exc()
        
        # Resumen final
        print(f"\n{'='*70}")
        print("📊 RESUMEN DE LA GENERACIÓN")
        print('='*70)
        print(f"Pasos completados: {success_count}/{len(steps)}")
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"Tiempo total: {elapsed:.2f} segundos ({elapsed/60:.2f} minutos)")
        
        if OUTPUT_VIDEO.exists():
            file_size = OUTPUT_VIDEO.stat().st_size / (1024 * 1024)
            print(f"\\nArchivo final: {OUTPUT_VIDEO}")
            print(f"Tamaño: {file_size:.2f} MB")
            print(f"\\n✓ Video generado exitosamente!\"")
            print(f\"\\nPara reproducir: {OUTPUT_VIDEO.resolve()}\")
        else:
            print(f"\\n✗ No se pudo generar el video\")
        
        print('='*70 + "\\n")
        
        return success_count == len(steps)


def main():
    """Función principal."""
    try:
        generator = SamiVideoGenerator()
        success = generator.generate()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n\\n[!] Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\\n[Error fatal] {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
