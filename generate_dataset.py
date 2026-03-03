import pandas as pd
import random

def generate_dataset(samples_per_device=500):
    data = []
    
    devices = ['Motor', 'Fan', 'Bulb']
    
    for _ in range(samples_per_device):
        # --- MOTOR CATEGORY ---
        data.append({
            'device_type': 'Motor',
            'voltage_v': round(random.uniform(0.0, 120.0), 2),
            'current_a': round(random.uniform(0.8, 2.0), 2),
            'temp_c': round(random.uniform(25.0, 95.0), 2),
            'vibration_g': round(random.uniform(0.2, 5.0), 2)
        })
        
        # --- FAN CATEGORY ---
        data.append({
            'device_type': 'Fan',
            'voltage_v': round(random.uniform(0.0, 24.0), 2),
            'current_a': round(random.uniform(0.0, 1.5), 2),
            'temp_c': round(random.uniform(20.0, 60.0), 2),
            'vibration_g': round(random.uniform(0.1, 2.5), 2)
        })
        
        # --- BULB CATEGORY ---
        data.append({
            'device_type': 'Bulb',
            'voltage_v': round(random.uniform(0.0, 12.0), 2),
            'current_a': round(random.uniform(0.3, 0.6), 2),
            'temp_c': round(random.uniform(25.0, 120.0), 2),
            'vibration_g': round(random.uniform(0.0, 0.02), 2) # Near zero for bulbs
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Shuffle the dataset so the ML model doesn't learn based on the order of devices
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Export to CSV
    df.to_csv('sensors_dataset_training.csv', index=False)
    print(f"Successfully generated dataset with {len(df)} rows.")

if __name__ == "__main__":
    generate_dataset()