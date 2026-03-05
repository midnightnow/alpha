import subprocess
import os
import time

def run():
    # 1. Start HTTP Server for Data/Assets on 8975
    # Since WebSocket server also wants 8975, we'll have to use different ports or integrated server.
    # SoftCreature.tsx uses: fetch('http://127.0.0.1:8975/data/05_anatomy_relative.csv')
    # So we need HTTP on 8975.

    # 2. Wait, websocket_orchestrator.py uses ws://localhost:8975
    # On most systems, you can't have both HTTP and WS on same port unless handled by same process.
    
    print("[SERVER] Orchestrating Sovereign Engine...")
    
    # We'll use a single script that handles both if possible, or use a Proxy.
    # But for simplicity, let's just use two distinct ports and update the visualizer if needed.
    # BUT the user wants the release 'vitrified'. 
    
    # Let's modify websocket_orchestrator.py to also serve static files.
    pass

if __name__ == "__main__":
    # For now, let's just run the websocket server on 8975.
    # And we'll run a static server for the CSV.
    # We'll change the CSV fetch URL in SoftCreature.tsx to 8976 if necessary.
    
    # Actually, let's just run them:
    # Term 1: Websocket (8975)
    # Term 2: HTTP (8976)
    
    os.chdir('/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine')
    subprocess.Popen(['python3', 'websocket_orchestrator.py'])
    
    # Simple HTTP server on 8976
    import http.server
    import socketserver

    PORT = 8976
    Handler = http.server.SimpleHTTPRequestHandler
    
    # We need to serve the 'data' directory.
    # SoftCreature.tsx looks for /data/05_anatomy_relative.csv
    # So we create a 'data' symlink or move it.
    os.makedirs('data', exist_ok=True)
    import shutil
    shutil.copy('05_anatomy_relative.csv', 'data/05_anatomy_relative.csv')

    print(f"[HTTP] Serving data at http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

