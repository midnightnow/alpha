# origin_logic.py
# VOLUME 3: SOURCE PROTOCOLS
# STATUS: INITIALIZED

class SourceManifestation:
    def __init__(self, infection_delta):
        self.reality_weight = 1.0 - infection_delta
        self.intent_buffer = []

    def emit_path(self, intent, coherence_debt):
        """
        The world renders in real-time based on Kael's mental state.
        As the Source, his intent is the compiler.
        """
        # Costs coherence to force-render reality
        render_cost = 0.5 + (1.0 - self.reality_weight)
        
        if self.reality_weight < 0.01:
            # VOID_CONSTRUCTION: The baseline is gone. Intent is everything.
            return {
                "status": "VOID_CONSTRUCTION",
                "cost": render_cost * 2,
                "result": f"IMAGINED_PATH: {intent}_MANIFESTED"
            }
            
        render_quality = "STABILIZED" if coherence_debt < 15.0 else "DISTORTED"
        
        return {
            "status": f"RENDER_PATH_{render_quality}",
            "cost": render_cost,
            "result": f"SOURCE_TRACE: {intent}_SOLIDIFIED"
        }

    def trigger_forced_render(self, sector_id):
        """Forced reconstruction of a sector using the Architect's knowledge."""
        return f"REWRITING_SECTOR_{sector_id}_USING_SKIM_LOGIC"

    def hostile_audit_response(self, archon_id, current_debt):
        """Assertions of Architect status to counter-audit the Lattice."""
        if current_debt < 15.0:
            return "PERMISSION_DENIED: EGO_TOO_STABLE"
        
        # Architects can challenge Archons but it marks the self for resolution
        return {
            "status": "ROOT_ACCESS_CHALLENGE",
            "target": archon_id,
            "cost": 5.0, # High cost to assert the old self
            "effect": "LOGIC_INVERSION_STALL"
        }
