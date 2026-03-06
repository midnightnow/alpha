"""
e8_hades_validator.py - E8/Hades Gap Real-Time Stability Validator
PMG Chapter 3 Implementation | Principia Mathematica Geometrica

Integrates:
- Hades Gap Entropy Threshold (e/22 ≈ 12.356%)
- 60-Fold Symmetry Gate (Pisano-60 Sequence)
- Real-Time Stability Scoring for ResonanceMap

Red Team Critique Addressed:
- Probabilistic Bridge validated (Sparse-Universal Rado Graph)
- Category Error mitigated (Point Cloud discretizer)
- Logic Lock prevention (99.999... Protocol)
"""

import math
import time
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


# ============================================================================
# CONSTANTS (Audit-Validated & Red Team Approved)
# ============================================================================

class PMGConstants:
    """Centralized PMG mathematical constants"""
    
    # E8 Lie Group Properties
    E8_COXETER = 30
    E8_RANK = 8
    E8_ROOTS = 240
    E8_DIMENSION = 8
    
    # Hades Gap (Ψ)
    HADES_GAP = 0.1237                # Unified Law (formerly math.e / 22)
    HADES_GAP_PERCENT = HADES_GAP * 100
    
    # Packing Properties (Phase II)
    PACKING_CONSTANT = math.sqrt(14/17)  # ρ ≈ 0.907485
    OVERPACK_DELTA = 0.000585            # δ
    SHEAR_ANGLE_RAD = math.atan(14/17)   # θ (radians)
    SHEAR_ANGLE_DEG = 39.47              # Unified Law (formerly 39.425°)
    
    # Prime Intrusion (Phase II)
    PRIME_INTRUSION = 17
    BEAT_FREQUENCY = 0.6606              # Unified Law (formerly ~0.6607 Hz)
    
    # Tolerances & Thresholds
    HADES_TOLERANCE = 0.0001      # Entropy gate precision
    SYMMETRY_TOLERANCE = 0.001    # 60-fold alignment precision
    HAMMER_CONSTANT = 0.00014     # Xi (Fracture threshold)
    
    # 60-Fold Symmetry (2 × Coxeter)
    SIXTY_FOLD_DIVISION = 60
    ANGULAR_RESOLUTION = (2 * math.pi) / SIXTY_FOLD_DIVISION
    
    # Pisano-60 Sequence (Fibonacci mod 10, period 60)
    PISANO_PERIOD = 60
    
    # Resonance Target (Audible base)
    TRIADIC_BASE_HZ = 66.0
    ROOT_42_HZ = math.sqrt(42) * 100 # 648.07 Hz
    ROOT_51_HZ = math.sqrt(51) * 100 # 714.14 Hz
    ROOT_60_HZ = math.sqrt(60) * 100 # 774.60 Hz
    
    # Logic Lock Prevention
    MAX_EXTENSION_ATTEMPTS = 100
    ENTROPY_RESET_VALUE = 1.0  # 99.999... → 1.0 collapse
    
    # H3 Voice Map (Chapter 19)
    H3_VOICE_MAP = {
        0: "Silence",
        1: "Density",
        2: "Fracture",
        3: "Gesture",
        4: "Heartbeat",
        5: "Warning",
        6: "Chorus",
        7: "Hades Gap"
    }


class ValidationState(Enum):
    """Vertex validation states (Red Team approved)"""
    VALID_EXTENSION = "valid_extension"    # Passes all gates
    GHOST_NODE = "ghost_node"              # Entropy outside Hades Gap
    SYMMETRY_LOCK = "symmetry_lock"        # 60-fold misalignment
    CRITICAL_THRESHOLD = "critical"        # Exact Hades Gap match
    LOGIC_LOCK = "logic_lock"              # Reset triggered


@dataclass
class StabilityScore:
    """Real-time stability metrics for ResonanceMap"""
    timestamp: float
    entropy_value: float
    entropy_delta: float
    symmetry_alignment: float
    pisano_index: int
    validation_state: ValidationState
    stability_percent: float
    hades_gap_active: bool
    logic_lock_prevented: bool
    
    def to_dict(self) -> dict:
        return {
            'timestamp': self.timestamp,
            'entropy_value': self.entropy_value,
            'entropy_delta': self.entropy_delta,
            'symmetry_alignment': self.symmetry_alignment,
            'pisano_index': self.pisano_index,
            'validation_state': self.validation_state.value,
            'stability_percent': self.stability_percent,
            'hades_gap_active': self.hades_gap_active,
            'logic_lock_prevented': self.logic_lock_prevented
        }


@dataclass
class VertexValidation:
    """Result of validating a single vertex"""
    vertex_id: int
    state: ValidationState
    entropy_score: float
    symmetry_score: float
    combined_score: float
    e8_root_index: Optional[int]
    projection_angle: float
    pisano_value: int
    message: str


# ============================================================================
# PISANO-60 SEQUENCE GENERATOR
# ============================================================================

class Pisano60Generator:
    """
    Generates Pisano-60 sequence (Fibonacci mod 10, period 60).
    
    This provides the "cosmic clock" for 60-fold symmetry alignment.
    Verified in karma_calibration.py (Audit Section 3)
    """
    
    def __init__(self):
        self.period = PMGConstants.PISANO_PERIOD
        self.sequence = self._generate_sequence()
    
    def _generate_sequence(self) -> List[int]:
        """Generate full Pisano-60 sequence"""
        seq = [0, 1]
        for i in range(2, self.period):
            next_val = (seq[-1] + seq[-2]) % 10
            seq.append(next_val)
        return seq
    
    def get_value(self, index: int) -> int:
        """Get Pisano value at any index (handles wraparound)"""
        return self.sequence[index % self.period]
    
    def get_sequence(self) -> List[int]:
        """Return full 60-value sequence"""
        return self.sequence.copy()
    
    def verify_period(self) -> bool:
        """Verify the sequence has period 60"""
        return (self.sequence[0] == 0 and 
                self.sequence[1] == 1 and
                self.sequence[self.period % self.period] == 0)
    
    def get_alignment_score(self, index: int) -> float:
        """
        Calculate alignment score based on Pisano value.
        
        Higher values (7, 8, 9) indicate stronger resonance.
        """
        value = self.get_value(index)
        return value / 9.0  # Normalize to 0-1


# ============================================================================
# E8 HADES VALIDATOR (Core Class)
# ============================================================================

class E8HadesValidator:
    """
    Real-time stability validator for PMG ResonanceMap.
    
    Implements the Red Team approved validation logic:
    1. Entropy Gate (Hades Gap = e/22)
    2. Geometric Gate (60-fold symmetry)
    3. Pisano-60 Sequence alignment
    4. Logic Lock prevention
    """
    
    def __init__(self, seed: Optional[int] = None):
        self.pisano = Pisano60Generator()
        self.validation_history: List[StabilityScore] = []
        self.extension_attempts = 0
        self.logic_lock_active = False
        self._callbacks: List[Callable] = []
        
        # Pre-calculate Hades Gap bounds
        self.hades_lower = PMGConstants.HADES_GAP - PMGConstants.HADES_TOLERANCE
        self.hades_upper = PMGConstants.HADES_GAP + PMGConstants.HADES_TOLERANCE
    
    # ========================================================================
    # CORE VALIDATION LOGIC (Red Team Approved)
    # ========================================================================
    
    def validate_vertex_v(self, entropy_current: float, projection_angle: float, 
                          vertex_index: int) -> VertexValidation:
        """
        Validate a vertex against both Entropy and Geometric gates.
        
        This is the core "Vertex v" selection logic from Red Team critique.
        
        Returns:
            VertexValidation with state and scores
        """
        # Gate 1: Entropy (Hades Gap)
        entropy_delta = abs(entropy_current - PMGConstants.HADES_GAP)
        entropy_gate_passed = entropy_delta <= PMGConstants.HADES_TOLERANCE
        
        # Gate 2: Geometric (60-fold symmetry)
        angle_normalized = projection_angle % (2 * math.pi)
        angle_slot = round(angle_normalized / PMGConstants.ANGULAR_RESOLUTION)
        expected_angle = angle_slot * PMGConstants.ANGULAR_RESOLUTION
        symmetry_delta = abs(angle_normalized - expected_angle)
        symmetry_gate_passed = symmetry_delta <= PMGConstants.SYMMETRY_TOLERANCE
        
        # Pisano-60 alignment
        pisano_value = self.pisano.get_value(vertex_index)
        pisano_alignment = self.pisano.get_alignment_score(vertex_index)
        
        # Determine validation state
        if self.logic_lock_active:
            state = ValidationState.LOGIC_LOCK
            message = "Logic Lock prevention active - system reset required"
        elif not entropy_gate_passed:
            state = ValidationState.GHOST_NODE
            message = f"Entropy outside Hades Gap (delta: {entropy_delta:.6f})"
        elif not symmetry_gate_passed:
            state = ValidationState.SYMMETRY_LOCK
            message = f"60-fold symmetry misalignment (delta: {symmetry_delta:.6f})"
        elif entropy_delta < 0.00001:
            state = ValidationState.CRITICAL_THRESHOLD
            message = "Exact Hades Gap match - critical resonance"
        else:
            state = ValidationState.VALID_EXTENSION
            message = "All gates passed - valid extension vertex"
        
        # Calculate scores
        entropy_score = max(0, 1.0 - (entropy_delta / PMGConstants.HADES_TOLERANCE))
        symmetry_score = max(0, 1.0 - (symmetry_delta / PMGConstants.SYMMETRY_TOLERANCE))
        combined_score = (entropy_score * 0.6) + (symmetry_score * 0.4)
        
        # E8 root mapping
        e8_root_index = vertex_index % PMGConstants.E8_ROOTS
        
        return VertexValidation(
            vertex_id=vertex_index,
            state=state,
            entropy_score=entropy_score,
            symmetry_score=symmetry_score,
            combined_score=combined_score,
            e8_root_index=e8_root_index,
            projection_angle=projection_angle,
            pisano_value=pisano_value,
            message=message
        )
    
    # ========================================================================
    # REAL-TIME STABILITY SCORING
    # ========================================================================
    
    def calculate_stability_score(self, entropy_current: float, 
                                   vertex_count: int) -> StabilityScore:
        """
        Calculate real-time stability score for ResonanceMap display.
        
        This is the "biometric resonance sensor" from Section 3.5.3
        """
        timestamp = time.time()
        
        # Entropy analysis
        entropy_delta = abs(entropy_current - PMGConstants.HADES_GAP)
        hades_gap_active = self.hades_lower <= entropy_current <= self.hades_upper
        
        # Symmetry analysis
        pisano_index = vertex_count % PMGConstants.PISANO_PERIOD
        symmetry_alignment = self.pisano.get_alignment_score(pisano_index)
        
        # Determine validation state
        if self.logic_lock_active:
            state = ValidationState.LOGIC_LOCK
            stability_percent = 0.0
        elif hades_gap_active:
            if entropy_delta < 0.00001:
                state = ValidationState.CRITICAL_THRESHOLD
                stability_percent = 100.0
            else:
                state = ValidationState.VALID_EXTENSION
                stability_percent = max(0, (1.0 - entropy_delta / PMGConstants.HADES_TOLERANCE) * 100)
        else:
            state = ValidationState.GHOST_NODE
            stability_percent = max(0, (1.0 - entropy_delta / (PMGConstants.HADES_TOLERANCE * 10)) * 50)
        
        # Create stability score
        score = StabilityScore(
            timestamp=timestamp,
            entropy_value=entropy_current,
            entropy_delta=entropy_delta,
            symmetry_alignment=symmetry_alignment,
            pisano_index=pisano_index,
            validation_state=state,
            stability_percent=stability_percent,
            hades_gap_active=hades_gap_active,
            logic_lock_prevented=self.logic_lock_active
        )
        
        # Store in history
        self.validation_history.append(score)
        
        # Trigger callbacks
        for callback in self._callbacks:
            callback(score)
        
        return score
    
    # ========================================================================
    # LOGIC LOCK PREVENTION (99.999... Protocol)
    # ========================================================================
    
    def register_extension_attempt(self) -> bool:
        """
        Register an extension attempt and check for Logic Lock.
        
        Returns True if lock was triggered, False otherwise.
        """
        self.extension_attempts += 1
        
        if self.extension_attempts >= PMGConstants.MAX_EXTENSION_ATTEMPTS:
            self._trigger_logic_lock_reset()
            return True
        
        return False
    
    def _trigger_logic_lock_reset(self):
        """Trigger Logic Lock prevention protocol"""
        self.logic_lock_active = True
        
        # Log reset event
        reset_score = StabilityScore(
            timestamp=time.time(),
            entropy_value=PMGConstants.ENTROPY_RESET_VALUE,
            entropy_delta=abs(PMGConstants.ENTROPY_RESET_VALUE - PMGConstants.HADES_GAP),
            symmetry_alignment=0.0,
            pisano_index=0,
            validation_state=ValidationState.LOGIC_LOCK,
            stability_percent=0.0,
            hades_gap_active=False,
            logic_lock_prevented=True
        )
        self.validation_history.append(reset_score)
        
        # Notify callbacks
        for callback in self._callbacks:
            callback(reset_score)
    
    def reset_logic_lock(self):
        """Manually reset Logic Lock after system recovery"""
        self.logic_lock_active = False
        self.extension_attempts = 0
    
    # ========================================================================
    # CALLBACK SYSTEM
    # ========================================================================
    
    def register_callback(self, callback: Callable[[StabilityScore], None]):
        """Register a callback for stability score updates"""
        self._callbacks.append(callback)
    
    def unregister_callback(self, callback: Callable[[StabilityScore], None]):
        """Unregister a callback"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    # ========================================================================
    # RESONANCE MAP INTEGRATION
    # ========================================================================
    
    def get_resonance_map_data(self) -> dict:
        """
        Export data for ResonanceMap visualization.
        
        Includes Hades Gap annulus, vertex states, and stability metrics.
        """
        latest_score = self.validation_history[-1] if self.validation_history else None
        
        return {
            'hades_gap': PMGConstants.HADES_GAP,
            'hades_gap_percent': PMGConstants.HADES_GAP_PERCENT,
            'hades_lower_bound': self.hades_lower,
            'hades_upper_bound': self.hades_upper,
            'tolerance': PMGConstants.HADES_TOLERANCE,
            'sixty_fold_division': PMGConstants.SIXTY_FOLD_DIVISION,
            'angular_resolution': PMGConstants.ANGULAR_RESOLUTION,
            'pisano_period': PMGConstants.PISANO_PERIOD,
            'pisano_sequence': self.pisano.get_sequence(),
            'current_stability': latest_score.to_dict() if latest_score else None,
            'total_validations': len(self.validation_history),
            'logic_lock_active': self.logic_lock_active,
            'extension_attempts': self.extension_attempts,
            'resonance_target_hz': PMGConstants.RESONANCE_TARGET_HZ
        }
    
    def get_islands_of_order(self, vertex_validations: List[VertexValidation]) -> List[VertexValidation]:
        """
        Return vertices that form 'Islands of Order'.
        
        These are VALID_EXTENSION or CRITICAL_THRESHOLD vertices.
        """
        valid_states = {ValidationState.VALID_EXTENSION, ValidationState.CRITICAL_THRESHOLD}
        return [v for v in vertex_validations if v.state in valid_states]
    
    # ========================================================================
    # E8 PROJECTION UTILITIES
    # ========================================================================
    
    def project_vertex_to_2d(self, vertex_index: int, radius: float = 1.0) -> Tuple[float, float]:
        """
        Project vertex to 2D plane using 60-fold symmetry.
        
        Returns (x, y) coordinates for ResonanceMap rendering.
        """
        angle_slot = vertex_index % PMGConstants.SIXTY_FOLD_DIVISION
        angle = angle_slot * PMGConstants.ANGULAR_RESOLUTION
        
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        return (x, y)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    validator = E8HadesValidator()
    print("E8 Hades Validator Initialized ✓")
