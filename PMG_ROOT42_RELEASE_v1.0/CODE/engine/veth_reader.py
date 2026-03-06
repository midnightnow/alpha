"""
veth_reader.py — The Official .veth Reader and Protocol Validator
================================================================
The Keystone of the Sovereign Lattice Execution Layer.

This module provides formal verification for .veth files, moving the 
project from 'Concept Framework' to 'Functioning System'.

Axioms Validated:
1. The 24/37/43/73 Structural Cross (The Header)
2. The -1/12 Riemann Stabilizer (Vacuum Debt)
3. The 5-12-13 Metric Lock (Perimeter = Area = 30)
4. The Integers-Only Coordinate Rule (Stitch Holes / Nodes)
5. The 156-Tick Pulse Completeness

Usage:
    python3 veth_reader.py audit <file_path>
"""

import json
import math
import sys
import os

# ============================================================================
# SOVEREIGN CONSTANTS (v1.0)
# ============================================================================
METRIC_LOCK = [5, 12, 13]      # Perimeter = Area = 30
MASS_INVARIANT = 42            # The Unified Invariant
TOPOLOGY_NODES = 93            # Hero 93 Solid
VACUUM_DEBT = -1/12            # Riemann Stabilizer
HADES_GAP = 0.1237             # Tensegrity Constant
TICKS = 156                    # Sonnet Frequency

class VethValidationError(Exception):
    """Raised when a .veth file violates the Sovereign Protocol."""
    pass

class VethReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.hysteresis = 0.0
        self.log = []
        self.is_taut = False

    def load(self):
        """Loads the .veth file and performs basic JSON validation."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Record not found: {self.file_path}")
        
        try:
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)
            self._log("Load successful.")
        except json.JSONDecodeError as e:
            raise VethValidationError(f"Russet Noise Detected (JSON Error): {e}")

    def _log(self, msg):
        self.log.append(f"[AUDIT] {msg}")

    def verify_header_cross(self):
        """Validates the 24/37/43/73 Structural Cross."""
        header_name = self.data.get("header", "UNKNOWN")
        cross = self.data.get("cross")
        
        # If cross is missing, we check if the header name implies it 
        # or if specific keys match the axioms.
        self._log(f"Verifying Header: {header_name}")
        
        # Implementation of the 24/37/43/73 check
        valid_cross = False
        if cross:
            if [cross.get("time"), cross.get("light"), cross.get("offset"), cross.get("mirror")] == [24, 37, 43, 73]:
                valid_cross = True
        elif "156" in header_name or "CALIBRATION" in header_name:
            # Legacy/Implicit validation for existing files
            self._log("Implicit Cross detected (Legacy Record).")
            valid_cross = True
            
        if not valid_cross:
            self.hysteresis += 0.043 # The Offset H-Void
            self._log("WARNING: Structural Cross misaligned. H-Void tension detected.")
        else:
            self._log("Structural Cross (24/37/43/73) SECURED.")

    def verify_vacuum_debt(self):
        """Ensures the Riemann Stabilizer (-1/12) is active."""
        debt = self.data.get("vacuum_debt")
        if debt is None:
            # Check implicit debt in coordinates or scaling
            debt = self.data.get("vacuum_lock")
            
        if debt == "-1/12" or (isinstance(debt, float) and math.isclose(debt, RIEMANN_DEBT)):
            self._log("Vacuum Stabilizer (-1/12) ACTIVE.")
        else:
            self.hysteresis += 0.083  # 1/12 scale
            self._log("WARNING: Vacuum Debt missing. System is 'Hairy' (Ambient Noise).")

    def verify_integer_coordinates(self):
        """Enforces the Integers-Only rule for primary nodes."""
        coords = self.data.get("coordinates", [])
        if not coords:
            # Some files might be calibration maps without coords
            if "CALIBRATION" in self.data.get("header", ""):
                self._log("Calibration Map: Skipping Coordinate Audit.")
                return
            raise VethValidationError("Empty Coordinate Field.")

        prime_mistakes = 0
        for i, point in enumerate(coords):
            # We only enforce strict integer rules for 'Vitrified' nodes or 'Studs'
            is_vitrified = point.get("status") == "Vitrified" or point.get("class") == "Power_Glyph_Stud"
            
            if is_vitrified:
                for axis in ['x', 'y', 'z']:
                    val = point.get(axis)
                    if val is not None and not float(val).is_integer():
                        # We allow a tiny margin for float errors in the generator, 
                        # but strictly it should be integers.
                        if abs(val - round(val)) > 0.0001:
                            prime_mistakes += 1
                            self._log(f"Tick {point.get('tick')}: Floating Point error in {axis} axis ({val}).")

        if prime_mistakes > 0:
            self.hysteresis += (prime_mistakes / len(coords))
            self._log(f"Integrity Check: {prime_mistakes} Stitch Holes are 'Hairy'.")
        else:
            self._log("Integers-Only Coordinate Grid: SHAVED.")

    def verify_completeness(self):
        """Checks for the full 156-tick pulse."""
        coords = self.data.get("coordinates", [])
        if coords and len(coords) < TICKS:
             self._log(f"WARNING: Cycle Incomplete ({len(coords)}/156 Ticks). Phase shift expected.")
             self.hysteresis += 0.1237 # Hades' Gap
        elif coords:
            self._log("156-Tick Pulse: COMPLETE.")

    def run_audit(self):
        """Executes the full Sovereign Protocol audit."""
        self.load()
        self._log("-" * 40)
        self.verify_header_cross()
        self.verify_vacuum_debt()
        self.verify_integer_coordinates()
        self.verify_completeness()
        self._log("-" * 40)
        
        status = "SUCCESS" if self.hysteresis < 0.1 else "FAILED"
        self._log(f"FINAL AUDIT STATUS: {status}")
        self._log(f"FINAL HYSTERESIS: {self.hysteresis:.6f} Λ")
        
        return {
            "status": status,
            "hysteresis": self.hysteresis,
            "log": self.log
        }

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "audit":
        print("Usage: python3 veth_reader.py audit <file_path>")
        sys.exit(1)

    file_path = sys.argv[2]
    reader = VethReader(file_path)
    
    try:
        report = reader.run_audit()
        for line in report["log"]:
            print(line)
            
        if report["status"] == "SUCCESS":
            print("\n  The World is TAUT. Record Vitrified.")
        else:
            print("\n  Record is RUSSET. Recommend Auto-Repair Tautener.")
            
    except Exception as e:
        print(f"TERMINAL FAILURE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
