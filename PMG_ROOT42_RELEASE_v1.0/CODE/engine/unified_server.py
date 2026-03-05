import asyncio
import json
from aiohttp import web
import numpy as np
import yaml
import os

# ============================================================================
# SOVEREIGN ENGINE: UNIFIED SERVER (WS + HTTP)
# ============================================================================

class SimulationOrchestrator:
    def __init__(self):
        with open('config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
            
        self.pivot = self.config.get('pivot_constant', np.sqrt(42))
        self.boundary = self.config.get('boundary_constant', np.sqrt(51))
        self.fill_time = self.config.get('target_convergence_time', 8975)
        self.base_entropy = 5.557269
        self.target_drift = 0.00039

    async def generate_metrics(self):
        frame = 0
        while True:
            packing_rho = 0.907485
            hex_limit = np.pi / np.sqrt(12)
            overpack_delta = packing_rho - hex_limit
            
            torsion_angle = (frame % 540)
            noise = np.random.uniform(-0.0001, 0.0002)
            current_drift = abs(noise) * (1 - (frame / 8975))
            current_entropy = self.base_entropy + (np.sin(frame * 0.1237) * overpack_delta)
            is_locked = current_drift <= self.target_drift
            
            payload = {
                "pivot": float(self.pivot),
                "shellBoundary": float(self.boundary),
                "fillTime": int(self.fill_time),
                "currentEntropy": float(current_entropy),
                "maxRadialDrift": float(current_drift),
                "isPhaseLocked": bool(is_locked),
                "torsion": float(torsion_angle),
                "shearAngle": 39.4,
                "overpackDelta": float(overpack_delta),
                "archiveHash": "ROOT42-PHASE-II-FINAL"
            }
            
            yield json.dumps(payload)
            frame += 1
            await asyncio.sleep(0.1)

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    print("[WS] Connection established.")
    orchestrator = SimulationOrchestrator()
    
    try:
        async for metrics_json in orchestrator.generate_metrics():
            await ws.send_str(metrics_json)
    except Exception as e:
        print(f"[WS] Connection closed: {e}")
    finally:
        return ws

# Setup Application
app = web.Application()
app.router.add_get('/ws', websocket_handler)

# Serve Static Data (05_anatomy_relative.csv)
# SoftCreature.tsx uses: fetch('http://127.0.0.1:8975/data/05_anatomy_relative.csv')
# We map '/data' to the local directory
os.makedirs('data', exist_ok=True)
import shutil
shutil.copy('05_anatomy_relative.csv', 'data/05_anatomy_relative.csv')
app.router.add_static('/data', 'data')

if __name__ == '__main__':
    print("="*60)
    print("SOVEREIGN ENGINE: UNIFIED PIVOT SERVER (PORT 8975)")
    print("="*60)
    web.run_app(app, host='0.0.0.0', port=8975)
