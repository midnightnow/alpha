import asyncio
import json
import numpy as np
import yaml
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os

# Import the Primordial Solvers
from hydrodynamic_solver import HydrodynamicSolver1D
from species_automata import SpeciesAutomata
from anatomy_relative_matrix import PivotRelativeAnatomy

app = FastAPI()

# Allow connections from any origin (Dev only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SovereignEngine:
    """
    The High-Fidelity 93-Faced Interference Solid Orchestrator.
    Executes the Gastrulation of the Platonic Man: Blastula -> Tube -> Möbius Cord.
    """
    def __init__(self):
        # Vitrified Constants
        self.pivot = np.sqrt(42)
        self.boundary = np.sqrt(51)
        self.target_time = 8975
        self.packing_rho = 0.907485
        self.hex_limit = np.pi / np.sqrt(12)
        self.overpack_delta = self.packing_rho - self.hex_limit
        
        # Initialize Solvers
        self.hydro = HydrodynamicSolver1D()
        self.species = SpeciesAutomata()
        self.anatomy = PivotRelativeAnatomy()
        
        self.frame = 0

    def step(self):
        """Executes one frame of the 777-million iteration spin."""
        # 1. Physics: Laminar Flow & Bubble Drift
        # Steady state at 0.063 stroke width
        hydro_state = self.hydro.calculate_steady_state(0.063)
        
        # 2. Logic: 10-24-26 Species Automata
        self.species.step(1)
        entropy = self.species.calculate_entropy()
        
        # 3. Geometry: Möbius Torsion & Shear
        # The Torsion wrap (540 degrees)
        torsion = (self.frame * 0.5) % 540 # Slow roll
        
        # Drift consumes itself as coherence increases (Recursive Resonance)
        coherence = min(self.frame / 8975, 1.0)
        drift = 0.00039 * (1 - coherence) * abs(np.random.normal(1, 0.1))
        
        is_locked = drift <= 0.00039 and hydro_state['Re'] < 2300
        
        metrics = {
            "pivot": float(self.pivot),
            "shellBoundary": float(self.boundary),
            "fillTime": self.target_time,
            "currentEntropy": float(entropy),
            "maxRadialDrift": float(drift),
            "isPhaseLocked": bool(is_locked),
            "torsion": float(torsion),
            "shearAngle": 39.4, # arctan(14/17)
            "overpackDelta": float(self.overpack_delta * (1 + 0.1 * np.sin(self.frame * 0.1))),
            "reynoldsNumber": float(hydro_state['Re']),
            "flowState": hydro_state['state'],
            "archiveHash": "ROOT42-PHASE-II-FINAL"
        }
        
        self.frame += 1
        return metrics

engine = SovereignEngine()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[SOVEREIGN] Visualizer connected to High-Fidelity Bridge.")
    try:
        while True:
            metrics = engine.step()
            await websocket.send_text(json.dumps(metrics))
            await asyncio.sleep(0.033) # 30 FPS for smooth gastrulation
    except Exception as e:
        print(f"[SOVEREIGN] Connection Terminated: {e}")

@app.get("/data/05_anatomy_relative.csv")
async def serve_anatomy():
    csv_path = "/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine/05_anatomy_relative.csv"
    if os.path.exists(csv_path):
        return FileResponse(csv_path, media_type="text/csv")
    return {"error": "Anatomy matrix not found. Run 05_anatomy_relative_matrix.py first."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8975)
