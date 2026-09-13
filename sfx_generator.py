# Generador de efectos de sonido sintetizados
import numpy as np
from scipy.io import wavfile
from scipy import signal
from pathlib import Path
import os

class SFXGenerator:
    """Genera efectos de sonido sintetizados para usar como placeholders."""
    
    def __init__(self, sample_rate=44100, duration=2):
        self.sample_rate = sample_rate
        self.duration = duration
        self.num_samples = int(sample_rate * duration)
    
    def generate_birds(self):
        """Genera sonido de pájaros chirriando."""
        t = np.linspace(0, self.duration, self.num_samples)
        # Múltiples frecuencias de pájaros
        freqs = [1000, 1500, 2000, 1200, 1800]
        sound = np.zeros(self.num_samples)
        
        for i, freq in enumerate(freqs):
            # Modulación de amplitud para efecto de chirriante
            envelope = signal.windows.hann(self.num_samples)
            wave = np.sin(2 * np.pi * freq * t) * envelope
            # Desplazar en tiempo
            shift = int(i * self.num_samples / len(freqs))
            sound[shift:] += wave[:-shift] if shift > 0 else wave
        
        sound = sound / np.max(np.abs(sound))  # Normalizar
        sound = (sound * 32767).astype(np.int16)
        return sound
    
    def generate_wind(self):
        """Genera sonido de viento."""
        # Ruido blanco filtrado para simular viento
        wind_noise = np.random.randn(self.num_samples) * 0.3
        
        # Aplicar filtro pasa bajos para efecto de viento suave
        b, a = signal.butter(2, 0.3, btype='low')
        wind = signal.filtfilt(b, a, wind_noise)
        
        # Envolvente para que se desvanezca
        envelope = np.linspace(1, 0, self.num_samples)
        wind = wind * envelope
        
        wind = wind / np.max(np.abs(wind))  # Normalizar
        wind = (wind * 32767).astype(np.int16)
        return wind
    
    def generate_water(self):
        """Genera sonido de agua/riachuelo."""
        t = np.linspace(0, self.duration, self.num_samples)
        # Ruido de agua con tonos bajos
        water_noise = np.random.randn(self.num_samples) * 0.4
        
        # Oscilaciones bajas para efecto de agua
        low_freq = 200
        low_tone = np.sin(2 * np.pi * low_freq * t) * 0.2
        water = water_noise + low_tone
        
        # Filtro pasa bajos
        b, a = signal.butter(2, 0.2, btype='low')
        water = signal.filtfilt(b, a, water)
        
        water = water / np.max(np.abs(water))  # Normalizar
        water = (water * 32767).astype(np.int16)
        return water
    
    def generate_magic(self):
        """Genera sonido mágico (twinkle/tintineo)."""
        t = np.linspace(0, self.duration, self.num_samples)
        # Acordes mágicos ascendentes
        freqs = [1046, 1318, 1568, 1976, 2093]  # Do, Mi, Sol, Si, Do (octava)
        sound = np.zeros(self.num_samples)
        
        samples_per_freq = self.num_samples // len(freqs)
        for i, freq in enumerate(freqs):
            start = i * samples_per_freq
            end = start + samples_per_freq
            t_seg = np.linspace(0, self.duration/len(freqs), end-start)
            # Envolvente de campana para efecto mágico
            envelope = signal.windows.hann(end-start)
            wave = np.sin(2 * np.pi * freq * t_seg) * envelope
            sound[start:end] = wave
        
        sound = sound / np.max(np.abs(sound))  # Normalizar
        sound = (sound * 32767).astype(np.int16)
        return sound
    
    def generate_animals(self):
        """Genera sonidos de animales (ovejas, vacas, pollos)."""
        t = np.linspace(0, self.duration, self.num_samples)
        animal_sounds = np.zeros(self.num_samples)
        
        # Sonido de oveja (balido)
        sheep_freq = 500
        sheep_sound = np.sin(2 * np.pi * sheep_freq * t) * 0.2
        
        # Sonido de vaca (mugido)
        cow_freq = 300
        cow_sound = np.sin(2 * np.pi * cow_freq * t) * 0.2
        
        # Sonido de pollo (cacareo)
        chicken_freq = 2000
        chicken_sound = np.sin(2 * np.pi * chicken_freq * t) * 0.1
        
        # Combinar con envolventes
        t1 = self.num_samples // 3
        t2 = 2 * self.num_samples // 3
        
        animal_sounds[:t1] = sheep_sound[:t1]
        animal_sounds[t1:t2] = cow_sound[t1:t2]
        animal_sounds[t2:] = chicken_sound[t2:]
        
        animal_sounds = animal_sounds / np.max(np.abs(animal_sounds))  # Normalizar
        animal_sounds = (animal_sounds * 32767).astype(np.int16)
        return animal_sounds
    
    def save_sfx(self, output_dir):
        """Genera y guarda todos los efectos de sonido."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("[SFX] Generando efectos de sonido...")
        
        sfx_dict = {
            "birds.wav": self.generate_birds(),
            "wind.wav": self.generate_wind(),
            "water.wav": self.generate_water(),
            "magic.wav": self.generate_magic(),
            "animals.wav": self.generate_animals()
        }
        
        for filename, audio_data in sfx_dict.items():
            filepath = output_dir / filename
            wavfile.write(filepath, self.sample_rate, audio_data)
            print(f"✓ {filename} generado ({filepath})")
        
        return sfx_dict


if __name__ == "__main__":
    from config import SFX_DIR
    generator = SFXGenerator(duration=3)
    generator.save_sfx(SFX_DIR)
    print("\n✓ Todos los efectos de sonido han sido generados.")
