import numpy as np
import matplotlib.pyplot as plt

class VetRiskDashboard:
    """
    Visualizes the Safety Envelope for the Primordial 7 .vet Files.
    Maps constants to Risk Levels based on the Hydrodynamic Canon.
    """
    def __init__(self):
        # Canonical Constants (Vitrified)
        self.constants = {
            'Identity': {'value': 3, 'unit': 'Points', 'critical': True, 'tolerance': 0.0},
            'Time': {'value': 8975, 'unit': 'Seconds', 'critical': True, 'tolerance': 0.01},
            'Space': {'value': 51, 'unit': 'Root Boundary', 'critical': False, 'tolerance': 0.05},
            'Species': {'value': 60, 'unit': 'Points (10-24-26)', 'critical': False, 'tolerance': 0.10},
            'Anatomy': {'value': 93, 'unit': 'Total Points', 'critical': False, 'tolerance': 0.0},
            'Pathology': {'value': 0.00039, 'unit': 'Bubble Radius', 'critical': True, 'tolerance': 0.00001},
            'Vitrification': {'value': 0.063, 'unit': 'Stroke Width', 'critical': True, 'tolerance': 0.001}
        }
        
        # Risk Colors
        self.colors = {
            'Safe': '#00FF00',       # Green
            'Caution': '#FFFF00',    # Yellow
            'Critical': '#FF0000'    # Red
        }

    def calculate_risk(self, name, params):
        """
        Determines risk level based on tolerance and criticality.
        """
        if params['critical']:
            return 'Critical'
        elif params['tolerance'] > 0.05:
            return 'Safe'
        else:
            return 'Caution'

    def plot_dashboard(self):
        """
        Generates the Visual Risk Map.
        """
        names = list(self.constants.keys())
        values = [self.constants[n]['value'] for n in names]
        risks = [self.calculate_risk(n, self.constants[n]) for n in names]
        risk_colors = [self.colors[r] for r in risks]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(names, values, color=risk_colors, edgecolor='black', linewidth=1.5)
        
        # Add annotations
        for i, (name, params) in enumerate(self.constants.items()):
            risk_level = self.calculate_risk(name, params)
            ax.text(i, values[i] + (max(values)*0.05), 
                    f"{params['value']}\n({risk_level})", 
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_title('PRIMORDIAL 7: RISK MAP & SAFETY ENVELOPE', fontsize=14, fontweight='bold')
        ax.set_ylabel('Canonical Value (Units)', fontsize=12)
        ax.set_xlabel('Primordial File', fontsize=12)
        ax.axhline(y=0, color='black', linewidth=1)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=self.colors['Safe'], label='Safe Fluctuation (Species/Space)'),
                           Patch(facecolor=self.colors['Caution'], label='Caution (Anatomy)'),
                           Patch(facecolor=self.colors['Critical'], label='Critical Path (Identity/Time/Path/Vit)')]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        plt.savefig('/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine/risk_map.png')
        print("Safety Envelope Snapshot Saved to risk_map.png")
        plt.close()
        
        # Print Safety Report
        print("\n" + "="*60)
        print("SAFETY PROTOCOL REPORT")
        print("="*60)
        critical_files = [n for n, p in self.constants.items() if p['critical']]
        print(f"CRITICAL PATH FILES ({len(critical_files)}): {', '.join(critical_files)}")
        print("ACTION: DO NOT MODIFY WITHOUT HYDRODYNAMIC SOLVER VALIDATION.")
        print("="*60 + "\n")

if __name__ == "__main__":
    dashboard = VetRiskDashboard()
    dashboard.plot_dashboard()
