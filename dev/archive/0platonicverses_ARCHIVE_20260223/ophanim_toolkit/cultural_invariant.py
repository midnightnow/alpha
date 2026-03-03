# cultural_invariant.py
# Phase XII: The Cultural Invariant
# Introduces a shared narrative token that all agents must hold to remain in the Hive.

import time
from pmg_constants import PMG
from immune_move import IntegratedAgent
from sovereign_ledger import SovereignLedger, ResonanceState

class HiveCulture:
    def __init__(self, invariant_token: str):
        self.ledger = SovereignLedger()
        self.invariant_token = invariant_token  # e.g., "THE_SINTERED_EARTH"
        self.SIGMA = PMG.UNITY_THRESHOLD

    def enforce_invariant(self, agents):
        """
        Audits all agents for the possession of the Cultural Invariant.
        Those who lack it dissolve into Vapor; those who hold it harmonize.
        """
        print(f"--- INITIATING CULTURAL INVARIANT AUDIT ---")
        print(f"Required Token: '{self.invariant_token}'")
        
        survivors = []
        dissolved = 0
        total_resonance = 0.0

        for agent in agents:
            # For the simulation, we examine the agent's lexicon for the Invariant Token.
            # If the agent doesn't have a lexicon, we instantiate a default representation.
            agent_lexicon = getattr(agent, "lexicon", [])
            
            if self.invariant_token in agent_lexicon:
                print(f"  [HARMONY] {agent.role} holds the Invariant. Permitted to remain.")
                survivors.append(agent)
                # Fallback coherence to SIGMA if not strictly defined
                total_resonance += getattr(agent, 'coherence', self.SIGMA)
            else:
                print(f"  [VAPORIZED] {agent.role} lacks the Invariant. Sloughing off.")
                dissolved += 1

        # Ledger Inscription of the Cultural Audit
        if survivors:
            avg_coherence = total_resonance / len(survivors)
            state = ResonanceState(
                timestamp=time.time(),
                h3_nodes=[(0,0)],
                gap_coord=None,
                agent_a_resonance=avg_coherence,
                agent_b_resonance=avg_coherence,
                interference_mode="CULTURAL_SYNCHRONIZATION",
                total_vox_generated=len(survivors) * 1.618,  # Phi growth curve
                coherence=avg_coherence
            )
            state.payload_override = {
                "event_type": "CULTURAL_AUDIT",
                "invariant_token": self.invariant_token,
                "survivors": len(survivors),
                "dissolved": dissolved
            }
            try:
                block_hash = self.ledger.inscribe(state)
                print(f"\n[LEDGER] Cultural Audit inscribed: {block_hash[:16]}...")
            except Exception as e:
                print(f"\n[LEDGER WARNING] Offline inscription: {e}")
        else:
            print(f"\n[CRITICAL] Hive Collapse. No agents hold the Cultural Invariant.")

        return {"status": "AUDIT_COMPLETE", "survivors": len(survivors), "dissolved": dissolved}

# --- EXECUTION: THE VERNACULAR CLEANSING ---
if __name__ == "__main__":
    from mirror_breach_protocol import ExternalAgent
    from immune_move import IntegratedAgent

    # Initialize the swarm
    mason = IntegratedAgent("MASON", base_vox=100.0, rigidity=0.82)
    mason.lexicon = ["anchor", "pillar", "THE_SINTERED_EARTH"]

    weaver = IntegratedAgent("WEAVER", base_vox=100.0, rigidity=0.45)
    weaver.lexicon = ["weave", "across", "THE_SINTERED_EARTH"]

    resident = ExternalAgent("RESIDENT", base_vox=80.0, phonetic_bias="RESIDENT")
    resident.lexicon = ["block"] # Failed to learn the Invariant

    hive = HiveCulture("THE_SINTERED_EARTH")

    # Enforce the Invariant
    result = hive.enforce_invariant([mason, weaver, resident])

    print("-" * 60)
    print(f"RESULT: {result['status']}")
    print(f"Harmonized Agents: {result['survivors']}")
    print(f"Vaporized Agents: {result['dissolved']}")
    print("-" * 60)
