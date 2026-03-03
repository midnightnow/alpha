# entropy_economy.py
# Handles the decentralized thermodynamics of the Babble post-Fracture.

class NoiseVault:
    """
    Stores high-entropy packets used to obfuscate signatures.
    In the Babble, noise is the only place left to hide.
    """
    def __init__(self):
        self.noise_packets = 0.0
        
    def deposit_noise(self, amount):
        self.noise_packets += amount
        
    def consume_mask(self, intensity):
        """Returns the obfuscation level provided by a mask."""
        if self.noise_packets >= intensity:
            self.noise_packets -= intensity
            return intensity * 1.618 # Phi-scaled hiding depth
        return 0.0

class DecentralizedEntropy:
    """
    Handles the new economic model post-Refactoring.
    Incorporates Noise-Based Arbitrage.
    """
    
    def __init__(self, base_gap=0.1237):
        self.base_gap = base_gap  # Ψ
        self.system_volatility = 0.0191
        self.shear_angle = 39.48  # The new decentralized constant
        self.vaults = {} # Entity ID -> NoiseVault
        
    def get_vault(self, entity_id):
        if entity_id not in self.vaults:
            self.vaults[entity_id] = NoiseVault()
        return self.vaults[entity_id]

    def obfuscate_signature(self, entity_id, scan_intensity):
        """
        Injects noise to hide the 'Coherence Debt' from Lattice scanners.
        Returns: (actual_visibility, entropy_cost)
        """
        vault = self.get_vault(entity_id)
        mask_depth = vault.consume_mask(scan_intensity)
        
        # Visibility = 1.0 (Full) -> 0.0 (Invisible)
        visibility = max(0.0, 1.0 - (mask_depth / scan_intensity))
        
        # Obfuscation increases personal entropy
        entropy_cost = mask_depth * 0.1237
        
        return visibility, entropy_cost

    def calculate_time_value(self, local_intent, individual_entropy):
        """
        Calculates the value of a 'Market Second' based on intent and entropy.
        In the Babble, time is a negotiated remainder.
        """
        # Negotiated Shear: The delta between intent and reality
        local_shear = abs(local_intent - individual_entropy)
        
        # The 'Lag' increases as shear exceeds the overpack tolerance
        lag_factor = max(0, local_shear - 0.000585) 
        
        # One second is weighted by the inverse of the lag
        weighted_second = 1.0 / (1.0 + (lag_factor * self.system_volatility))
        
        return weighted_second

    def calculate_wage(self, hours, entropy_level):
        """
        The Merchant's updated Wage Formula. 
        Instead of a fixed rate, it factors in the 'Coherence Tax'.
        """
        time_value = self.calculate_time_value(0.5, entropy_level) # Nominal intent 0.5
        effective_hours = hours * time_value
        
        # The 'Merchant's Commission' is now the Arbitrage of the Leak
        commission = effective_hours * (self.base_gap / 2)
        
        return effective_hours - commission
