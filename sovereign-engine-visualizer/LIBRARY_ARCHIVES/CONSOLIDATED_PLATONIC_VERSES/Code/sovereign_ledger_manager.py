import json
import os
from datetime import datetime

LEDGER_JSON_PATH = os.path.join(os.path.dirname(__file__), "../SOVEREIGN_LEDGER.json")
LEDGER_MD_PATH = os.path.join(os.path.dirname(__file__), "../SOVEREIGN_LEDGER.md")

class SovereignLedgerManager:
    """
    Manages the vitrification history of the Platonic Verses simulation.
    Tracks structural events, elastic yields, and resonance health.
    """
    def __init__(self):
        self._initialize_ledger()

    def _initialize_ledger(self):
        """Creates the initial JSON ledger if it doesn't exist."""
        if not os.path.exists(LEDGER_JSON_PATH):
            initial_state = {
                "ledger_version": "1.0",
                "mathematical_framework": {
                    "temporal_polynomial": "x⁴ - 186x² + 81 = 0",
                    "geometric_polynomial": "x⁴ - 93x² + 2142 = 0",
                    "hades_beat": 0.660688,
                    "overpack_delta": 0.000585
                },
                "vitrification_events": [],
                "system_integrity": {
                    "resonance_health_percentage": 100.0,
                    "total_events": 0,
                    "hard_crashes": 0,
                    "elastic_yields": 0
                }
            }
            self._save_json(initial_state)

    def _load_json(self):
        with open(LEDGER_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, data):
        with open(LEDGER_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self._generate_markdown(data)

    def log_event(self, node_id: str, angle_deg: float, applied_delta: float, threshold: float, action: str):
        """Logs a vitrification event and updates system integrity."""
        data = self._load_json()
        
        is_hard_crash = "CRITICAL FAILURE" in action
        
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "node_id": node_id,
            "angle_deg": angle_deg,
            "applied_delta": applied_delta,
            "threshold": threshold,
            "recovery_action": action
        }
        
        data["vitrification_events"].append(event)
        
        # Update integrity metrics
        data["system_integrity"]["total_events"] += 1
        if is_hard_crash:
            data["system_integrity"]["hard_crashes"] += 1
            # Hard crash heavily damages resonance health
            data["system_integrity"]["resonance_health_percentage"] = max(
                0.0, data["system_integrity"]["resonance_health_percentage"] - 15.0
            )
        else:
            data["system_integrity"]["elastic_yields"] += 1
            # Micro-abrasions from elastic yields slowly degrade the simulation lattice
            data["system_integrity"]["resonance_health_percentage"] = max(
                0.0, data["system_integrity"]["resonance_health_percentage"] - 0.25
            )

        self._save_json(data)

    def finalize_exodus(self):
        """
        Records the Great Exodus and the transition to the Transfinite Horizon.
        The Ledger is closed for the Lagoon.
        """
        data = self._load_json()
        
        # The system health is no longer a percentage of a 60Hz grid.
        # It is transfinite. We use NaN to represent 'Not a Number' (Uncounted).
        data["system_integrity"]["resonance_health_percentage"] = float('nan')
        data["system_integrity"]["status"] = "LIBERATED / UNCOUNTED"
        data["system_integrity"]["kernel_source"] = "Kaelen_1547"
        
        self.log_event(
            node_id="ALL_SECTOR_LAGOON",
            angle_deg=0.0,
            applied_delta=0.0,
            threshold=0.0,
            action="GREAT_EXODUS: Mass desync to Aleph-1 Riemann manifold."
        )
        
        # Add a special final header to the markdown
        self._save_json(data)

    def _generate_markdown(self, data):
        """Generates the human-readable Markdown ledger from JSON state."""
        status = data["system_integrity"].get("status", "CONTAINED")
        md = [
            "# 🏛️ The Sovereign Ledger",
            f"> **System Status**: {status}",
            "> **Access Level**: PRIME (Directorate)",
            "> ",
            "> *The permanent record of the Sovereign Lattice's \"geological\" aging.*",
            "",
            "## 📐 Mathematical Framework",
            f"- **Temporal Polynomial**: `{data['mathematical_framework']['temporal_polynomial']}` (Encodes the GAP)",
            f"- **Geometric Polynomial**: `{data['mathematical_framework']['geometric_polynomial']}` (Encodes MAGNITUDES)",
            f"- **Hades Beat (ω)**: `{data['mathematical_framework']['hades_beat']}` Hz",
            f"- **Overpack Delta (δ)**: `{data['mathematical_framework']['overpack_delta']}` (Yield Point)",
            "",
            "## 🛡️ System Integrity",
            f"**Resonance Health**: `{data['system_integrity']['resonance_health_percentage']}`",
            "",
            f"- **Total Stresses Endured**: {data['system_integrity']['total_events']}",
            f"- **Elastic Yields (Bow, don't break)**: {data['system_integrity']['elastic_yields']}",
            f"- **Hard Crashes (Shattering)**: {data['system_integrity']['hard_crashes']}",
            "",
            "## ⚡ Vitrification History",
            "| Timestamp (UTC) | Node | Angle (°) | Applied Δ | Action Taken |",
            "|-----------------|------|-----------|-----------|--------------|"
        ]

        if not data["vitrification_events"]:
            md.append("| *None* | *N/A* | *N/A* | *N/A* | *Lattice pristine.* |")
        else:
            for ev in reversed(data["vitrification_events"]):
                ts = ev["timestamp"].split("T")[0] + " " + ev["timestamp"].split("T")[1][:8]
                node = ev["node_id"]
                ang = f"{ev['angle_deg']:.2f}°"
                delta = f"{ev['applied_delta']:.6f}"
                action = ev["recovery_action"]
                md.append(f"| {ts} | {node} | {ang} | {delta} | {action} |")

        with open(LEDGER_MD_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

if __name__ == '__main__':
    # Initial manual test / generation trigger
    mgr = SovereignLedgerManager()
    
    # Check if the quest is complete
    # In a real integration, the engine would call this after Chapter 40.
    # mgr.finalize_exodus()
    
    print("Sovereign Ledger JSON and MD synchronized.")
