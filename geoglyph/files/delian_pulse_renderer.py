#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
DELIAN PULSE RENDERER
═══════════════════════════════════════════════════════════════════════

The companion module to geoglyph_cursive.py.
Implements the visual and audio feedback layers for the Penman's
Delian Resonance — the moment when the anticlockwise loop crosses
R ≈ 6.299 (5 × ∛2) and the Cube of Delos is doubled.

Architecture:
    Forearm (Cubit Platform) → Pen Tip (Origin)
    │
    ├── Golden Spiral Overlay (φ-spiral from elbow pivot)
    ├── Cube Doubling Animation (original + doubled, counter-rotating)
    ├── Cubit Arc Glow (modulated by sin(loop_count × π/13))
    ├── Manus Illumination (hexagonal "Mastered 6" halo)
    └── Audio Cue (432Hz chime, 800ms, exponential fade)

The 93-Node Correspondence:
    90 tentacles → peripheral sensing array
     3 hearts    → central power triad
     2 eyes + 1 mouth → perception-action pipeline
    13-tooth radula → 13-node compass

Usage:
    python3 delian_pulse_renderer.py

    Or import into geoglyph_cursive.py:
        from delian_pulse_renderer import DelianPulseRenderer
        renderer = DelianPulseRenderer(screen)
        renderer.update(penman_state)

Keys:
    1/2/3   — Slope: 10° Copperplate / 15° Italic / 30° Royal
    F       — Toggle Cubit Platform (forearm)
    A       — Toggle Cubit Arcs
    D       — Toggle Delos Ring
    S       — Toggle Log Spiral Pyramid
    R       — Reverse (Staff of the Demiurge)
    G       — Toggle Golden Spiral Overlay
    H       — Toggle Hexagonal Halo (Manus Illumination)
    C       — Toggle Counter-rotating Cubes
    SPACE   — Pause/Resume

═══════════════════════════════════════════════════════════════════════
"""

import math
import sys
import time
import struct
import wave
import tempfile
import os

try:
    import pygame
    import pygame.gfxdraw
except ImportError:
    print("═" * 60)
    print("  DELIAN PULSE RENDERER requires pygame")
    print("  Install: pip install pygame --break-system-packages")
    print("═" * 60)
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# CONSTANTS: The Sacred Numbers
# ═══════════════════════════════════════════════════════════════

DEG = math.pi / 180
PHI = (1 + math.sqrt(5)) / 2           # Golden Ratio ≈ 1.618
CBRT2 = 2 ** (1/3)                     # Cube root of 2 ≈ 1.2599
DELOS_RADIUS = 5 * CBRT2               # ≈ 6.299
DELOS_VOLUME = 250                     # 2 × 5³
CHIME_FREQ = 432                       # Hz — the "Mastered 6" frequency
CHIME_DURATION = 0.8                   # seconds
SAMPLE_RATE = 44100

# The 93-Node Manifold
TENTACLES = 90
HEARTS = 3
RADULA_TEETH = 13
HERO_TOTAL = TENTACLES + HEARTS        # 93

# Historical Slopes
SLOPES = {
    10: {"name": "Copperplate", "era": "18th Century", "state": "Manus (5)",
         "color": (74, 124, 89)},
    15: {"name": "Italic", "era": "15th Century", "state": "Cubit (6)",
         "color": (46, 107, 138)},
    30: {"name": "Royal", "era": "Writing Lines", "state": "Royal (7)",
         "color": (123, 45, 142)},
}

# Colors
VOID = (10, 10, 15)
VOID_REVERSE = (15, 5, 30)
GOLD = (201, 168, 76)
GOLD_DIM = (138, 109, 43)
DELOS_GOLD = (232, 197, 71)
PARCHMENT = (240, 230, 208)
MANUS_GREEN = (74, 124, 89)
CUBIT_BLUE = (46, 107, 138)
ROYAL_PURPLE = (123, 45, 142)
SQUID_INK = (22, 33, 62)


# ═══════════════════════════════════════════════════════════════
# AUDIO: The 432Hz Chime
# ═══════════════════════════════════════════════════════════════

def generate_chime_wav():
    """Generate a 432Hz chime with exponential fade as a temp WAV file."""
    n_samples = int(SAMPLE_RATE * CHIME_DURATION)
    samples = []

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Exponential decay envelope
        envelope = math.exp(-t * 4.0)
        # Fundamental 432Hz + harmonics
        signal = (
            0.6 * math.sin(2 * math.pi * CHIME_FREQ * t) +          # Fundamental
            0.2 * math.sin(2 * math.pi * CHIME_FREQ * 2 * t) +      # 2nd harmonic
            0.1 * math.sin(2 * math.pi * CHIME_FREQ * 3 * t) +      # 3rd harmonic
            0.05 * math.sin(2 * math.pi * CHIME_FREQ * PHI * t)      # φ-harmonic
        )
        sample = int(signal * envelope * 32767 * 0.5)
        sample = max(-32767, min(32767, sample))
        samples.append(sample)

    # Write to temp WAV
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    with wave.open(tmp.name, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack(f'<{len(samples)}h', *samples))
    return tmp.name


# ═══════════════════════════════════════════════════════════════
# GEOMETRY: Vectors, Projections, Transformations
# ═══════════════════════════════════════════════════════════════

def forearm_vector(phi_deg, theta_deg=3):
    """Cubit Platform vector in 3D."""
    p = phi_deg * DEG
    t = theta_deg * DEG
    return (
        math.cos(p) * math.cos(t),
        math.sin(p),
        math.cos(p) * math.sin(t)
    )


def project_3d(x3, y3, z3, cx, cy, scale, cam_angle=15):
    """Project 3D point to 2D screen coordinates."""
    ca = cam_angle * DEG
    yr = y3 * math.cos(ca) - z3 * math.sin(ca)
    zr = y3 * math.sin(ca) + z3 * math.cos(ca)
    perspective = 1 + zr * 0.02
    sx = cx + x3 * scale / perspective
    sy = cy - yr * scale / perspective
    return int(sx), int(sy), zr


def rotate_y(x, y, z, angle):
    """Rotate point around Y axis."""
    ca = math.cos(angle)
    sa = math.sin(angle)
    return (x * ca + z * sa, y, -x * sa + z * ca)


def rotate_x(x, y, z, angle):
    """Rotate point around X axis."""
    ca = math.cos(angle)
    sa = math.sin(angle)
    return (x, y * ca - z * sa, y * sa + z * ca)


# ═══════════════════════════════════════════════════════════════
# PENMAN STATE
# ═══════════════════════════════════════════════════════════════

class PenmanState:
    """Complete state of the Penman system."""

    def __init__(self):
        self.slope_angle = 10       # φ: degrees
        self.tilt_angle = 3         # θ: degrees (invariant Master Key)
        self.time = 0.0
        self.loop_count = 0.0
        self.current_radius = 5.0
        self.position = (0.0, 0.0, 0.0)
        self.trail = []
        self.max_trail = 1200

        # Display toggles
        self.show_forearm = True
        self.show_arcs = True
        self.show_delos = True
        self.show_spiral = False
        self.show_golden = True
        self.show_hexhalo = True
        self.show_cubes = True
        self.animate = True
        self.reverse = False

        # Delos state
        self.delos_active = False
        self.delos_pulse_time = 0.0
        self.delos_chime_cooldown = 0.0

    @property
    def forearm(self):
        return forearm_vector(self.slope_angle, self.tilt_angle)

    @property
    def volume(self):
        return self.current_radius ** 3

    @property
    def delos_proximity(self):
        """How close is the current radius to the Delian threshold."""
        return abs(self.current_radius - DELOS_RADIUS)


# ═══════════════════════════════════════════════════════════════
# DELIAN PULSE RENDERER
# ═══════════════════════════════════════════════════════════════

class DelianPulseRenderer:
    """
    The display engine for the Penman's Delian Resonance.

    Implements all visual + audio feedback layers:
    - Golden Spiral Overlay
    - Cube Doubling Animation
    - Cubit Arc Glow (13-modulated)
    - Manus Illumination (hexagonal halo)
    - 432Hz Chime
    """

    def __init__(self, screen):
        self.screen = screen
        self.w = screen.get_width()
        self.h = screen.get_height()
        self.cx = self.w // 2
        self.cy = self.h // 2
        self.scale = min(self.w, self.h) * 0.05

        # Load / generate chime
        self.chime_path = generate_chime_wav()
        try:
            pygame.mixer.init(frequency=SAMPLE_RATE)
            self.chime_sound = pygame.mixer.Sound(self.chime_path)
            self.chime_sound.set_volume(0.4)
            self.audio_enabled = True
        except Exception:
            self.audio_enabled = False

        # Surfaces for glow effects
        self.glow_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.halo_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

    def cleanup(self):
        """Remove temp audio file."""
        try:
            os.unlink(self.chime_path)
        except Exception:
            pass

    def project(self, x, y, z):
        return project_3d(x, y, z, self.cx, self.cy, self.scale)

    # ── Background ──
    def draw_void(self, reverse=False):
        bg = VOID_REVERSE if reverse else VOID
        self.screen.fill(bg)

        # Radial grid
        for i in range(12):
            angle = (i / 12) * math.pi * 2
            r = min(self.w, self.h) * 0.45
            ex = self.cx + int(r * math.cos(angle))
            ey = self.cy + int(r * math.sin(angle))
            pygame.draw.aaline(self.screen, (*GOLD, 8), (self.cx, self.cy), (ex, ey))

        # Concentric rings
        for r in range(1, 11):
            rad = int(r * self.scale)
            pygame.draw.circle(self.screen, (*GOLD, 8), (self.cx, self.cy), rad, 1)

    # ── Cubit Arcs (Manus/Cubit/Royal rings) ──
    def draw_cubit_arcs(self, state):
        arc_data = [
            (5, MANUS_GREEN, "MANUS (5)"),
            (6, CUBIT_BLUE, "CUBIT (6)"),
            (7, ROYAL_PURPLE, "ROYAL (7)"),
        ]
        for radius, color, label in arc_data:
            # Modulated glow: sin(loop_count × π/13)
            glow = 0.3 + 0.3 * abs(math.sin(state.loop_count * math.pi / RADULA_TEETH))
            alpha = int(glow * 255)
            rad = int(radius * self.scale)

            # Draw arc
            surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*color, alpha), (self.cx, self.cy), rad, 1)
            self.screen.blit(surf, (0, 0))

            # Label
            lx, ly, _ = self.project(radius + 0.3, 0.4, 0)
            font = pygame.font.SysFont('serif', 11)
            lbl = font.render(label, True, (*color, alpha))
            self.screen.blit(lbl, (lx, ly))

    # ── Delos Ring ──
    def draw_delos_ring(self, state):
        pulse = 0.5 + 0.5 * math.sin(state.time * 3)
        alpha = int((0.3 + 0.5 * pulse) * 255)
        width = int(2 + 2 * pulse)
        rad = int(DELOS_RADIUS * self.scale)

        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*DELOS_GOLD, alpha), (self.cx, self.cy), rad, width)

        # Inner glow ring
        if state.delos_active:
            glow_alpha = int(pulse * 80)
            pygame.draw.circle(surf, (*DELOS_GOLD, glow_alpha),
                               (self.cx, self.cy), rad + 4, 3)
            pygame.draw.circle(surf, (*DELOS_GOLD, glow_alpha // 2),
                               (self.cx, self.cy), rad + 8, 2)

        self.screen.blit(surf, (0, 0))

        # Label
        lx, ly, _ = self.project(DELOS_RADIUS + 0.4, -0.6, 0)
        font = pygame.font.SysFont('serif', 12)
        lbl = font.render(f"∛2·5 ≈ {DELOS_RADIUS:.3f}", True,
                          (*DELOS_GOLD, alpha))
        self.screen.blit(lbl, (lx, ly))

    # ── Cubit Platform (Forearm) ──
    def draw_forearm(self, state):
        fv = state.forearm
        arm_len = 6  # 1 cubit = 6 manus

        # Forearm endpoint (elbow)
        ex = -fv[0] * arm_len
        ey = -fv[1] * arm_len
        ez = -fv[2] * arm_len

        # Draw forearm line
        p1 = self.project(0, 0, 0)
        p2 = self.project(ex, ey, ez)
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.line(surf, (*GOLD, 160), (p1[0], p1[1]), (p2[0], p2[1]), 2)
        self.screen.blit(surf, (0, 0))

        # Elbow dot
        pygame.draw.circle(self.screen, GOLD, (p2[0], p2[1]), 5)

        # Pen tip dot (origin)
        pygame.draw.circle(self.screen, DELOS_GOLD, (p1[0], p1[1]), 3)

        # Equilateral triangle at midpoint
        mx = ex * 0.5
        my = ey * 0.5
        mz = ez * 0.5
        tri_size = 1.5
        for i in range(4):
            angle = state.time * 0.3 + (i / 3) * math.pi * 2
            tx = mx + tri_size * math.cos(angle)
            ty = my + tri_size * math.sin(angle)
            pt = self.project(tx, ty, mz)
            if i == 0:
                pts = [pt]
            else:
                pts.append(pt)
        if len(pts) >= 3:
            pygame.draw.polygon(self.screen, (*GOLD, 40),
                                [(p[0], p[1]) for p in pts[:3]], 1)

        # Platform label
        lx, ly, _ = self.project(mx, my - 1.2, mz)
        font = pygame.font.SysFont('serif', 10)
        lbl = font.render("CUBIT PLATFORM", True, (*GOLD, 100))
        self.screen.blit(lbl, (lx - 45, ly))

    # ── Golden Spiral Overlay (φ-spiral from elbow pivot) ──
    def draw_golden_spiral(self, state):
        """φ-spiral emanating from elbow, aligning with Cubit Arc path."""
        fv = state.forearm
        # Elbow position
        ox = -fv[0] * 6
        oy = -fv[1] * 6
        oz = -fv[2] * 6

        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        growth = math.log(PHI) / (math.pi / 2)  # 90° per golden expansion
        steps = 400
        max_angle = 6 * math.pi
        prev = None

        for i in range(steps + 1):
            angle = (i / steps) * max_angle
            r = 0.3 * math.exp(growth * angle)
            if r > 12:
                break
            x = ox + r * math.cos(-angle + state.time * 0.15)
            y = oy + r * math.sin(-angle + state.time * 0.15)
            z = oz + angle * 0.02

            px, py, _ = self.project(x, y, z)
            age = i / steps
            alpha = int(age * 80)

            if prev:
                pygame.draw.aaline(surf, (*GOLD, min(alpha, 80)),
                                   prev, (px, py))
            prev = (px, py)

        self.screen.blit(surf, (0, 0))

    # ── Cube Doubling Animation ──
    def draw_counter_cubes(self, state):
        """Original cube (s=5) and doubled cube (s≈6.299), counter-rotating."""
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        for cube_idx, (side, color, rot_dir) in enumerate([
            (2.5, MANUS_GREEN, 1),     # Original (scaled for display)
            (3.15, DELOS_GOLD, -1),     # Doubled (≈ 6.299/2 for display)
        ]):
            rot = state.time * 0.4 * rot_dir
            # 8 vertices of a cube centered at origin, offset for display
            offset_x = -4 if cube_idx == 0 else 4
            verts = []
            for dx in (-1, 1):
                for dy in (-1, 1):
                    for dz in (-1, 1):
                        x = dx * side * 0.5
                        y = dy * side * 0.5
                        z = dz * side * 0.5
                        # Rotate
                        x, y, z = rotate_y(x, y, z, rot)
                        x, y, z = rotate_x(x, y, z, rot * 0.3)
                        x += offset_x
                        y += 5  # Position above center
                        verts.append(self.project(x, y, z))

            # Draw edges
            edges = [
                (0,1),(0,2),(0,4),(1,3),(1,5),(2,3),
                (2,6),(3,7),(4,5),(4,6),(5,7),(6,7)
            ]
            alpha = 60 if cube_idx == 0 else int(40 + 30 * abs(math.sin(state.time)))
            for a, b in edges:
                pygame.draw.aaline(surf, (*color, alpha),
                                   (verts[a][0], verts[a][1]),
                                   (verts[b][0], verts[b][1]))

        # Labels
        font = pygame.font.SysFont('serif', 10)
        p1 = self.project(-4, 3.5, 0)
        p2 = self.project(4, 3.5, 0)
        l1 = font.render("V = 125", True, (*MANUS_GREEN, 120))
        l2 = font.render("V = 250", True, (*DELOS_GOLD, 120))
        surf.blit(l1, (p1[0] - 20, p1[1]))
        surf.blit(l2, (p2[0] - 20, p2[1]))

        self.screen.blit(surf, (0, 0))

    # ── Manus Illumination: Hexagonal Halo ──
    def draw_hex_halo(self, state):
        """Hexagonal 'Mastered 6' halo at the pen tip."""
        pulse = 0.5 + 0.5 * math.sin(state.time * 2.5)
        alpha = int(30 + 50 * pulse)
        size = 1.0 + 0.3 * pulse

        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pts = []
        for i in range(7):
            angle = (i / 6) * math.pi * 2 + state.time * 0.2
            x = size * math.cos(angle)
            y = size * math.sin(angle)
            px, py, _ = self.project(x, y, 0)
            pts.append((px, py))

        if len(pts) >= 6:
            pygame.draw.polygon(surf, (*GOLD, alpha), pts[:6], 1)
            # Inner hex
            inner_pts = []
            for i in range(7):
                angle = (i / 6) * math.pi * 2 + state.time * 0.2 + math.pi / 6
                x = size * 0.5 * math.cos(angle)
                y = size * 0.5 * math.sin(angle)
                px, py, _ = self.project(x, y, 0)
                inner_pts.append((px, py))
            pygame.draw.polygon(surf, (*GOLD, alpha // 2), inner_pts[:6], 1)

        self.screen.blit(surf, (0, 0))

    # ── Log Spiral Pyramid ──
    def draw_spiral_pyramid(self, state):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        gf = math.log(DELOS_RADIUS / 0.5) / (5 * math.pi)
        steps = 400
        prev = None

        for i in range(steps + 1):
            angle = (i / steps) * 8 * math.pi
            r = 0.5 * math.exp(gf * angle)
            if r > 10:
                break
            x = r * math.cos(-angle)
            y = r * math.sin(-angle)
            z = angle * 0.04
            px, py, _ = self.project(x, y, z)
            age = min(i / steps, 1.0)

            if prev:
                pygame.draw.aaline(surf, (*GOLD, int(age * 60)),
                                   prev, (px, py))
            prev = (px, py)

        # Pyramid edges
        for f in range(3):
            angle = (f / 3) * math.pi * 2 + state.time * 0.1
            bx = 5 * math.cos(angle)
            by = 5 * math.sin(angle)
            p1 = self.project(0, 0, 3)
            p2 = self.project(bx, by, 0)
            pygame.draw.aaline(surf, (*GOLD, 30),
                               (p1[0], p1[1]), (p2[0], p2[1]))

        self.screen.blit(surf, (0, 0))

    # ── Trail ──
    def draw_trail(self, state):
        if len(state.trail) < 2:
            return

        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        for i in range(1, len(state.trail)):
            pt = state.trail[i]
            prev = state.trail[i - 1]
            age = i / len(state.trail)

            r = math.sqrt(pt[0]**2 + pt[1]**2 + pt[2]**2)

            if r < 5.5:
                color = MANUS_GREEN
            elif r < 6.15:
                color = CUBIT_BLUE
            elif abs(r - DELOS_RADIUS) < 0.2:
                color = DELOS_GOLD
            else:
                color = ROYAL_PURPLE

            alpha = int(age * 200)
            p1 = self.project(prev[0], prev[1], prev[2])
            p2 = self.project(pt[0], pt[1], pt[2])
            width = max(1, int(1 + age * 2))

            pygame.draw.line(surf, (*color, alpha),
                             (p1[0], p1[1]), (p2[0], p2[1]), width)

        self.screen.blit(surf, (0, 0))

        # Pen tip glow
        if state.trail:
            tip = state.trail[-1]
            px, py, _ = self.project(tip[0], tip[1], tip[2])
            r = math.sqrt(tip[0]**2 + tip[1]**2 + tip[2]**2)
            is_delos = abs(r - DELOS_RADIUS) < 0.3
            glow_color = DELOS_GOLD if is_delos else PARCHMENT
            glow_size = 15 if is_delos else 8
            glow_surf = pygame.Surface((glow_size*4, glow_size*4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*glow_color, 60),
                               (glow_size*2, glow_size*2), glow_size)
            pygame.draw.circle(glow_surf, (*glow_color, 120),
                               (glow_size*2, glow_size*2), glow_size // 2)
            self.screen.blit(glow_surf,
                             (px - glow_size*2, py - glow_size*2))

    # ── Audio: 432Hz Chime ──
    def trigger_chime(self, state):
        """Play the 432Hz chime when Delos resonance is hit."""
        if (self.audio_enabled and
            state.delos_active and
            state.delos_chime_cooldown <= 0):
            self.chime_sound.play()
            state.delos_chime_cooldown = 3.0  # Cooldown in seconds

    # ── HUD ──
    def draw_hud(self, state):
        font = pygame.font.SysFont('serif', 12)
        bold_font = pygame.font.SysFont('serif', 14, bold=True)
        title_font = pygame.font.SysFont('serif', 22, bold=True)
        small_font = pygame.font.SysFont('serif', 10)

        # Title
        title = title_font.render("PENMAN GEOGLYPH", True, GOLD)
        self.screen.blit(title, (24, 20))
        sub = font.render("The Cubit Platform & Delian Resonance", True,
                          (*PARCHMENT, 120))
        self.screen.blit(sub, (26, 46))

        # Info panel (right side)
        slope_info = SLOPES.get(state.slope_angle, SLOPES[10])
        fv = state.forearm

        info_lines = [
            (f"Slope (φ)", f"{state.slope_angle}° {slope_info['name']}"),
            ("Tilt (θ)", f"{state.tilt_angle}° (Master Key)"),
            ("Radius", f"{state.current_radius:.3f}"),
            ("Volume", f"{state.volume:.1f}"),
            ("Forearm", f"[{fv[0]:.3f}, {fv[1]:.3f}, {fv[2]:.3f}]"),
            ("Delos Target", f"{DELOS_RADIUS:.3f}"),
            ("Loops", f"{state.loop_count:.1f}"),
            ("13-Mod Glow",
             f"{abs(math.sin(state.loop_count * math.pi / 13)):.3f}"),
        ]

        y = 24
        for key, val in info_lines:
            ksurf = small_font.render(key, True, (*PARCHMENT, 80))
            vsurf = font.render(val, True, GOLD)
            kw = ksurf.get_width()
            vw = vsurf.get_width()
            self.screen.blit(ksurf, (self.w - 24 - kw - vw - 12, y))
            self.screen.blit(vsurf, (self.w - 24 - vw, y))
            y += 20

        # Delos indicator
        if state.delos_active:
            pulse = 0.7 + 0.3 * math.sin(state.time * 4)
            alpha = int(pulse * 255)
            delos_title = bold_font.render("DELIAN RESONANCE", True,
                                           (*DELOS_GOLD, alpha))
            delos_val = title_font.render(f"∛2 · 5 ≈ {DELOS_RADIUS:.3f}",
                                          True, (*DELOS_GOLD, alpha))
            tw = delos_title.get_width()
            vw = delos_val.get_width()
            self.screen.blit(delos_title,
                             (self.w - 32 - tw, self.h - 70))
            self.screen.blit(delos_val,
                             (self.w - 32 - vw, self.h - 48))

        # Keyboard hints
        hints = "1/2/3:Slopes  F:Forearm  A:Arcs  D:Delos  S:Spiral  " \
                "G:Golden  H:Halo  C:Cubes  R:Reverse  SPACE:Pause"
        hsurf = small_font.render(hints, True, (*PARCHMENT, 60))
        hw = hsurf.get_width()
        self.screen.blit(hsurf, ((self.w - hw) // 2, self.h - 24))

    # ── Master Update ──
    def update(self, state, dt):
        """Full render pass."""
        # Background
        self.draw_void(state.reverse)

        # Layers (back to front)
        if state.show_spiral:
            self.draw_spiral_pyramid(state)
        if state.show_golden:
            self.draw_golden_spiral(state)
        if state.show_arcs:
            self.draw_cubit_arcs(state)
        if state.show_delos:
            self.draw_delos_ring(state)
        if state.show_cubes:
            self.draw_counter_cubes(state)
        if state.show_forearm:
            self.draw_forearm(state)
        if state.show_hexhalo:
            self.draw_hex_halo(state)

        # Trail (always)
        self.draw_trail(state)

        # HUD
        self.draw_hud(state)

        # Audio
        self.trigger_chime(state)

        # Cooldown
        if state.delos_chime_cooldown > 0:
            state.delos_chime_cooldown -= dt


# ═══════════════════════════════════════════════════════════════
# MAIN: Standalone Execution
# ═══════════════════════════════════════════════════════════════

def anticlockwise_loop_point(t, radius, phi_deg, theta_deg, z_offset):
    """Generate a point on the anticlockwise loop with Neusis precession."""
    th = theta_deg * DEG
    p = phi_deg * DEG

    # Anticlockwise in XY
    x = radius * math.cos(-t)
    y = radius * math.sin(-t)
    z = z_offset

    # 3° tilt (Neusis precession)
    xr = x * math.cos(th) - z * math.sin(th)
    zr = x * math.sin(th) + z * math.cos(th)

    # Slope rotation
    yr2 = y * math.cos(p * 0.1) - zr * math.sin(p * 0.1)
    zr2 = y * math.sin(p * 0.1) + zr * math.cos(p * 0.1)

    return (xr, yr2, zr2)


def main():
    pygame.init()

    # Fullscreen or windowed
    info = pygame.display.Info()
    w, h = min(info.current_w, 1400), min(info.current_h, 900)
    screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    pygame.display.set_caption("Penman Geoglyph — Delian Pulse Renderer")

    clock = pygame.time.Clock()
    state = PenmanState()
    renderer = DelianPulseRenderer(screen)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    state.slope_angle = 10
                    state.trail.clear()
                elif event.key == pygame.K_2:
                    state.slope_angle = 15
                    state.trail.clear()
                elif event.key == pygame.K_3:
                    state.slope_angle = 30
                    state.trail.clear()
                elif event.key == pygame.K_f:
                    state.show_forearm = not state.show_forearm
                elif event.key == pygame.K_a:
                    state.show_arcs = not state.show_arcs
                elif event.key == pygame.K_d:
                    state.show_delos = not state.show_delos
                elif event.key == pygame.K_s:
                    state.show_spiral = not state.show_spiral
                elif event.key == pygame.K_g:
                    state.show_golden = not state.show_golden
                elif event.key == pygame.K_h:
                    state.show_hexhalo = not state.show_hexhalo
                elif event.key == pygame.K_c:
                    state.show_cubes = not state.show_cubes
                elif event.key == pygame.K_r:
                    state.reverse = not state.reverse
                elif event.key == pygame.K_SPACE:
                    state.animate = not state.animate
            elif event.type == pygame.VIDEORESIZE:
                w, h = event.w, event.h
                screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                renderer = DelianPulseRenderer(screen)

        # ── Physics Update ──
        if state.animate:
            direction = -1 if state.reverse else 1
            state.time += dt * direction

            # Target radius from slope
            target_r = {10: 5.0, 15: 6.0, 30: 7.0}.get(state.slope_angle, 5.0)
            state.current_radius += (target_r - state.current_radius) * dt * 2

            # Loop generation
            loop_speed = 1.2
            t = state.time * loop_speed
            z_off = state.loop_count * math.sin(state.tilt_angle * DEG) * \
                    state.current_radius * 0.1

            dynamic_r = 5 + (state.current_radius - 5) * \
                        (0.5 + 0.5 * math.sin(t * 0.3))

            pt = anticlockwise_loop_point(
                t, dynamic_r, state.slope_angle, state.tilt_angle, z_off
            )
            state.position = pt
            state.trail.append(pt)
            if len(state.trail) > state.max_trail:
                state.trail.pop(0)

            state.loop_count = abs(state.time * loop_speed) / (math.pi * 2)

            # Delos check
            current_r = math.sqrt(pt[0]**2 + pt[1]**2 + pt[2]**2)
            state.delos_active = (
                abs(current_r - DELOS_RADIUS) < 0.3 and
                state.show_delos
            )

        # ── Render ──
        renderer.update(state, dt)
        pygame.display.flip()

    renderer.cleanup()
    pygame.quit()


if __name__ == "__main__":
    print("═" * 60)
    print("  DELIAN PULSE RENDERER")
    print("  The Penman Geoglyph Engine")
    print(f"  Delos Target: 5 × ∛2 = {DELOS_RADIUS:.6f}")
    print(f"  Volume: {DELOS_VOLUME}")
    print(f"  93-Node Manifold: {TENTACLES} tentacles + {HEARTS} hearts")
    print("═" * 60)
    main()
