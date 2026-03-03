import json
import os
from datetime import datetime

# Define absolute paths
CODE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(CODE_DIR, "SOVEREIGN_LEDGER.json")
DOCS_DIR = os.path.join(os.path.dirname(CODE_DIR), "Docs")
MD_PATH = os.path.join(DOCS_DIR, "SOVEREIGN_LEDGER.md")

class LedgerWriter:
    """
    Writes and manages vitrification events to the SOVEREIGN_LEDGER.
    Automatically syncs between the canonical JSON and human-readable Markdown.
    """
    
    def __init__(self):
        # Ensure the Docs directory exists
        os.makedirs(DOCS_DIR, exist_ok=True)
        self._ensure_json_exists()

    def _ensure_json_exists(self):
        """Creates the initial JSON ledger if it missing."""
        if not os.path.exists(JSON_PATH):
            initial_schema = {
                "ledger_version": "1.0",
                "mathematical_framework": {
                    "temporal_polynomial": "x⁴ - 186x² + 81 = 0",
                    "geometric_polynomial": "x⁴ - 93x² + 2142 = 0",
                    "hades_beat": 0.660688,
                    "overpack_delta": 0.000585
                },
                "vitrification_events": [],
                "system_integrity": {
                    "total_events": 0,
                    "hard_crashes": 0,
                    "elastic_yields": 0,
                    "resonance_health": 100.0
                }
            }
            self._write_json(initial_schema)

    def _read_json(self):
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_json(self, data):
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self._generate_markdown()

    def log_event(self, node_id: str, angle_deg: float, applied_delta: float, threshold: float, action: str):
        """Logs a new vitrification scar and computes resonance damage."""
        data = self._read_json()
        
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "node_id": node_id,
            "angle_deg": round(angle_deg, 6),
            "applied_delta": applied_delta,
            "threshold": threshold,
            "recovery_action": action
        }
        
        data["vitrification_events"].append(event)
        
        # Update system integrity metrics
        data["system_integrity"]["total_events"] += 1
        
        is_hard_crash = "CRITICAL" in action.upper() or "SHATTER" in action.upper() or "FAILURE" in action.upper()
        
        if is_hard_crash:
            data["system_integrity"]["hard_crashes"] += 1
            # A catastrophic collapse inflicts severe damage to the resonance lattice
            data["system_integrity"]["resonance_health"] = max(0.0, data["system_integrity"]["resonance_health"] - 15.0)
        else:
            data["system_integrity"]["elastic_yields"] += 1
            # An elastic yield represents micromechanical fatigue, slowly degrading the structure
            data["system_integrity"]["resonance_health"] = max(0.0, data["system_integrity"]["resonance_health"] - 0.5)
            
        self._write_json(data)

    def _generate_markdown(self):
        """Generates the SOVEREIGN_LEDGER.md overview for narrative and diagnostic reference."""
        data = self._read_json()
        
        md_lines = [
            "# 🏛️ SOVEREIGN LEDGER",
            "",
            "> **CLASSIFICATION: DIRECTORY PRIME**  ",
            "> *Permanent record of the Vitrification Handler. Documents structural degradation and micro-yielding of the simulation lattice over time.*",
            "",
            "## 📐 Mathematical Framework",
            "",
            f"- **Temporal Roots (Gap)**: `{data['mathematical_framework']['temporal_polynomial']}`",
            f"- **Geometric Roots (Magnitude)**: `{data['mathematical_framework']['geometric_polynomial']}`",
            f"- **Hades Beat (ω)**: `{data['mathematical_framework']['hades_beat']}` Hz",
            f"- **Overpack Delta (δ)**: `{data['mathematical_framework']['overpack_delta']}`",
            "",
            "## 📉 System Integrity",
            "",
            f"- **Resonance Health**: **{data['system_integrity']['resonance_health']:.2f}%**",
            f"- **Total Stress Events**: {data['system_integrity']['total_events']}",
            f"- **Elastic Yields**: {data['system_integrity']['elastic_yields']}",
            f"- **Hard Collapses**: {data['system_integrity']['hard_crashes']}",
            "",
            "## 📖 Vitrification Scar Log",
            "",
            "| Timestamp | Node | Angle | Applied Δ | Action / Deformation |",
            "|-----------|------|-------|-----------|----------------------|"
        ]

        if not data["vitrification_events"]:
            md_lines.append("| *N/A*     | *-*  | *-*   | *-*       | *Lattice pristine, no events logged.* |")
        else:
            for ev in data["vitrification_events"]:
                # Format timestamp for better readability
                try:
                    dt = datetime.fromisoformat(ev["timestamp"])
                    ts_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    ts_str = ev["timestamp"]
                    
                md_lines.append(
                    f"| {ts_str} | **{ev['node_id']}** | {ev['angle_deg']}° | `{ev['applied_delta']:.6f}` | {ev['recovery_action']} |"
                )
                
        with open(MD_PATH, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines) + "\n")

if __name__ == "__main__":
    writer = LedgerWriter()
    print(f"Ledger synced successfully: {MD_PATH}")
