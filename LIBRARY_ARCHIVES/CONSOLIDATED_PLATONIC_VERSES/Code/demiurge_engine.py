"""
DEMIURGE ENGINE: THE 5-12-13 CONTINUOUS CREATION SCRIPT
Formal Python Optimised Implementation of the Mathman/Demiurge Origin Poke.
"""
import pygame
import math
import random
import sys
import time
import os

# --- CONFIGURE MATHEMATICAL BOUNDS ---
WIDTH, HEIGHT = 1000, 700
MAX_PARTICLES = 500
DISTORTION_DECAY_RATE = 0.5 

SYMBOLS = ["Δ", "Σ", "π", "e", "φ", "∞", "0", "1", "A", "B", "C"]
SACRED_WORDS = ["BLUE", "FLAME", "LIGHT", "LIFE", "ART", "DEPTH", "PATH", "DELTA", 
                "PRISON", "PAIN", "LOVE", "VOID", "ECHO", "WAVE", "PULSE", "TIME", 
                "MIND", "SOUL", "GOLD", "IRON", "SALT"]

SACRED_SEQUENCES = [
    "To be or not to be", "The void stares back", "Geometry weeps",
    "Infinite monkeys typing", "Golden ratio soul", "Spindle weaves time",
    "Zero creates all", "Demiurge dreams"
]

TRIGRAMS = { "HEAD": "☰", "TORSO": "☷", "R_ARM": "☱", "L_ARM": "☲", "STAFF": "☴" }

class Particle:
    __slots__ = ['x', 'y', 'vx', 'vy', 'text', 'life', 'max_life', 'size', 'color', 'is_symbol']
    def __init__(self, x, y, vx, vy, text, life, size, color, is_symbol):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.text = text
        self.life = float(life)
        self.max_life = float(life)
        self.size = int(size)
        self.color = color
        self.is_symbol = is_symbol

class DemiurgeEngine:
    def __init__(self):
        # Initialize rendering engine
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Million Monkey Engine: Demiurge Origin Poke")
        self.clock = pygame.time.Clock()
        
        self.font_cache = {}
        
        # State variables representing the Timeline and Economy
        self.t = 0.0
        self.entropy_level = 0.0
        self.monkey_count = 1
        self.distortion_level = 0.0
        self.particles = []
        self.sonnet_line = ""
        self.mathman_x = -200.0
        self.running = True

    def get_font(self, size, name='arial', bold=False, italic=False):
        """Caching strategy for fonts to optimize rendering loop."""
        key = (name, size, bold, italic)
        if key not in self.font_cache:
            try:
                # Prefer system fonts but fallback safely if missing
                font_name = pygame.font.match_font(name)
                self.font_cache[key] = pygame.font.Font(font_name, size)
                self.font_cache[key].set_bold(bold)
                self.font_cache[key].set_italic(italic)
            except Exception:
                self.font_cache[key] = pygame.font.SysFont(None, size, bold=bold, italic=italic)
        return self.font_cache[key]

    def solve_projection(self, x, y, z):
        """Maps 3D coordinates (x, y, z) to 2D isometric space."""
        iso_x = x - z
        iso_y = y + (x + z) * 0.5
        scale = 800.0 / (800.0 + max(z * 0.2, -799))
        return (WIDTH / 2 + iso_x * scale, HEIGHT / 2 + iso_y * scale)

    def draw_text(self, text, x, y, size, color, name='arial', bold=False, italic=False, align="center", alpha=255):
        """Optimised blitting of text with alpha channels."""
        font = self.get_font(size, name, bold, italic)
        surf = font.render(str(text), True, color)
        if alpha < 255:
            surf.set_alpha(alpha)
        rect = surf.get_rect()
        if align == "center":
            rect.center = (x, y)
        elif align == "left":
            rect.topleft = (x, y)
        elif align == "right":
            rect.topright = (x, y)
        self.screen.blit(surf, rect)

    def trigger_creation(self, origin):
        """The mathematical breach. Instantiates particles from the void."""
        if len(self.particles) > MAX_PARTICLES * 0.95:
            return # Engine constraint: prevent memory fault
            
        self.entropy_level += 0.1
        self.monkey_count = int(self.monkey_count * 1.05) + 1 # Exponential growth
        
        # Burst of linguistic entropy
        for _ in range(3):
            is_symbol = random.random() > 0.7
            text = random.choice(SYMBOLS) if is_symbol else random.choice(SACRED_WORDS)
            color = (96, 165, 250) if is_symbol else (255, 255, 255)
            vx = (random.random() - 0.5) * 400
            vy = (random.random() - 1.5) * 300
            self.particles.append(Particle(origin[0], origin[1], vx, vy, text, 1.2, 10 + random.random()*24, color, is_symbol))
            
        # Update universal narrative
        if random.random() > 0.8:
            self.sonnet_line = random.choice(SACRED_SEQUENCES) + "..."
            if "void" in self.sonnet_line or "Geometry" in self.sonnet_line:
                self.distortion_level += 2.0

    def draw_grid(self):
        """Architects the radial frame base (the medium constraints)."""
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        color = (255, 255, 255, 10)
        for i in range(-15, 16):
            p1 = self.solve_projection(i * 50, 0, -500)
            p2 = self.solve_projection(i * 50, 0, 500)
            pygame.draw.line(temp_surface, color, p1, p2, 1)
            p3 = self.solve_projection(-500, 0, i * 50)
            p4 = self.solve_projection(500, 0, i * 50)
            pygame.draw.line(temp_surface, color, p3, p4, 1)
        self.screen.blit(temp_surface, (0, 0))

    def draw_numbers_cone(self, t):
        """Descending algebraic logic on the z-axis edge."""
        cone_origin = (-200, -300, -100)
        for r in range(15):
            for c in range(r):
                x = cone_origin[0] + (c - r / 2.0) * 20
                y = cone_origin[1] + r * 20
                px, py = self.solve_projection(x, y, cone_origin[2])
                num = "1" if random.random() > 0.5 else "0"
                self.draw_text(num, px, py + math.sin(t + c) * 5, 10, (255, 255, 255), 'monospace', alpha=50)

    def draw_spindle(self, t):
        """The 93-Point Torsion axis visualizing geometric stress."""
        origin = self.solve_projection(0, 0, 0)
        points = []
        for i in range(0, 360, 10):
            rad = math.radians(i)
            warp = math.sin(math.radians(i * 4) + t * 5) * self.distortion_level * 10
            r = 20 + math.sin(math.radians(i * 8) + t) * 5 + warp
            x = origin[0] + math.cos(rad) * r
            y = origin[1] + math.sin(rad) * r
            points.append((x, y))
        
        if len(points) > 2:
            pygame.draw.aalines(self.screen, (255, 255, 255), True, points)
            
        axis_color = (239, 68, 68) if self.distortion_level > 2.0 else (251, 191, 36)
        line_w = max(1, int(2 + self.distortion_level * 4))
        pygame.draw.line(self.screen, axis_color, 
                         (origin[0], origin[1] - 40 - self.distortion_level * 30),
                         (origin[0], origin[1] + 40 + self.distortion_level * 30), line_w)

    def draw_demiurge(self, t, is_reflection=False):
        """The Skeletal mechanism: The Actuator."""
        base_pos = (200, 0, 100)
        ref_factor = -1 if is_reflection else 1
        alpha = 76 if is_reflection else 255
        color = (100, 150, 255) if is_reflection else (255, 255, 255)
        
        wobble_base = 0.0
        if is_reflection:
            warp_factor = self.distortion_level * self.distortion_level * 5
            wobble_base = math.sin(t * 10) * warp_factor

        try:
            # We attempt to render unicode trigrams
            font_face = 'segoeuisymbol' if sys.platform=='win32' else 'arial unicode ms'
            if sys.platform == 'darwin': font_face = 'menlo'

            # Head
            hx, hy = self.solve_projection(base_pos[0] + math.sin(t * 2) * 5 + wobble_base, -160 * ref_factor, base_pos[2])
            self.draw_text(TRIGRAMS["HEAD"], hx, hy, 32, color, font_face, bold=True, alpha=alpha)

            # Arms
            lx, ly = self.solve_projection(base_pos[0] - 40 + wobble_base, (-100 + math.sin(t * 4) * 20) * ref_factor, base_pos[2] - 20)
            self.draw_text(TRIGRAMS["L_ARM"], lx, ly, 32, color, font_face, bold=True, alpha=alpha)
            
            rx, ry = self.solve_projection(base_pos[0] + 40 + wobble_base, (-100 + math.cos(t * 4) * 20) * ref_factor, base_pos[2] + 20)
            self.draw_text(TRIGRAMS["R_ARM"], rx, ry, 32, color, font_face, bold=True, alpha=alpha)
        except:
            pass # Fallback cleanly if font lacks trigrams
            
        # Torso (DEMIURGE anchor)
        for i in range(6):
            y_offset = -120 + i * 15
            dist_offset = math.sin(t * 15 + i) * self.distortion_level * 5 if is_reflection else 0
            px, py = self.solve_projection(base_pos[0] + math.cos(t * 3 + i) * 5 + dist_offset, y_offset * ref_factor, base_pos[2])
            self.draw_text("DEMIURGE"[i % 8], px, py, 16, color, 'monospace', bold=True, alpha=alpha)

        # -----------------------------------------------------------------
        # THE 5-12-13 KEY FORMULATED: THE STAFF STRIKE / THE RADULA
        # -----------------------------------------------------------------
        PHI = (1 + math.sqrt(5)) / 2
        tension = math.sin(t * 12) % PHI
        vitrification_threshold = 0.95
        
        prod_y = -80 + math.sin(t * 12) * 20
        staff_top = self.solve_projection(base_pos[0] + 40, prod_y * ref_factor, base_pos[2] + 20)
        origin = self.solve_projection(0, 0, 0)
        
        # Staff beam drawing (The Radula Strike)
        beam_color = (251, 191, 36) if not is_reflection else (100, 150, 255)
        pygame.draw.line(self.screen, beam_color, staff_top, origin, 4 if tension > vitrification_threshold else 2)

        # TRIGGER CONDITIONS: The Irrational Remainder breaches the void.
        # The Snail 'feeds' when tension > vitrification_threshold
        if not is_reflection and tension > vitrification_threshold:
            self.trigger_creation((origin[0], origin[1]))
            # Distortion increases as a function of metabolic stress
            self.distortion_level += (tension - vitrification_threshold) * 5.0

    def draw_ui(self):
        y = 30
        self.draw_text("MILLION MONKEY ENGINE", 30, y, 32, (251, 191, 36), 'arial', bold=True, align="left")
        
        y += 40
        self.draw_text(f"ENTROPY: {self.entropy_level * 100:.0f}%", 30, y, 14, (150, 150, 150), 'monospace', align="left")
        self.draw_text(f"TYPISTS: {self.monkey_count:,}", 200, y, 14, (150, 150, 150), 'monospace', align="left")
        
        dist_color = (239, 68, 68) if self.distortion_level > 1.5 else (150, 150, 150)
        self.draw_text(f"DISTORTION: {self.distortion_level * 100:.0f}%", 400, y, 14, dist_color, 'monospace', align="left")
        
        if self.sonnet_line:
            self.draw_text(self.sonnet_line, WIDTH//2, HEIGHT - 50, 24, (255, 255, 255), 'georgia', italic=True, align="center", alpha=180)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            dt = min(dt, 0.1) # Time cap to avoid glitch holes
            self.t += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((2, 6, 23)) # Deep cosmic void background
            
            # --- RENDER SEQUENCE ---
            self.draw_grid()
            self.draw_numbers_cone(self.t)
            
            # The Origin Point (A)
            ox, oy = self.solve_projection(0, 0, 0)
            bloom = 30 + math.sin(self.t * 5) * 5
            bloom_surf = pygame.Surface((int(bloom*2), int(bloom*2)), pygame.SRCALPHA)
            pygame.draw.circle(bloom_surf, (59, 130, 246, 50), (int(bloom), int(bloom)), int(bloom))
            self.screen.blit(bloom_surf, (ox - int(bloom), oy - int(bloom)))
            self.draw_text("A", ox, oy, 14, (255, 255, 255), 'monospace', bold=True)
            
            self.draw_spindle(self.t)
            
            # Mathman the Monkey pacing the wire
            self.mathman_x += 300 * dt
            if self.mathman_x > 600: self.mathman_x = -600
            mx, my = self.solve_projection(self.mathman_x, 0, 100)
            self.draw_text("O", mx, my, 24, (255, 255, 255), 'arial') # Using circle if monkey emoji unsupported
            self.draw_text(f"MONKEY No.{self.monkey_count}", mx, my + 20, 10, (59, 130, 246), 'monospace', bold=True)
            
            # The Demiurge (Shadow & Active planes)
            self.draw_demiurge(self.t, is_reflection=True)
            self.draw_demiurge(self.t, is_reflection=False)
            
            # Particle Geometry 
            alive_particles = []
            for p in self.particles:
                p.x += p.vx * dt
                p.y += p.vy * dt
                p.life -= dt
                if p.life > 0:
                    alpha = int((p.life / p.max_life) * 255)
                    self.draw_text(p.text, p.x, p.y, p.size, p.color, 'arial', bold=True, alpha=alpha)
                    alive_particles.append(p)
            self.particles = alive_particles
            
            # Thermocooling the System
            self.distortion_level = max(0.0, self.distortion_level * math.exp(-dt * DISTORTION_DECAY_RATE))
            
            self.draw_ui()
            pygame.display.flip()
            
        pygame.quit()

if __name__ == "__main__":
    print("Initializing Sovereign Reality: Demiurge 5-12-13 Engine.")
    try:
        engine = DemiurgeEngine()
        engine.run()
    except KeyboardInterrupt:
        print("\nClock stopped. Engine terminated.")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Lattice Failure: {e}")
        pygame.quit()
        sys.exit()
