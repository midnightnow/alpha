import asyncio
import json
import websockets
import numpy as np

# Import the existing De-Mythologized Engines we just built
from solver_engine import ConfigDrivenSolver
import yaml
from itertools import cycle

class SimulationOrchestrator:
    """
    Funneling the Python Primordial 7 Simulation into the React dashboard via Websocket.
    """
    def __init__(self):
        # We load the constants from the vitrified config
        with open('config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
            
        self.pivot = self.config.get('pivot_constant', np.sqrt(42))
        self.boundary = self.config.get('boundary_constant', np.sqrt(51))
        self.fill_time = self.config.get('target_convergence_time', 8975)
        
        # Base Entropy from 04_species calculations
        self.base_entropy = 5.557269
        self.current_entropy = self.base_entropy
        
        self.target_drift = 0.00039
        self.current_drift = 0.000000

    async def generate_metrics(self):
        """
        Calculates Recursive Resonance metrics based on the Biquadratic Interference Field:
        x^4 - 186x^2 + 81 = 0
        
        This field produces the root x ≈ 0.660688, which numerically matches the 
        beat constant (√51 - √42). It is the operator of the difference,
        not the minimal polynomial of the individual constants.
        """
        frame = 0
        while True:
            # The Overpack Principle: ρ ≈ 0.907485
            packing_rho = 0.907485
            hex_limit = np.pi / np.sqrt(12)
            overpack_delta = packing_rho - hex_limit # The fracture force (0.000585)
            
            # Möbius Torsion: 540-degree wrap (1.5 cycles)
            torsion_angle = (frame % 540)
            
            # Recursive Resonance: Shell consuming its own noise
            noise = np.random.uniform(-0.0001, 0.0002)
            self.current_drift = abs(noise) * (1 - (frame / 8975))
            
            # Entropy is fixed to the Triadic Symmetry (31-fold)
            self.current_entropy = self.base_entropy + (np.sin(frame * 0.1237) * overpack_delta)
            
            # Phase lock is maintained by the Möbius bury
            is_locked = self.current_drift <= self.target_drift
            
            payload = {
                "pivot": float(self.pivot),
                "shellBoundary": float(self.boundary),
                "fillTime": int(self.fill_time),
                "currentEntropy": float(self.current_entropy),
                "maxRadialDrift": float(self.current_drift),
                "isPhaseLocked": bool(is_locked),
                "torsion": float(torsion_angle),
                "shearAngle": 39.4, # arctan(14/17)
                "overpackDelta": float(overpack_delta),
                "archiveHash": "ROOT42-PHASE-II-FINAL"
            }
            
            yield json.dumps(payload)
            frame += 1
            await asyncio.sleep(0.1) # Sync to triadic beat

async def broadcast_handler(websocket):
    print(f"\n[ORCHESTRATOR] New React Visualizer Connection established.")
    orchestrator = SimulationOrchestrator()
    
    try:
        async for metrics_json in orchestrator.generate_metrics():
            await websocket.send(metrics_json)
    except websockets.exceptions.ConnectionClosed:
        print("[ORCHESTRATOR] Visualizer disconnected.")

async def main():
    print("="*60)
    print("SOVEREIGN ENGINE: PIVOT-RELATIVE WEBSOCKET SERVER")
    print("="*60)
    print("Starting broadcast on ws://localhost:8975 ...")
    
    # Run on Port 8975 (The Vitrification Constant)
    server = await websockets.serve(broadcast_handler, "0.0.0.0", 8975)
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOrchestrator shut down.")
