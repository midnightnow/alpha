import requests
import json
import logging

class AlexandriaBridge:
    def __init__(self, api_url="http://localhost:8080"):
        self.api_url = api_url
        self.timeout = 5

    def check_health(self):
        """Verify Alexandria is reachable."""
        try:
            response = requests.get(f"{self.api_url}/healthz", timeout=self.timeout)
            return response.status_code == 200
        except Exception:
            return False

    def query_knowledge(self, topic):
        """Fetch related research context from Alexandria."""
        # Note: In the 'simple' version, this might use the /validate endpoint
        # or a search endpoint if available.
        try:
            payload = {
                "prompt": f"Research context for: {topic}",
                "category": "INFORMATION",
                "context": {"source": "paperbee"}
            }
            response = requests.post(f"{self.api_url}/validate", json=payload, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                # Use the 'output' or 'evidence' as context
                return data.get("output") or "No further clinical context found in Alexandria."
        except Exception as e:
            logging.error(f"Alexandria Query Error: {e}")
        return None

    def store_research_asset(self, manifest):
        """Persist a distilled manifest to Alexandria as a new entry."""
        # This would ideally hit a /works or /entries endpoint
        # For now, we simulate storage or hit a log/audit endpoint
        try:
            print(f"[*] Storing '{manifest['research_title']}' in Alexandria Library...")
            # Placeholder for actual persistence logic
            return True
        except Exception as e:
            logging.error(f"Alexandria Storage Error: {e}")
            return False

if __name__ == "__main__":
    bridge = AlexandriaBridge()
    print(f"Alexandria Status: {'Online' if bridge.check_health() else 'Offline'}")
