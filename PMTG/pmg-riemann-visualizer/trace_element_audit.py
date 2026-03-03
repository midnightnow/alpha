import math

TOTAL_NODES = 93
DECAY_CONSTANT = 0.05

def simulate_decay():
    print("Initiating Trace Element Audit...")
    print(f"Lattice Size: {TOTAL_NODES} nodes")
    print(f"Decay Constant (λ): {DECAY_CONSTANT}")
    
    active_particles = TOTAL_NODES * 100
    time_steps = 50
    
    for t in range(time_steps):
        decayed = int(active_particles * (1 - math.exp(-DECAY_CONSTANT)))
        active_particles -= decayed
        if t % 10 == 0:
            print(f"T={t}: Active Particles = {active_particles}, Decayed = {decayed}")
            
    print("Audit Complete.")

if __name__ == "__main__":
    simulate_decay()
