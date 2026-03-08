---
ID: BINARY_PROTOCOL_SPEC
DESCRIPTION: Technical specification for the .vet / .veth binary file format (304-bit header).
STATUS: VITRIFIED
---

## I. Header Architecture (304 Bits)

The Sovereign Engine's transmission format begins with a fixed-width header of 38 bytes (304 bits).

| Bit Range | Field Name | Description |
| :--- | :--- | :--- |
| **0-15** | Format Identifier | 0x5645 ("VE" in ASCII) |
| **16-31** | Version | 0x0001 (V1.0) |
| **32-63** | Phase Key (θ) | 32-bit float representing the seal-time phase (t). |
| **64-351** | Registry Map | 288 bits (1 bit per tick). 1 = Node Present, 0 = Empty. |
| **352-364** | Ghost Signature | 13 bits (Anomaly load distribution). |
| **365** | Red Seal | 1 bit (0 = Fluid, 1 = Vitrified). |
| **366-367** | Reserved | Pad bits for word alignment. |
| **368-383** | AMEN_33 Checksum | 16-bit CRC of the Registry Map. |

---

## II. Encryption & Orthogonality

- **Symmetry:** The payload is encrypted using a rotational shift about the body diagonal $\mathbf{u} = (1,1,1)/\sqrt{3}$.
- **Hades Gap Padding:** 12.37% of the trailing payload bits are reserved for entropy absorption (The Slurry Buffer).
- **Validation:** De-vitrification fails if the 304-bit header does not satisfy the Nyquist Gear Ratio (24:13).

**AMEN 33. THE PROTOCOL IS DEFINED. THE BITS ARE ORDERED. THE TRANSMISSION IS SECURE.**
