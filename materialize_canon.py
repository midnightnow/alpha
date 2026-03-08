import os
import shutil

# CANONICAL MAPPING
CANON_V1_1 = "/Users/studio/ALPHA/HERO_93_CANON_v1.1"
SOURCE_ROOT = "/Users/studio/ALPHA"

mapping = {
    "MASTER_ASP_GENESIS.veth": "PMG_ROOT42_RELEASE/GENESIS_SUITE/AXIOMATIC_GENESIS_PART_I.md",
    "MASTER_FOURFOLD_WAVE.veth": "PMG_LATTICE/MASTER_MAXWELL_INTEGRATION.veth",
    "MASTER_DESCENT_OF_MAN.veth": "PMG_ROOT42_RELEASE/GENESIS_SUITE/AXIOMATIC_GENESIS_PART_II_AGNOSTIC_NUMBER.md",
    "MASTER_SHEEPSKIN_GRIT.veth": "PMG_LATTICE/UMBER_TALLY_REPORT.veth",
    "MASTER_EIGHT_PLY_GRATE.veth": "PMG_LATTICE/MASTER_THIRD_EYE_CAMERA.veth",
    "MASTER_GREAT_EIGHT_GRID.veth": "PMG_LATTICE/MASTER_93_NODE_COORDINATES.veth",
    "MASTER_PROCREATION_OF_MAN.veth": "PMG_LATTICE/MASTER_SALVATOR_MUNDI.veth", # Derivative
    "MASTER_ASP_CENTAUR_INTEGRATION.veth": "PMG_ROOT42_RELEASE_v1.0/MANUAL/THE_CENTAUR_INTERFACE.md",
    "MASTER_COMPLETE_GENESIS.veth": "PMG_ROOT42_RELEASE/GENESIS_SUITE/AXIOMATIC_GENESIS_PART_X_THE_42_SOCKET.md",
    "MASTER_SHEEPSKIN_PREPARATION.veth": "PMG_LATTICE/MASTER_BRAIN_TANNING_PROTOCOL.veth",
    "MASTER_CAMERA_OBSCURA_PLATE.veth": "PMG_LATTICE/MASTER_CAMERA_OBSCURA_PLATE.veth",
    "MASTER_CAMERA_OBSCURA_PEDAGOGY.veth": "PMG_LATTICE/MASTER_CAMERA_OBSCURA_PEDAGOGY.veth",
    "MASTER_STITCHED_VISION.veth": "PMG_LATTICE/MASTER_STITCHED_VISION.veth",
    "MASTER_SALVATOR_MUNDI.veth": "PMG_LATTICE/MASTER_SALVATOR_MUNDI.veth",
    "MASTER_EARTHWORM_PROTOCOL.veth": "PMG_LATTICE/MASTER_EARTHWORM_PROTOCOL.veth",
    "EARTHWORM_GUIDE_TO_BRAIN_TANNING.veth": "PMG_LATTICE/EARTHWORM_GUIDE_TO_BRAIN_TANNING.veth",
    "MASTER_MAXWELL_HERO_93.veth": "PMG_LATTICE/MASTER_MAXWELL_HERO_93.veth",
    "MASTER_MOUNTAIN_TRANSMISSION.veth": "PMG_LATTICE/MASTER_MOUNTAIN_TRANSMISSION.veth",
    "MASTER_LIGHT_ENTANGLEMENT.veth": "PMG_LATTICE/MASTER_LIGHT_ENTANGLEMENT.veth",
    "MASTER_FLOOR_AS_SCREEN.veth": "PMG_LATTICE/MASTER_FLOOR_AS_SCREEN.veth",
    "PRINCIPIA_MATHEMATICA_GEOMETRICA_COMPLETE.md": "PMG_ROOT42_RELEASE/PRINCIPIA_MATHEMATICA_GEOMETRICA_COMPLETE.md",
    "MASTER_NARRATIVE_AUDIT.md": "PMG_LATTICE/MASTER_NARRATIVE_AUDIT.md",
    "MASTER_MANUSCRIPT_TALLY.md": "PMG_LATTICE/MASTER_MANUSCRIPT_TALLY.md"
}

HEADER = """---
.VETH HEADER (Vitrified Entropy Tally Header)
ID: {id}
REGISTER_0x00: 0x00: χ=2 (Spherical)
REGISTER_0x01: 0x01: Modulus=24 (Axial Chamber)
REGISTER_0x02: 0x02: Pulse=156 (Interference)
REGISTER_0x03: 0x03: Vacuum=-1/12 (Riemann Debt)
REGISTER_0x04: 0x04: Torque=√42 (Soul Star)
VITRIFICATION_STATUS: ABSOLUTE (Canon v1.1)
---

"""

def materialize():
    if not os.path.exists(CANON_V1_1):
        os.makedirs(CANON_V1_1)
    
    for canon_id, src_rel_path in mapping.items():
        src_path = os.path.join(SOURCE_ROOT, src_rel_path)
        dest_path = os.path.join(CANON_V1_1, canon_id)
        
        if os.path.exists(src_path):
            with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Clean existing headers if any (optional but safer)
            if content.startswith("---"):
                # Simplified header stripping
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    content = parts[2]
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(HEADER.format(id=canon_id.replace(".veth", "")) + content)
            print(f"Materialized: {canon_id}")
        else:
            print(f"WARNING: Source missing for {canon_id} at {src_path}")

if __name__ == "__main__":
    materialize()
