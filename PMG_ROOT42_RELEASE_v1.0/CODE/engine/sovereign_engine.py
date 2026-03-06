import asyncio
import json
import time
import random
import websockets

async def handler(websocket, path):
    print("Sovereign Engine: Client Connected")
    start_time = time.time()
    
    # 8975 / 10242 = 87.63% (Active Fill)
    TOTAL_CYCLE = 10242
    ACTIVE_FILL = 8975
    
    try:
        while True:
            elapsed = time.time() - start_time
            # Simulate a 10,242-second cycle in 102 seconds for testing
            progress = (elapsed * 10) % TOTAL_CYCLE
            
            is_active = progress < ACTIVE_FILL
            
            metrics = {
                "pivot": 6.48074,
                "shellBoundary": 7.14142,
                "fillTime": ACTIVE_FILL,
                "currentEntropy": random.uniform(0.1, 0.4) if is_active else 0.8975,
                "maxRadialDrift": random.uniform(0.0001, 0.0003) if is_active else 0.042,
                "isPhaseLocked": is_active,
                "torsion": (progress * 360 / TOTAL_CYCLE),
                "overpackDelta": 0.05 if is_active else 0.0,
                "cycleProgress": round(progress, 2)
            }
            
            await websocket.send(json.dumps(metrics))
            await asyncio.sleep(0.1)
            
            if not is_active:
                print("HADES GAP DETECTED: PRUNING...")
                
    except websockets.exceptions.ConnectionClosed:
        print("Sovereign Engine: Client Disconnected")

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8975):
        print("PRINCIPIA MATHEMATICA GEOMETRICA v1.0")
        print("ENGINE LIVE at ws://127.0.0.1:8975")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
