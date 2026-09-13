# Constructor de escenas con placeholders y movimientos
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
from config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, SCENES_DIR, CHARACTERS_DIR,
    COLORS, SCENE_FILES, CHARACTER_FILES
)

class SceneBuilder:
    """Construye escenas infantiles con placeholders y animaciones."""
    
    def __init__(self):
        self.width = VIDEO_WIDTH
        self.height = VIDEO_HEIGHT
    
    def create_gradient_background(self, color1, color2, direction="vertical"):
        """Crea un fondo con gradiente infantil."""
        image = Image.new('RGB', (self.width, self.height))
        pixels = image.load()
        
        if direction == "vertical":
            for y in range(self.height):
                ratio = y / self.height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                for x in range(self.width):
                    pixels[x, y] = (r, g, b)
        
        return image
    
    def add_text_to_image(self, image, text, position=(960, 540), font_size=80, color=(255, 255, 255)):
        """Añade texto a una imagen."""
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calcular posición centrada si es necesario
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        
        # Dibujar sombra para mejor legibilidad
        draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0))
        draw.text((x, y), text, font=font, fill=color)
        
        return image
    
    def create_scene_1_seed_falling(self):
        """Escena 1: Semilla cayendo del cielo."""
        print("[Scene] Creando escena 1: Semilla cayendo...")
        img = self.create_gradient_background(COLORS["sky_blue"], COLORS["grass_green"])
        img = self.add_text_to_image(img, "✨ Semilla Arcoíris ✨", font_size=120, color=(255, 215, 0))
        return img
    
    def create_scene_2_planting(self):
        """Escena 2: Plantando la semilla."""
        print("[Scene] Creando escena 2: Plantando...")
        img = self.create_gradient_background(COLORS["sky_blue"], COLORS["grass_green"])
        img = self.add_text_to_image(img, "🌱 Plantando la semilla 🌱", font_size=100, color=(255, 255, 255))
        return img
    
    def create_scene_3_wind_blast(self):
        """Escena 3: Viento llevándose el brote."""
        print("[Scene] Creando escena 3: Viento travieso...")
        img = self.create_gradient_background(COLORS["sky_blue"], COLORS["grass_green"])
        img = self.add_text_to_image(img, "💨 ¡El viento! 💨", font_size=110, color=(200, 200, 200))
        return img
    
    def create_scene_4_cow_canela(self):
        """Escena 4: Vaca Canela ayudando."""
        print("[Scene] Creando escena 4: Vaca Canela...")
        img = self.create_gradient_background(COLORS["sky_blue"], COLORS["grass_green"])
        img = self.add_text_to_image(img, "🐄 Canela ayuda 🐄", font_size=100, color=(139, 69, 19))
        return img
    
    def create_scene_5_crossing_stream(self):
        """Escena 5: Cruzando el riachuelo con patitos."""
        print("[Scene] Creando escena 5: Cruzando riachuelo...")
        img = self.create_gradient_background(COLORS["sky_blue"], (100, 200, 255))
        img = self.add_text_to_image(img, "🦆 Cruzando el riachuelo 🦆", font_size=90, color=(255, 255, 255))
        return img
    
    def create_scene_6_animals_help(self):
        """Escena 6: Todos los animales ayudan."""
        print("[Scene] Creando escena 6: Ayuda de animales...")
        img = self.create_gradient_background(COLORS["sky_blue"], COLORS["grass_green"])
        img = self.add_text_to_image(img, "🐾 La magia despierta 🐾", font_size=100, color=(255, 100, 255))
        return img
    
    def create_scene_7_rainbow_tree(self):
        """Escena 7: Árbol arcoíris creciendo."""
        print("[Scene] Creando escena 7: Árbol arcoíris...")
        img = self.create_gradient_background(COLORS["sky_blue"], COLORS["grass_green"])
        # Dibujar un árbol arcoíris simple
        draw = ImageDraw.Draw(img)
        # Tronco
        draw.rectangle([900, 700, 1020, 900], fill=(139, 69, 19))
        # Follaje con colores arcoíris
        colors_rainbow = [
            COLORS["rainbow_red"],
            COLORS["rainbow_orange"],
            COLORS["rainbow_yellow"],
            COLORS["rainbow_green"],
            COLORS["rainbow_blue"],
            COLORS["rainbow_indigo"],
            COLORS["rainbow_violet"]
        ]
        for i, color in enumerate(colors_rainbow):
            y = 600 - i * 80
            draw.ellipse([700, y, 1220, y + 200], fill=color)
        img = self.add_text_to_image(img, "🌈 ¡El árbol arcoíris! 🌈", font_size=90, color=(255, 255, 255))
        return img
    
    def create_scene_8_sharing_fruits(self):
        """Escena 8: Sami repartiendo frutas."""
        print("[Scene] Creando escena 8: Compartiendo frutas...")
        img = self.create_gradient_background(COLORS["sky_blue"], COLORS["grass_green"])
        img = self.add_text_to_image(img, "🍎 Compartiendo magia 🍎", font_size=100, color=(255, 100, 100))
        return img
    
    def create_all_scenes(self, output_dir=None):
        """Crea todas las escenas y las guarda como archivos PNG."""
        if output_dir is None:
            output_dir = SCENES_DIR
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        scenes = [
            ("seed_falling.png", self.create_scene_1_seed_falling),
            ("planting.png", self.create_scene_2_planting),
            ("wind_blast.png", self.create_scene_3_wind_blast),
            ("cow_canela.png", self.create_scene_4_cow_canela),
            ("crossing_stream.png", self.create_scene_5_crossing_stream),
            ("animals_help.png", self.create_scene_6_animals_help),
            ("rainbow_tree.png", self.create_scene_7_rainbow_tree),
            ("sharing_fruits.png", self.create_scene_8_sharing_fruits)
        ]
        
        for filename, create_func in scenes:
            filepath = output_dir / filename
            if not filepath.exists():
                img = create_func()
                img.save(filepath)
                print(f"✓ {filename} guardado ({filepath})")
            else:
                print(f"⊘ {filename} ya existe, saltando...")
        
        print(f"\n✓ Todas las escenas placeholder creadas en {output_dir}")
    
    def create_character_placeholder(self, name, color, output_dir=None):
        """Crea un personaje placeholder."""
        if output_dir is None:
            output_dir = CHARACTERS_DIR
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear imagen con gradiente
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Dibujar círculo base (cabeza)
        draw.ellipse([50, 50, 350, 350], fill=color)
        
        # Dibujar ojos
        draw.ellipse([120, 150, 160, 190], fill=(255, 255, 255))
        draw.ellipse([240, 150, 280, 190], fill=(255, 255, 255))
        draw.ellipse([135, 165, 145, 175], fill=(0, 0, 0))
        draw.ellipse([255, 165, 265, 175], fill=(0, 0, 0))
        
        # Añadir texto
        filename = f"{name}.png"
        filepath = output_dir / filename
        if not filepath.exists():
            img.save(filepath)
            print(f"✓ {filename} creado ({filepath})")
        else:
            print(f"⊘ {filename} ya existe, saltando...")


if __name__ == "__main__":
    builder = SceneBuilder()
    builder.create_all_scenes()
    print("\n✓ Todas las escenas han sido creadas.")
