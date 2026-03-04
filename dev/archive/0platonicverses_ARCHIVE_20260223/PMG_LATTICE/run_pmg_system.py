from pmg_constants import PMG
from sovereign_ledger import SovereignLedger
from sovereign_console import SovereignConsole

def boot():
    print("--- PRINCIPIA MATHEMATICA GEOMETRICA v1.0 BOOTING ---")
    ledger = SovereignLedger()
    console = SovereignConsole()
    print(f"Lattice Beat: {PMG.BEAT_FREQUENCY} Hz")
    print(f"Initial Vox Pool: {console.vox_pool}")
    print("STATUS: SYSTEM LIVE.")

if __name__ == "__main__":
    boot()