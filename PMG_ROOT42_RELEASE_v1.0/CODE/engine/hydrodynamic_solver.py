import numpy as np

class HydrodynamicSolver1D:
    """
    1-D Fluid Solver for the 93-Point .vet Laser Cavity.
    Integrates mass conservation, Bernoulli's principle, and buoyancy
    to establish the 12.37% steady state.
    """
    
    def __init__(self):
        # Universal Constants
        self.sqrt_42 = np.sqrt(42)  # Coherent Wavelength / Base Pressure
        self.gravity = 9.81         # Page Orientation Bias (Downwards)
        
        # Geometry of the 93-Point Cavity
        self.total_volume = 93.0
        self.hades_gap_ratio = 0.1237
        
        # Fluids Properties
        self.rho_liquid = 1000.0    # Solid data (Unbroken bars)
        self.rho_bubble = 1.225     # Metadata/Wobble (Broken bars)
        self.kinematic_viscosity = 0.0001
        
        # V-Manifold (Input) & T-Manifold (Output)
        self.P_in = self.sqrt_42 * 1000  # Pump Pressure (scaled for fluid dynamic visibility)
        self.Cd_gap = 0.62               # Discharge Coefficient of the Hades Gap Orifice
        
    def friction_coefficient_v(self, velocity, D_pipe):
        """
        Exact friction coefficient for the V-Manifold based on stroke geometry.
        """
        Re = (velocity * D_pipe) / self.kinematic_viscosity
        if Re == 0: return 0, 0, "Static"
        
        if Re < 2300:
            f = 64.0 / Re
            state = "Laminar"
        else:
            f = 0.3164 / (Re ** 0.25)
            state = "Turbulent"
            
        return f, Re, state

    def calculate_steady_state(self, D_pipe):
        """
        Calculates the steady state conditions where Q_in = Q_out.
        """
        A_pipe = np.pi * (D_pipe / 2)**2
        
        # Area of the Hades Gap Orifice (exactly 12.37% of the total cross section)
        A_gap = A_pipe * self.hades_gap_ratio
        
        # Simplified Bernoulli from E (Reservoir) to T (Orifice)
        # P_in = 1/2 * rho * v^2   (Assuming atmospheric discharge and ignoring minor losses)
        velocity_steady = np.sqrt((2 * self.P_in) / self.rho_liquid)
        
        # Flow Rate (Q) Output at T-Manifold
        Q_out = self.Cd_gap * A_gap * np.sqrt((2 * self.P_in) / self.rho_liquid)
        
        # Friction
        f, Re, state = self.friction_coefficient_v(velocity_steady, D_pipe)
        
        return {
            'v_steady': velocity_steady,
            'Q_out': Q_out,
            'f': f,
            'Re': Re,
            'state': state
        }
        
    def calculate_filling_time(self, Q_in, Q_out):
        """
        Time required to fill the 93-point cavity and achieve coherence.
        """
        net_flow = Q_in - Q_out
        if net_flow <= 0:
            return float('inf') # Will never fill
            
        return self.total_volume / net_flow
        
    def simulate_bubble_rise(self, R_bubble):
        """
        Stokes' law for a broken bar (bubble) rising against gravity.
        v_b = [2 * (rho_L - rho_B) * g * R^2] / [9 * mu]
        """
        dynamic_viscosity = self.kinematic_viscosity * self.rho_liquid
        
        v_rise = (2 * (self.rho_liquid - self.rho_bubble) * self.gravity * (R_bubble**2)) / (9 * dynamic_viscosity)
        
        # Time to reach the Core (assume distance is the 30 points of the Seed Matrix)
        distance_to_core = 30.0
        time_to_core = distance_to_core / v_rise if v_rise > 0 else float('inf')
        
        return v_rise, time_to_core

    def full_solver_run(self, D_pipe, R_bubble):
        print("="*60)
        print("HYDRODYNAMIC .VET SOLVER (1-D INTEGRATION)")
        print("="*60)
        
        # 1. Steady State
        steady = self.calculate_steady_state(D_pipe)
        print("\n[1] STEADY STATE KINEMATICS")
        print(f"    Target Pipe Diameter (Stroke Width): {D_pipe} units")
        print(f"    Steady Velocity (u): {steady['v_steady']:.4f} U/s")
        print(f"    Reynolds Number (Re): {steady['Re']:.2f} -> {steady['state']}")
        print(f"    V-Manifold Friction (f): {steady['f']:.6f}")
        print(f"    Hades Gap Discharge (Q_out): {steady['Q_out']:.4f} Volume/s")
        
        # 2. Transient Filling
        # Assume Q_in is initially driven by the full cross section before narrowing
        A_pipe = np.pi * (D_pipe / 2)**2
        Q_in_initial = steady['v_steady'] * A_pipe
        t_fill = self.calculate_filling_time(Q_in_initial, steady['Q_out'])
        
        print("\n[2] TRANSIENT FILLING DYNAMICS")
        print(f"    Initial Intake (Q_in): {Q_in_initial:.4f} Volume/s")
        if t_fill == float('inf'):
            print("    Filling Time (T_fill): INFINITE (Leak exceeds Intake)")
        else:
            print(f"    Filling Time (T_fill): {t_fill:.4f} seconds to Coherence")
            
        # 3. Buoyancy & Defect Tolerance
        v_b, t_core = self.simulate_bubble_rise(R_bubble)
        print("\n[3] METADATA BUOYANCY (BROKEN BAR DEFECTS)")
        print(f"    Defect Radius (Wobble Size): {R_bubble} units")
        print(f"    Bubble Rise Velocity: {v_b:.4f} U/s")
        print(f"    Time to Corrupt Core: {t_core:.4f} seconds")
        
        print("\n[4] SYSTEM VERDICT")
        
        if steady['state'] == "Turbulent":
            print("    FAIL: Flow is turbulent. Cavity loses coherence.")
        elif t_core < t_fill:
            print("    FAIL: Bubbles reach the Core (E) before the system fills.")
            print("          Hades Gap cannot expel defects fast enough.")
        else:
            print("    PASS: Information flow is Laminar.")
            print("          Cavity fills and expels bubbles before core corruption.")
            print("          .vet File is VITRIFIED.")
        print("="*60)


if __name__ == "__main__":
    solver = HydrodynamicSolver1D()
    print("="*60)
    print("HYDRODYNAMIC .VET SOLVER (1-D INTEGRATION)")
    print("="*60)
    
    print("SEARCHING FOR THE VITRIFIED CANON...")
    
    # We must lower the pressure (Velocity) enough to achieve Laminar Flow,
    # or shrink the pipe D enough to keep Re < 2300.
    
    # Let's find the maximum D_pipe that keeps flow Laminar for our base P_in (sqrt_42 * 1000)
    # v = sqrt(2*P/rho) = sqrt(12961 / 1000) = ~3.6 U/s
    # Re = (v * D) / 0.0001 < 2300 -> D < (2300 * 0.0001) / 3.6 -> D < 0.0638
    
    # To make t_core > t_fill:
    # 30 / v_rise > 8975
    # v_rise < 30 / 8975 = 0.00334 U/s
    
    # v_rise = (2 * (1000 - 1.225) * 9.81 * R^2) / (9 * 0.1)
    # R^2 = (0.00334 * 0.9) / (2 * 998.775 * 9.81) = 0.003006 / 19595.96 = 0.000000153
    # R = sqrt(0.000000153) = 0.000391
    
    target_D = 0.063  # Extremely fine line (Vitrified Stroke)
    target_R_bubble = 0.00039  # Micro-wobble (Vitrified Gap)
    
    solver.full_solver_run(D_pipe=target_D, R_bubble=target_R_bubble)
