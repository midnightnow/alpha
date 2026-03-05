import sys
import os
import json
import time

# Add engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'CODE', 'engine'))

from veth_schema_5_12_13 import VethRecord, VethFieldType, VethHeader, SureFaceValidator

def generate_point_001():
    print("Initiating the First Roll. Generating point_001.veth...")
    
    # 1. Provide Real "Savage" Data (A Wellness Check)
    # The count (5) -> Identity, Timestamp, Observer, Species, Locus
    record = VethRecord()
    record.add_field(VethFieldType.IDENTITY, "CANINE-PATIENT-ALPHA-77")
    record.add_field(VethFieldType.TIMESTAMP, int(time.time()))
    record.add_field(VethFieldType.OBSERVER, "DR. SUN MAN")
    record.add_field(VethFieldType.SPECIES, "CANIS LUPUS FAMILIARIS")
    record.add_field(VethFieldType.LOCUS, "RAINBOW CABIN, HARRIS")
    
    # The measure (12) -> Weight through Consciousness
    record.add_field(VethFieldType.WEIGHT, 24) # 24 kg
    record.add_field(VethFieldType.HEART_RATE, 84) # 84 bpm (42 * 2)
    record.add_field(VethFieldType.TEMPERATURE, 37) # 37°C
    
    # 2. Shave and Vitrify
    # The record automatically handles creating the 93-bit header and enforcing integer fields
    
    # Let's inspect the header
    header_hex = f"0x{record.header.to_93_bits():024X}"
    print(f"93-Bit Solid Header Generated: {header_hex}")
    
    # Is it taut?
    validator = SureFaceValidator(record)
    hysteresis_data = validator.measure_hysteresis(record)
    hysteresis = hysteresis_data["hysteresis"]
    print(f"Initial Hysteresis: {hysteresis}°")
    
    # 3. Export to JSON (The .veth file)
    output_path = os.path.join(os.path.dirname(__file__), "point_001.veth")
    
    fc = record.field_count
    veth_data = {
        "header": {
            "hex": header_hex,
            "count": fc["COUNT"],
            "measure": fc["MEASURE"],
            "comm": fc["COMMUNICATION"]
        },
        "fields": {f.field_type.name: f.value for f in record.fields},
        "hysteresis": hysteresis,
        "is_taut": hysteresis == 0.0
    }
    
    with open(output_path, "w") as f:
        json.dump(veth_data, f, indent=4)
        
    print(f"VITRIFICATION COMPLETE. Saved to {output_path}")

if __name__ == "__main__":
    generate_point_001()
