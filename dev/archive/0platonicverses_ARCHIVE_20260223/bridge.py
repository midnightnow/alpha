"""
FastAPI WebSocket Bridge — The Oracle Grid Interface
Part of Phase III: The Sentient Sieve

Bridges the Three.js viewport with the Python Ophanim Toolkit.
Handles coordinate projection, H3 residency, and the Naming Ceremony.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ophanim_toolkit.addresser import OracleAddresser
from ophanim_toolkit.perception import StandingManObserver
from ophanim_toolkit.actualizer import Actualizer
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Bridge")

app = FastAPI(title="Ophanim Oracle Bridge")
addresser = OracleAddresser(resolution=9)
observer = StandingManObserver(addresser)
actualizer = Actualizer()

@app.get("/")
async def root():
    return {"status": "ACTIVE", "phase": "III", "module": "Oracle Bridge"}

@app.websocket("/ws/grid")
async def grid_socket(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established.")
    
    try:
        while True:
            # Receive data from the Three.js frontend
            # Expected format: {"x": float, "y": float, "lat": float, "lng": float}
            data_str = await websocket.receive_text()
            data = json.loads(data_str)
            
            x, y = data.get('x', 0), data.get('y', 0)
            lat, lng = data.get('lat', 0), data.get('lng', 0)
            
            # Calculate H3 Residency
            h3_idx = addresser.project_to_grid(x, y, lat, lng)
            
            # Perform the Naming Ceremony (Lexical Retrieval)
            stone_name = addresser.get_stone_name(h3_idx)
            is_hades = addresser.check_hades_gap(h3_idx)
            
            # --- PHASE IV: PERCEPTION & ACTUALIZATION ---
            # 1. Perception Loop
            perception = observer.scan_neighborhood(h3_idx, []) # Mock local field for now
            # Recalculate salience based on Hades alignment (entropy)
            perception['salience_score'] = observer.calculate_salience(0.66, 0.1237 if is_hades else 0.9074)
            perception['resonance_state'] = "FRACTURE_WITNESSED" if not is_hades else "CHORUS_EMERGENT"

            # 2. Actualization Loop (Distill Intent)
            intent_packet = actualizer.distill_intent(perception)
            
            # Construct the Phonetic Packet
            response = {
                "address": h3_idx,
                "name": stone_name,
                "composition": addresser.h3_to_phonemes(int(h3_idx, 16)),
                "carrier": "66Hz",
                "is_hades_gap": is_hades,
                "harmonic_bias": 0.1237 if is_hades else 0.9074,
                # Phase IV Data
                "salience": float(perception['salience_score']),
                "intent": intent_packet['action'],
                "actualization_intensity": float(intent_packet['intensity']),
                "shear_correction": float(intent_packet['vector_shift'])
            }
            
            # Send the packet back to the HUD
            await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed.")
    except Exception as e:
        logger.error(f"Bridge Error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
