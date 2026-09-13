# Validador de video: verifica duración, resolución, audio y sincronización
import subprocess
import json
from pathlib import Path
from config import (
    MIN_DURATION, MAX_DURATION, EXPECTED_WIDTH, EXPECTED_HEIGHT,
    EXPECTED_ASPECT_RATIO, TOLERANCE_ASPECT
)

class VideoValidator:
    """Valida las especificaciones del video final."""
    
    @staticmethod
    def get_video_info(video_path):
        """Obtiene información del video usando ffprobe."""
        try:
            result = subprocess.run(
                [
                    'ffprobe', '-v', 'error',
                    '-show_entries', 'format=duration:stream=width,height,r_frame_rate,codec_type',
                    '-of', 'json',
                    str(video_path)
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"[Error] No se pudo obtener info del video: {e}")
            return None
    
    @staticmethod
    def validate_duration(video_path, min_duration=MIN_DURATION, max_duration=MAX_DURATION):
        """Valida la duración del video."""
        print("[Validar] Verificando duración...")
        info = VideoValidator.get_video_info(video_path)
        
        if info and 'format' in info and 'duration' in info['format']:
            duration = float(info['format']['duration'])
            print(f"  Duración: {duration:.2f}s (esperado: 120s)")
            
            if min_duration <= duration <= max_duration:
                print("✓ Duración válida")
                return True
            else:
                print(f"✗ Duración fuera de rango: {duration:.2f}s ({min_duration}-{max_duration}s)")
                return False
        return False
    
    @staticmethod
    def validate_resolution(video_path, expected_width=EXPECTED_WIDTH, expected_height=EXPECTED_HEIGHT):
        """Valida la resolución del video."""
        print("[Validar] Verificando resolución...")
        info = VideoValidator.get_video_info(video_path)
        
        if info and 'streams' in info:
            for stream in info['streams']:
                if stream.get('codec_type') == 'video':
                    width = stream.get('width')
                    height = stream.get('height')
                    print(f"  Resolución: {width}×{height} (esperado: {expected_width}×{expected_height})")
                    
                    if width == expected_width and height == expected_height:
                        print("✓ Resolución válida")
                        return True
                    else:
                        print(f"✗ Resolución incorrecta: {width}×{height}")
                        return False
        return False
    
    @staticmethod
    def validate_aspect_ratio(video_path, expected_ratio=EXPECTED_ASPECT_RATIO, tolerance=TOLERANCE_ASPECT):
        """Valida la relación de aspecto."""
        print("[Validar] Verificando relación de aspecto...")
        info = VideoValidator.get_video_info(video_path)
        
        if info and 'streams' in info:
            for stream in info['streams']:
                if stream.get('codec_type') == 'video':
                    width = stream.get('width')
                    height = stream.get('height')
                    if width and height:
                        actual_ratio = width / height
                        print(f"  Relación: {actual_ratio:.4f} (esperado: {expected_ratio:.4f})")
                        
                        if abs(actual_ratio - expected_ratio) <= tolerance:
                            print("✓ Relación de aspecto válida (16:9)")
                            return True
                        else:
                            print(f"✗ Relación de aspecto incorrecta: {actual_ratio:.4f}")
                            return False
        return False
    
    @staticmethod
    def validate_audio(video_path):
        """Valida que el video tiene audio."""
        print("[Validar] Verificando audio...")
        info = VideoValidator.get_video_info(video_path)
        
        if info and 'streams' in info:
            for stream in info['streams']:
                if stream.get('codec_type') == 'audio':
                    print("✓ Audio presente")
                    return True
        print("✗ Sin audio detectado")
        return False
    
    @staticmethod
    def validate_fps(video_path, expected_fps=30):
        """Valida los FPS del video."""
        print("[Validar] Verificando FPS...")
        info = VideoValidator.get_video_info(video_path)
        
        if info and 'streams' in info:
            for stream in info['streams']:
                if stream.get('codec_type') == 'video':
                    frame_rate = stream.get('r_frame_rate')
                    if frame_rate:
                        # Parsear frame_rate (ej: "30/1")
                        try:
                            num, den = map(int, frame_rate.split('/'))
                            fps = num / den
                            print(f"  FPS: {fps:.2f} (esperado: {expected_fps})")
                            
                            if abs(fps - expected_fps) < 1:
                                print("✓ FPS válido (30fps)")
                                return True
                            else:
                                print(f"⚠ FPS diferente: {fps:.2f}")
                                return False
                        except:
                            pass
        return False
    
    @staticmethod
    def validate_all(video_path):
        """Ejecuta todas las validaciones."""
        print("\n" + "="*60)
        print("VALIDACIÓN DE VIDEO FINAL")
        print("="*60)
        
        video_path = Path(video_path)
        if not video_path.exists():
            print(f"✗ Video no encontrado: {video_path}")
            return False
        
        print(f"\nArchivo: {video_path.name}")
        print(f"Tamaño: {video_path.stat().st_size / (1024*1024):.2f} MB")
        print()
        
        results = {
            "duration": VideoValidator.validate_duration(video_path),
            "resolution": VideoValidator.validate_resolution(video_path),
            "aspect_ratio": VideoValidator.validate_aspect_ratio(video_path),
            "audio": VideoValidator.validate_audio(video_path),
            "fps": VideoValidator.validate_fps(video_path)
        }
        
        print()
        print("="*60)
        if all(results.values()):
            print("✓ VALIDACIÓN COMPLETADA: ÉXITO")
            print("El video cumple con todas las especificaciones.")
        else:
            failed = [k for k, v in results.items() if not v]
            print(f"⚠ VALIDACIÓN PARCIAL: {len(failed)} error(es)")
            print(f"Fallos: {', '.join(failed)}")
        print("="*60 + "\n")
        
        return all(results.values())


if __name__ == "__main__":
    from config import OUTPUT_VIDEO
    VideoValidator.validate_all(OUTPUT_VIDEO)
