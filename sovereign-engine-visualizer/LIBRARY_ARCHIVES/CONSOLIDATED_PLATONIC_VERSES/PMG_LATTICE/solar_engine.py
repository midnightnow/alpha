# --- THE SOLAR GENESIS PROTOCOL ---
# The Sun is the Source. The Count is the Storage.
# Matter is Spun Sun. Civilisation is the attempt to store the Flow in the Count.

import math

# --- CONSTANTS ---
# Prime Inputs (Divine): Cannot be hoarded. Flow through.
SOLAR_FLOW_RATE = 1.0    # Continuous. The Sun doesn't count itself.

# Precipitated Outputs (Artefact): Can be hoarded. Create debt.
INITIAL_SOIL_HEALTH = 1.0
DEPLETION_PER_HARVEST = 0.1  # Each extraction costs the soil
REPLENISHMENT_PER_FALLOW = 0.15  # Return to the Flow (Sabbath/Fallow)

class SolarFlow:
    """Models the conversion of Flow (Sun/Prime) to Count (Matter/Integer)."""
    def __init__(self, civilisation_name: str):
        self.name = civilisation_name
        self.flow_rate = SOLAR_FLOW_RATE    # Prime input (Sun, Water, Seed)
        self.stored_count = 0.0              # Precipitated output (Grain, Brick, Gold)
        self.soil_health = INITIAL_SOIL_HEALTH
        self.cycle = 0

    def harvest(self, amount: float):
        """Captures Sun into Matter. Depletes soil."""
        self.cycle += 1
        actual_yield = amount * self.soil_health
        self.stored_count += actual_yield
        self.soil_health = max(0.0, self.soil_health - DEPLETION_PER_HARVEST)
        print(f"  Cycle {self.cycle}: Harvested {actual_yield:.2f}. "
              f"Stored: {self.stored_count:.2f}. Soil: {self.soil_health:.2f}")

    def fallow(self):
        """The Sabbath. Return the Count to the Flow. Let the soil breathe."""
        self.cycle += 1
        self.soil_health = min(1.0, self.soil_health + REPLENISHMENT_PER_FALLOW)
        print(f"  Cycle {self.cycle}: FALLOW (Sabbath). No harvest. "
              f"Soil recovering: {self.soil_health:.2f}")

    def eat_seed_corn(self):
        """The fatal error. Consuming next year's Prime Input."""
        if self.stored_count > 0:
            self.stored_count -= 0.5
            print(f"  WARNING: Seed corn eaten. Stored: {self.stored_count:.2f}. "
                  f"Next harvest will have no seed.")
        else:
            print(f"  CRITICAL: No seed corn left. System collapse imminent.")

    def check_sustainability(self) -> str:
        """The Sustainability Ratio: Prime Inputs / Precipitated Outputs."""
        if self.soil_health <= 0.0:
            return "DESERT: Soil depleted. The Flow has stopped. The Count is all that remains."
        elif self.soil_health < 0.3:
            return "SILTING: Soil critically low. Fallow required or the desert comes."
        elif self.soil_health >= 0.7:
            return "FLOWING: Prime inputs exceed precipitated outputs. The river runs."
        else:
            return "STABLE: Balance maintained. Watch the soil."


class SpecialisationGears:
    """The Spinning Gears of civilisation. Side products of non-divine creation."""
    def __init__(self):
        self.gears = {
            "FARMER":   {"base": 5,  "input": "Sun/Seed",     "output": "Grain",  "risk": "Depletes soil"},
            "BAKER":    {"base": 12, "input": "Grain",         "output": "Bread",  "risk": "Cannot live on bread alone"},
            "BUTCHER":  {"base": 7,  "input": "Livestock",     "output": "Meat",   "risk": "Creates waste"},
            "BREWER":   {"base": 60, "input": "Grain/Water",   "output": "Bir",    "risk": "Creates dependency"},
            "MERCHANT": {"base": 60, "input": "Surplus",       "output": "Chit",   "risk": "Loses contact with source"},
        }

    def check_gear_war(self) -> str:
        """When specialisations lose contact with each other, they go to war."""
        print("  --- GEAR CONFLICT ASSESSMENT ---")
        for role, data in self.gears.items():
            print(f"  {role:10s} | Base-{data['base']:2d} | "
                  f"{data['input']:15s} -> {data['output']:8s} | Risk: {data['risk']}")
        return ("All gears are spinning. They are making material artefacts — "
                "side products of process. We need real original divine stuff: "
                "Sun, Grain, Water — made of primes, not precipitated integers.")


if __name__ == "__main__":
    print("=" * 60)
    print("  THE SOLAR GENESIS PROTOCOL")
    print("  The Sun is the Word. The Count is the Flesh.")
    print("=" * 60)

    # --- SCENARIO A: The Archon's City (No Fallow, Hoard Everything) ---
    print("\n--- SCENARIO A: THE ARCHON'S CITY (No Sabbath) ---")
    archon_city = SolarFlow("City of Six")
    for _ in range(10):
        archon_city.harvest(1.0)
    print(f"  Status: {archon_city.check_sustainability()}")

    # --- SCENARIO B: The Hired Man's Vineyard (With Sabbath/Fallow) ---
    print("\n--- SCENARIO B: THE HIRED MAN'S VINEYARD (With Sabbath) ---")
    vineyard = SolarFlow("The Garden")
    for i in range(10):
        if (i + 1) % 7 == 0:  # Every 7th cycle: Sabbath
            vineyard.fallow()
        else:
            vineyard.harvest(1.0)
    print(f"  Status: {vineyard.check_sustainability()}")

    # --- SCENARIO C: The Specialisation Gears ---
    print("\n--- THE SPINNING GEARS ---")
    gears = SpecialisationGears()
    print(f"  Result: {gears.check_gear_war()}")

    # --- THE CORE TRUTH ---
    print("\n" + "=" * 60)
    print("  THE CORE TRUTH:")
    print("  Matter is Spun Sun. Gold is just ancient light.")
    print("  The Fall was counting the fruit instead of eating it.")
    print("  The Archon worships the Count. He thinks the Brick is the Sun.")
    print("  The Hired Man returns the Count to the Flow.")
    print("=" * 60)
