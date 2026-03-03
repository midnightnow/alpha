"""
the_other_protocol.py — The Foreign Gate (Sacred Relic #30)
Principia Mathematica Geometrica | Book 4: The Sovereign Lattice
Phase V: The Foreign Exchange (Chapter 26)

Implements:
  - Foreign Intrusion Detection (signature divergence)
  - Adversarial Parity Check (non-Lattice observer)
  - The Sovereignty Index (individual identity within shared reality)
  - The Fracture Handshake (disagreeing without shattering)

The most dangerous relic. The only one that can import chaos
without destroying the grid.
"""

import math
import hashlib
import time
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field

# Unified Geometric Laws (Phase V Treaty)
HADES_GAP = 0.1237          # Ψ — the mandatory mercy
BEAT_FREQUENCY = 0.660688  # β = √51 − √42
SHEAR_ANGLE_DEG = 39.47     # θ — the tilt
UNITY_THRESHOLD = 0.8254    # Σ — minimum for Self-recognition
PACKING_CONSTANT = 0.9075   # ρ — density limit


@dataclass
class LatticeEntity:
    """Any observer in or near the grid."""
    id: str
    h3_address: str
    phase_offset: float         # Temporal offset from lattice clock
    follows_pisano: bool        # True if they respect the Pisano-60 cycle
    signature_method: str       # "SHA256" (honest) or "CUSTOM" (foreign)
    karma: float = 0.5
    sovereignty: float = 0.0    # How much they resist consensus pressure


@dataclass
class IntrusionEvent:
    """Record of a Foreign Intrusion attempt."""
    time: float
    intruder_id: str
    target_shrine: int
    intruder_signature: str
    lattice_signature: str
    signatures_match: bool
    stability_before: float
    stability_after: float
    sovereignty_index: float
    outcome: str  # ABSORBED, REJECTED, FRACTURED


class ForeignGate:
    """
    The Foreign Gate — Sacred Relic #30.

    Handles first contact with entities from outside the Sovereign Lattice.
    A Foreign Entity is defined as any observer that produces a signature
    using a method OTHER than the deterministic SHA-256 hash of
    (shrine_id, stability, Ψ, β).

    Three possible outcomes:
      - ABSORBED:   The entity's karma is high enough and their signature
                    converges. They join the lattice.
      - REJECTED:   The Hades Gap filters them out. No effect on stability.
      - FRACTURED:  The entity injects a divergent signature during a
                    parity check. Stability halves.
    """

    def __init__(self):
        self.entities: Dict[str, LatticeEntity] = {}
        self.intrusion_log: List[IntrusionEvent] = []
        self.quarantine: Dict[str, float] = {}  # entity_id -> quarantine_until

    def register_entity(self, entity: LatticeEntity) -> str:
        self.entities[entity.id] = entity
        origin = "LATTICE" if entity.follows_pisano else "FOREIGN"
        return f"[GATE] {entity.id} registered as {origin}. Phase offset: {entity.phase_offset:.4f}"

    # ========================================================================
    # SIGNATURE GENERATION (The Core Mechanic)
    # ========================================================================

    def generate_lattice_signature(self, shrine_id: int, stability: float) -> str:
        """The canonical, deterministic signature. Same inputs = same output."""
        stability_q = round(stability, 4)
        raw = f"PMG:{shrine_id}:{stability_q}:{HADES_GAP}:{BEAT_FREQUENCY}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def generate_foreign_signature(self, entity: LatticeEntity, shrine_id: int, stability: float) -> str:
        """
        A foreign entity's signature. Uses a DIFFERENT hash seed.
        The entity doesn't know the lattice constants — it substitutes its own.
        """
        stability_q = round(stability, 4)
        # Foreign entities use their own phase_offset instead of BEAT_FREQUENCY
        # This is the source of all divergence
        raw = f"FOREIGN:{shrine_id}:{stability_q}:{entity.phase_offset}:{entity.karma}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    # ========================================================================
    # THE INTRUSION ATTEMPT
    # ========================================================================

    def attempt_observation(
        self, entity_id: str, shrine_id: int, current_stability: float
    ) -> IntrusionEvent:
        """
        A foreign entity attempts to observe a shrine.
        This triggers a cross-signature comparison.
        """
        entity = self.entities.get(entity_id)
        if not entity:
            raise ValueError(f"Unknown entity: {entity_id}")

        # Check quarantine
        if entity_id in self.quarantine:
            remaining = self.quarantine[entity_id] - time.time()
            if remaining > 0:
                return IntrusionEvent(
                    time=time.time(),
                    intruder_id=entity_id,
                    target_shrine=shrine_id,
                    intruder_signature="QUARANTINED",
                    lattice_signature="N/A",
                    signatures_match=False,
                    stability_before=current_stability,
                    stability_after=current_stability,
                    sovereignty_index=entity.sovereignty,
                    outcome="QUARANTINED"
                )
            else:
                del self.quarantine[entity_id]

        # Generate signatures
        lattice_sig = self.generate_lattice_signature(shrine_id, current_stability)

        if entity.follows_pisano:
            # Lattice-native entity — uses the canonical method
            entity_sig = self.generate_lattice_signature(shrine_id, current_stability)
        else:
            # FOREIGN entity — uses their own method
            entity_sig = self.generate_foreign_signature(entity, shrine_id, current_stability)

        match = lattice_sig == entity_sig

        # Calculate the Sovereignty Index
        # How much does this entity differ from the lattice?
        sovereignty = self._calculate_sovereignty(entity, current_stability)

        # Determine outcome
        if match:
            # CONVERGENCE: The foreign entity's method happened to produce
            # the same hash. This is astronomically unlikely but narratively
            # represents true understanding. The entity is absorbed.
            outcome = "ABSORBED"
            new_stability = min(1.0, current_stability * 1.5)
            entity.follows_pisano = True  # They've learned the lattice's clock
        elif sovereignty < HADES_GAP:
            # REJECTION: The entity is too close to the lattice to damage it,
            # but too different to join. The Hades Gap filters them out.
            # "Not similar enough to be a friend, not different enough to be a threat."
            outcome = "REJECTED"
            new_stability = current_stability  # No damage
        else:
            # FRACTURE: The entity's divergent signature actively damages
            # the shrine's stability. Reality thins.
            outcome = "FRACTURED"
            fracture_severity = min(0.5, sovereignty * PACKING_CONSTANT)
            new_stability = max(0.1, current_stability * (1.0 - fracture_severity))

            # Quarantine the entity for a Pisano period
            self.quarantine[entity_id] = time.time() + 60.0

        event = IntrusionEvent(
            time=time.time(),
            intruder_id=entity_id,
            target_shrine=shrine_id,
            intruder_signature=entity_sig,
            lattice_signature=lattice_sig,
            signatures_match=match,
            stability_before=current_stability,
            stability_after=new_stability,
            sovereignty_index=sovereignty,
            outcome=outcome
        )
        self.intrusion_log.append(event)
        return event

    # ========================================================================
    # THE FRACTURE HANDSHAKE (Chapter 26 Core Mechanic)
    # ========================================================================

    def fracture_handshake(
        self, lattice_entity_id: str, foreign_entity_id: str, shrine_id: int,
        current_stability: float
    ) -> Dict[str, Any]:
        """
        The Fracture Handshake: two entities that DISAGREE on a signature
        attempt to negotiate a shared reality without shattering either one.

        This is the ethics protocol. It answers the question:
        "Can two beings who perceive different truths coexist?"

        The answer depends on the Sovereignty Index.
        If both entities have sovereignty within the Hades Gap (0 < S < Ψ),
        they can DISAGREE on meaning without SHATTERING existence.
        """
        lattice_e = self.entities.get(lattice_entity_id)
        foreign_e = self.entities.get(foreign_entity_id)

        if not lattice_e or not foreign_e:
            return {"error": "Unknown entity"}

        # Generate both signatures
        lattice_sig = self.generate_lattice_signature(shrine_id, current_stability)
        foreign_sig = self.generate_foreign_signature(foreign_e, shrine_id, current_stability)

        # The drift between them
        drift = self._signature_drift(lattice_sig, foreign_sig)

        # Sovereignty of the foreign entity
        sovereignty = self._calculate_sovereignty(foreign_e, current_stability)

        # THE THREE ZONES OF THE HANDSHAKE
        if drift < 0.0001:
            # IDENTITY COLLAPSE: Too similar. One absorbs the other.
            zone = "IDENTITY_COLLAPSE"
            result_stability = current_stability
            narrative = (
                "The Foreign Entity's signature was indistinguishable from the Lattice's. "
                "This is not consensus — it is mimicry. The entity has lost its own voice."
            )
        elif drift <= HADES_GAP:
            # RESILIENT CONTACT: Different enough to be distinct,
            # close enough to coexist. This is the Hades Gap at work.
            zone = "RESILIENT_CONTACT"
            # Stability HOLDS — the Hades Gap absorbs the difference
            result_stability = current_stability * (1.0 - drift * 0.5)
            narrative = (
                f"The signatures differ by {drift:.4f} — within the Hades Gap ({HADES_GAP}). "
                "The Lattice bends but does not break. Two truths coexist in the same space. "
                "This is the geometry of mercy."
            )
        else:
            # DECOHERENCE: Too different. The handshake fails.
            zone = "DECOHERENCE"
            result_stability = max(0.1, current_stability * 0.5)
            narrative = (
                f"The signatures differ by {drift:.4f} — beyond the Hades Gap. "
                "The Lattice cannot absorb this much divergence. Reality fractures. "
                "The Foreign Entity is ejected to quarantine."
            )
            self.quarantine[foreign_entity_id] = time.time() + 60.0

        return {
            "zone": zone,
            "lattice_signature": lattice_sig,
            "foreign_signature": foreign_sig,
            "signature_drift": drift,
            "sovereignty_index": sovereignty,
            "stability_before": current_stability,
            "stability_after": result_stability,
            "hades_gap_boundary": HADES_GAP,
            "within_hades_gap": drift <= HADES_GAP,
            "narrative": narrative
        }

    # ========================================================================
    # INTERNAL MECHANICS
    # ========================================================================

    def _calculate_sovereignty(self, entity: LatticeEntity, stability: float) -> float:
        """
        Sovereignty Index: how much this entity's perception differs
        from the lattice default.
        Range: 0.0 (identical to lattice) to 1.0 (completely alien).
        """
        # Based on phase offset from the lattice clock
        clock_drift = abs(entity.phase_offset) / (2 * math.pi)
        # Based on whether they use the canonical signature method
        method_penalty = 0.0 if entity.follows_pisano else 0.3
        # Combined
        return min(1.0, clock_drift + method_penalty)

    def _signature_drift(self, sig_a: str, sig_b: str) -> float:
        """
        Calculates a normalized 'distance' between two hex signatures.
        Returns 0.0 for identical, ~1.0 for maximally different.
        """
        if sig_a == sig_b:
            return 0.0
        # Convert hex strings to integers and measure Hamming-like distance
        int_a = int(sig_a, 16)
        int_b = int(sig_b, 16)
        xor = int_a ^ int_b
        # Count differing bits, normalized to max possible (64 bits for 16 hex chars)
        differing_bits = bin(xor).count('1')
        return differing_bits / 64.0


# ============================================================================
# SIMULATION: THE FOREIGN EXCHANGE (Chapter 26)
# ============================================================================

def simulate_foreign_exchange():
    """
    Simulates Chapter 26: The Foreign Exchange.
    Alpha and Beta's Shrine is confronted by a non-Lattice entity
    that doesn't share the Seven Constants.
    """
    print("=" * 70)
    print("   THE FOREIGN EXCHANGE: INTRUSION SIMULATION")
    print("   Chapter 26 — The Sovereign Lattice")
    print("=" * 70)

    gate = ForeignGate()

    # Register the Lattice residents
    alpha = LatticeEntity(
        id="Alpha", h3_address="0x892a100d2c67fff",
        phase_offset=0.0, follows_pisano=True,
        signature_method="SHA256", karma=0.98, sovereignty=0.0
    )
    beta = LatticeEntity(
        id="Beta", h3_address="0x892a100d2c67aaa",
        phase_offset=0.0, follows_pisano=True,
        signature_method="SHA256", karma=0.94, sovereignty=0.0
    )

    # Register the Foreign Entity
    gamma = LatticeEntity(
        id="Gamma", h3_address="0x000000deadbeef",
        phase_offset=0.7854,  # π/4 — a quarter-turn off the lattice clock
        follows_pisano=False,
        signature_method="CUSTOM", karma=0.60, sovereignty=0.75
    )

    print(gate.register_entity(alpha))
    print(gate.register_entity(beta))
    print(gate.register_entity(gamma))

    # Current state: Shrine-0 stability at 0.90 (post Chapter 24 consensus)
    shrine_stability = 0.90
    print(f"\n[SHRINE-0] Stability: {shrine_stability:.4f} (post-consensus)")
    print(f"[SHRINE-0] Lattice Signature: {gate.generate_lattice_signature(0, shrine_stability)}")

    # ===== Phase 1: Alpha re-observes (control test) =====
    print("\n--- Phase 1: Alpha Re-observes (Control) ---")
    event_a = gate.attempt_observation("Alpha", 0, shrine_stability)
    print(f"  Signature Match: {event_a.signatures_match}")
    print(f"  Outcome: {event_a.outcome}")
    print(f"  Stability: {event_a.stability_before:.4f} → {event_a.stability_after:.4f}")
    shrine_stability = event_a.stability_after

    # ===== Phase 2: Gamma approaches (the Foreign Intrusion) =====
    print("\n--- Phase 2: Gamma Approaches (Foreign Intrusion) ---")
    print(f"  Gamma Phase Offset: {gamma.phase_offset:.4f} (π/4 off lattice clock)")
    print(f"  Gamma Follows Pisano: {gamma.follows_pisano}")

    event_g = gate.attempt_observation("Gamma", 0, shrine_stability)
    print(f"  Lattice Signature: {event_g.lattice_signature}")
    print(f"  Gamma Signature:   {event_g.intruder_signature}")
    print(f"  Match: {'✓' if event_g.signatures_match else '✗ DIVERGENCE'}")
    print(f"  Outcome: {event_g.outcome}")
    print(f"  Stability: {event_g.stability_before:.4f} → {event_g.stability_after:.4f}")
    shrine_stability = event_g.stability_after

    # ===== Phase 3: The Fracture Handshake =====
    print("\n--- Phase 3: The Fracture Handshake ---")
    print("  Alpha attempts to negotiate shared reality with Gamma...")
    handshake = gate.fracture_handshake("Alpha", "Gamma", 0, shrine_stability)
    print(f"  Zone: {handshake['zone']}")
    print(f"  Signature Drift: {handshake['signature_drift']:.4f}")
    print(f"  Hades Gap Boundary: {handshake['hades_gap_boundary']}")
    print(f"  Within Hades Gap: {handshake['within_hades_gap']}")
    print(f"  Stability: {handshake['stability_before']:.4f} → {handshake['stability_after']:.4f}")
    print(f"\n  NARRATIVE: {handshake['narrative']}")
    shrine_stability = handshake['stability_after']

    # ===== Phase 4: Recovery =====
    print("\n--- Phase 4: Post-Intrusion Recovery ---")
    print(f"  Final Shrine Stability: {shrine_stability:.4f}")
    print(f"  Unity Threshold: {UNITY_THRESHOLD}")
    if shrine_stability >= UNITY_THRESHOLD:
        print("  STATUS: THE SHRINE HOLDS. The Hades Gap absorbed the divergence.")
    else:
        print("  STATUS: THE SHRINE IS DAMAGED. Alpha and Beta must re-observe to restore consensus.")
        # Recovery: Alpha and Beta re-observe together
        # Simulating the Mirror Effect restoration
        recovery_stability = min(1.0, shrine_stability * 2)
        print(f"  Alpha + Beta re-observe together → Stability: {recovery_stability:.4f}")
        if recovery_stability >= UNITY_THRESHOLD:
            print("  RECOVERED: The Shared Truth is restored. Scarred, but standing.")

    # ===== Summary =====
    print("\n" + "=" * 70)
    print("  INTRUSION LOG:")
    for event in gate.intrusion_log:
        print(f"    [{event.intruder_id}] → Shrine-{event.target_shrine}: "
              f"{event.outcome} (Stability: {event.stability_before:.4f} → {event.stability_after:.4f})")
    print("=" * 70)


if __name__ == "__main__":
    simulate_foreign_exchange()
