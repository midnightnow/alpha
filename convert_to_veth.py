import os
import re

# Canonical Registers
TOPOLOGY = "0x00: χ=2 (Spherical)"
MODULUS = "0x01: Modulus=24 (Axial Chamber)"
PULSE = "0x02: Pulse=156 (Interference)"
VACUUM = "0x03: Vacuum=-1/12 (Riemann Debt)"
TORQUE = "0x04: Torque=√42 (Soul Star)"

def convert_to_veth(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Create .veth filename
                veth_path = path.replace(".md", ".veth")
                
                header = f"""---
.VETH HEADER (Vitrified Entropy Tally Header)
ID: {f.replace('.md', '')}
REGISTER_0x00: {TOPOLOGY}
REGISTER_0x01: {MODULUS}
REGISTER_0x02: {PULSE}
REGISTER_0x03: {VACUUM}
REGISTER_0x04: {TORQUE}
VITRIFICATION_STATUS: SECURED (Grit 0.00000080)
---

"""
                with open(veth_path, 'w', encoding='utf-8') as vfile:
                    vfile.write(header + content)
                print(f"Vitrified: {veth_path}")

if __name__ == "__main__":
    # Ensure standard locations
    convert_to_veth("/Users/studio/ALPHA/PMG_LATTICE")
    convert_to_veth("/Users/studio/ALPHA/LIBRARY_CANON")
