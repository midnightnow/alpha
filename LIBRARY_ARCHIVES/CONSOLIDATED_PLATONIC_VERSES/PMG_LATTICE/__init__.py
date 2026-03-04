"""
PMG_LATTICE — The Principia Mathematica Geometrica v1.0
Sovereign Constants, Mechanical Alphabet, and Lattice Physics.

Public API:
    PMG                — Frozen dataclass of all sovereign invariants
    MechanicalAlphabet — 26-vector phonetic torque engine
    SovereignLedger    — Append-only chain with genesis hash 46cb7da997946a14
    LatticeImmunity    — Pre-flight toxic torque rejection
    SovereignConsole   — Command interface with immunity integration
"""

from .pmg_constants import PMG, SovereignConstants
from .mechanical_alphabet import MechanicalAlphabet, GlyphType, GlyphProperties
from .sovereign_ledger import SovereignLedger
from .lattice_immunity import LatticeImmunity
from .sovereign_console import SovereignConsole

__version__ = "1.0.0"
__all__ = [
    "PMG", "SovereignConstants",
    "MechanicalAlphabet", "GlyphType", "GlyphProperties",
    "SovereignLedger",
    "LatticeImmunity",
    "SovereignConsole",
]
