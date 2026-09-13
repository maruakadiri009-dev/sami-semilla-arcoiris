# Procesador de audio: narración, música y efectos de sonido
import numpy as np
from scipy.io import wavfile
from scipy import signal
import edge_tts
import asyncio
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from config import (
    AUDIO_SAMPLE_RATE, AUDIO_CHANNELS, NARRATION_VOICE,
    MUSIC_VOLUME, DUCKING_LEVEL, NARRATION_VOLUME,
    TOTAL_DURATION, CLIP_DURATION, NARRATIONS, MUSIC_DIR,
    SFX_DIR, TEMP_DIR, TEMP_AUDIO, TEMP_NARRATION, TEMP_MUSIC
)

class AudioProcessor:
    """Procesa audio: narración, música y sincronización."""
    
    def __init__(self):
        self.sample_rate = AUDIO_SAMPLE_RATE
        self.duration = TOTAL_DURATION
        self.num_samples = int(self.sample_rate * self.duration)
    
    async def generate_narration_async(self, text, output_path):
        """Genera narración en español usando Edge TTS."""
        communicate = edge_tts.Communicate(text, NARRATION_VOICE, rate="-10%", volume="0%")
        await communicate.save(str(output_path))
    
    def generate_narration(self, text, output_path):
        """Genera narración (wrapper síncrono)."""
        try:
            asyncio.run(self.generate_narration_async(text, output_path))
            return True
        except Exception as e:
            print(f"[Error] No se pudo generar narración: {e}")
            return False
    
    def load_or_generate_music(self):
        """Carga música local o la genera como placeholder."""
        print("[Audio] Buscando música de fondo...")
        
        # Buscar archivos de música locales
        for music_file in MUSIC_DIR.glob("*"):
            if music_file.suffix.lower() in ['.mp3', '.wav', '.ogg']:
                print(f"✓ Música encontrada: {music_file.name}")
                return music_file
        
        print("[Audio] Música no encontrada. Generando placeholder...")
        return self.generate_placeholder_music()
    
    def generate_placeholder_music(self):
        """Genera música infantil placeholder."""
        output_path = MUSIC_DIR / "placeholder_music.wav"
        
        if output_path.exists():
            print(f"✓ Música placeholder ya existe: {output_path}")
            return output_path
        
        print(f"[Audio] Generando música placeholder ({output_path})...")
        t = np.linspace(0, self.duration, self.num_samples)
        
        # Melodía infantil simple (Do-Re-Mi-Fa-Sol)
        notes = [262, 294, 330, 349, 392]  # Hz
        repeats = self.duration // 5
        
        music = np.zeros(self.num_samples)
        samples_per_note = self.num_samples // (len(notes) * repeats)
        
        for repeat in range(int(repeats)):
            for i, note in enumerate(notes):
                start = int((repeat * len(notes) + i) * samples_per_note)
                end = int(start + samples_per_note)
                if end > self.num_samples:
                    end = self.num_samples
                
                t_seg = np.linspace(0, self.duration / (len(notes) * repeats), end - start)
                # Envolvente de campana
                envelope = signal.windows.hann(end - start)
                wave = np.sin(2 * np.pi * note * t_seg) * envelope * 0.1
                music[start:end] = wave
        
        # Normalizar y guardar
        music = music / np.max(np.abs(music))
        music = (music * 32767).astype(np.int16)
        
        wavfile.write(output_path, self.sample_rate, music)
        print(f"✓ Música placeholder generada: {output_path}")
        return output_path
    
    def apply_ducking(self, music_audio, narration_audio, ducking_level=DUCKING_LEVEL):
        """Reduce el volumen de la música cuando hay narración (ducking)."""
        print("[Audio] Aplicando ducking (música → 15% durante narración)...")
        
        # Crear máscara de narración
        # Detectar dónde hay sonido en la narración
        narration_energy = np.abs(narration_audio)
        
        # Suavizar la detección
        kernel_size = int(0.05 * self.sample_rate)  # 50ms
        kernel = np.ones(kernel_size) / kernel_size
        narration_mask = np.convolve(narration_energy, kernel, mode='same')
        
        # Normalizar máscara
        if np.max(narration_mask) > 0:
            narration_mask = narration_mask / np.max(narration_mask)
        
        # Aplicar ducking
        ducking_factor = 1 - (narration_mask * (1 - ducking_level))
        ducked_music = music_audio * ducking_factor
        
        return ducked_music
    
    def mix_audio(self, narration_path, music_path, output_path=None):
        """Mezcla narración y música con ducking."""
        if output_path is None:
            output_path = TEMP_AUDIO
        
        print("[Audio] Mezclando narración y música...")
        
        # Cargar archivos de audio
        try:
            nar_rate, narration_audio = wavfile.read(str(narration_path))
            print(f"✓ Narración cargada: {narration_path}")
        except Exception as e:
            print(f"[Error] No se pudo cargar narración: {e}")
            # Crear narración silenciosa
            narration_audio = np.zeros(self.num_samples)
            nar_rate = self.sample_rate
        
        try:
            mus_rate, music_audio = wavfile.read(str(music_path))
            print(f"✓ Música cargada: {music_path}")
        except Exception as e:
            print(f"[Error] No se pudo cargar música: {e}")
            music_audio = np.zeros(self.num_samples)
            mus_rate = self.sample_rate
        
        # Resample si es necesario
        if len(narration_audio) != self.num_samples:
            narration_audio = np.interp(
                np.linspace(0, 1, self.num_samples),
                np.linspace(0, 1, len(narration_audio)),
                narration_audio
            )
        
        if len(music_audio) != self.num_samples:
            music_audio = np.interp(
                np.linspace(0, 1, self.num_samples),
                np.linspace(0, 1, len(music_audio)),
                music_audio
            )
        
        # Normalizar
        if np.max(np.abs(narration_audio)) > 0:
            narration_audio = narration_audio / np.max(np.abs(narration_audio)) * NARRATION_VOLUME
        
        if np.max(np.abs(music_audio)) > 0:
            music_audio = music_audio / np.max(np.abs(music_audio)) * MUSIC_VOLUME
        
        # Aplicar ducking
        music_ducked = self.apply_ducking(music_audio, narration_audio)
        
        # Mezclar
        mixed = narration_audio + music_ducked
        
        # Prevenir clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 1.0:
            mixed = mixed / max_val * 0.95
        
        # Convertir a int16 y guardar
        mixed = (mixed * 32767).astype(np.int16)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        wavfile.write(str(output_path), self.sample_rate, mixed)
        
        print(f"✓ Audio mezclado guardado: {output_path}")
        return output_path
    
    def generate_all_narrations(self, output_dir=None):
        """Genera todas las narraciones."""
        if output_dir is None:
            output_dir = TEMP_DIR
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("[Audio] Generando narraciones en español...")
        narration_files = []
        
        for i, text in enumerate(NARRATIONS, 1):
            output_path = output_dir / f"narration_{i:02d}.wav"
            print(f"[{i}/8] Generando: {text[:50]}...")
            
            success = self.generate_narration(text, output_path)
            if success and output_path.exists():
                narration_files.append(output_path)
                print(f"✓ Narración {i} guardada")
            else:
                print(f"⚠ No se pudo generar narración {i}")
                # Crear archivo de silencio como placeholder
                silent = np.zeros(self.sample_rate * CLIP_DURATION, dtype=np.int16)
                wavfile.write(output_path, self.sample_rate, silent)
                narration_files.append(output_path)
        
        return narration_files


if __name__ == "__main__":
    processor = AudioProcessor()
    
    # Generar narraciones
    narrations = processor.generate_all_narrations()
    print(f"\n✓ {len(narrations)} narraciones generadas")
    
    # Generar música
    music = processor.load_or_generate_music()
    print(f"✓ Música: {music}")
