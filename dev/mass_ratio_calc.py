# Mass Ratio Calculations

vol_total = 2600000
vol_granite_values = [6000, 7000, 8000]

density_limestone = 2500 # kg/m^3
density_granite = 2750 # kg/m^3

print("Carbon to Silicon Mass Ratio Calculations")
print("-" * 50)
for vol_granite in vol_granite_values:
    vol_limestone = vol_total - vol_granite
    mass_limestone = vol_limestone * density_limestone
    mass_granite = vol_granite * density_granite
    
    mass_ratio = mass_limestone / mass_granite
    volume_ratio = vol_limestone / vol_granite
    
    print(f"Granite Volume: {vol_granite} m^3")
    print(f"Limestone Volume: {vol_limestone} m^3")
    print(f"Volume Ratio (Limestone:Granite): {volume_ratio:.2f}")
    print(f"Mass Ratio (Limestone:Granite): {mass_ratio:.2f}")
    print(f"Relationship to 432: 432 / Mass Ratio = {432 / mass_ratio:.4f}")
    print(f"Relationship to 7/11 (0.636 / 1.571): Mass Ratio / 324 = {mass_ratio / 324:.4f}")
    print("-" * 50)
