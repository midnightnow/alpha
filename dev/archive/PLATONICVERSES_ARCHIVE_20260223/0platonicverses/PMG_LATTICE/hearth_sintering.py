# hearth_sintering.py
# Phase XVI: Centripetal Stabilization

from sovereign_narrative_sintering import NarrativeSinter

def anchor_the_center():
    print("--- INITIATING CENTRIPETAL STABILIZATION ---")
    sinter = NarrativeSinter()
    
    # Sintering 'THE HEARTH' at the Origin
    result, sigma = sinter.sinter_myth(
        myth_name="The Sovereign Hearth",
        phonetic_root="hearthstone",
        target_coord=(0, 0)
    )
    
    print(f"[STATUS] Center of Gravity re-balanced at (0,0).")
    print(f"[RESULT] {result} | Coherence: {sigma:.4f}")

if __name__ == "__main__":
    anchor_the_center()
