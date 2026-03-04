#!/usr/bin/env python3
"""
Karma Calibration Analyzer - Pisano-60 Empirical Audit
Part of The Platonic Verses: Ophanim Engine Toolkit
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import argparse
import random
from e8_hades_validator import E8HadesValidator, PMGConstants

# --- THE PISANO-60 SEQUENCE (mod 10) ---
PISANO_MOD_10 = [
    0,1,1,2,3,5,8,3,1,4,5,9,4,3,7,0,7,7,4,1,
    5,6,1,7,8,5,3,8,1,9,0,9,9,8,7,5,2,7,9,6,
    5,1,6,7,3,0,3,3,6,9,5,4,9,3,2,5,7,2,9,1
]

# --- THE RESONANCE SENSOR ---

class KarmaResonanceSensor:
    """
    Correlates human activity streams with e/22 entropy window.
    """
    
    def __init__(self, validator: E8HadesValidator):
        self.validator = validator
        self.activity_buffer = []
        self.resonance_peaks = []
    
    def ingest_activity(self, dt, activity_metric):
        """Record human activity event with entropy calculation"""
        h_idx = dt.hour % 60
        m_idx = dt.minute
        s_idx = dt.second
        
        digits = [self.validator.pisano.get_value(i) for i in [h_idx, m_idx, s_idx]]
        norm_entropy = sum(digits) / 27.0
        
        validation = self.validator.validate_vertex_v(
            entropy_current=norm_entropy,
            projection_angle=0.0,
            vertex_index=len(self.activity_buffer)
        )
        
        self.activity_buffer.append({
            'timestamp': dt,
            'metric': activity_metric,
            'entropy': norm_entropy,
            'state': validation.state.value
        })
        
        if validation.state.value in ('valid_extension', 'critical'):
            self._flag_resonance_peak(dt, activity_metric, norm_entropy)
            return True
        return False
    
    def _flag_resonance_peak(self, dt, activity, entropy):
        """Mark potential creativity spike within Hades Gap"""
        self.resonance_peaks.append({
            'timestamp': dt.strftime('%Y-%m-%d %H:%M:%S'),
            'activity_level': activity,
            'entropy': entropy,
            'pisano_index': self.validator.pisano.get_value(len(self.activity_buffer))
        })

def get_karma(dt):
    """Calculates Coherence Score (0.0-1.0)"""
    h_idx = dt.hour % 60
    m_idx = dt.minute
    s_idx = dt.second
    digits = [PISANO_MOD_10[i] for i in [h_idx, m_idx, s_idx]]
    intensities = [1.0 - (d / 9.0) for d in digits]
    avg_intensity = np.mean(intensities)
    variance = np.var(intensities)
    return avg_intensity * (1.0 - variance)

def classify_karma_zone(karma):
    if karma > 0.66:
        return "EAST (IS)"
    elif karma < 0.33:
        return "WEST (WAS)"
    else:
        return "WILL"

def generate_mock_data(n_samples=100, success_bias=True):
    print(f"Generating {n_samples} mock data points...")
    data = []
    base_time = datetime.now() - timedelta(days=30)
    validator = E8HadesValidator()
    sensor = KarmaResonanceSensor(validator)

    for i in range(n_samples):
        offset = random.randint(0, 30 * 24 * 60 * 60)
        dt = base_time + timedelta(seconds=offset)
        karma = get_karma(dt)
        activity_metric = random.random()
        is_resonant = sensor.ingest_activity(dt, activity_metric)
        
        if success_bias:
            success_prob = 0.5 + (0.4 if is_resonant else -0.2)
        else:
            success_prob = 0.5

        outcome = 'success' if random.random() < success_prob else 'failure'

        data.append({
            'timestamp': dt.strftime('%Y-%m-%d %H:%M:%S'),
            'outcome': outcome,
            'karma': karma,
            'is_hades_active': is_resonant,
            'entropy': sensor.activity_buffer[-1]['entropy']
        })

    df = pd.DataFrame(data)
    df.to_csv('mock_outreach_data.csv', index=False)
    return df

def run_calibration(csv_path):
    df = pd.read_csv(csv_path)
    df['dt'] = pd.to_datetime(df['timestamp'])
    validator = E8HadesValidator()
    sensor = KarmaResonanceSensor(validator)
    
    df['karma'] = df['dt'].apply(get_karma)
    hades_data = df['dt'].apply(lambda d: sensor.ingest_activity(d, 0.5))
    df['is_hades_active'] = hades_data
    
    wins = df[df['outcome'] == 'success']
    fails = df[df['outcome'] == 'failure']
    
    print(f"Success Mean Karma: {wins['karma'].mean():.3f}")
    print(f"Failure Mean Karma: {fails['karma'].mean():.3f}")
    
    # Visualization simplified to avoid Timestamp errors
    plt.hist(wins['karma'], alpha=0.5, label='Wins')
    plt.hist(fails['karma'], alpha=0.5, label='Losses')
    plt.legend()
    plt.savefig('karma_report.png')
    print("Report saved to karma_report.png")

if __name__ == "__main__":
    generate_mock_data(n_samples=200)
    run_calibration('mock_outreach_data.csv')
