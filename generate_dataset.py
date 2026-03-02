import pandas as pd
import numpy as np

def generate_motor_data(samples=500):
    np.random.seed(42)
    
    
    normal_samples = int(samples * 0.7)
    df_normal = pd.DataFrame({
        'current': np.random.normal(2.5, 0.2, normal_samples),      
        'vibration': np.random.normal(0.05, 0.01, normal_samples),  
        'temp': np.random.normal(40, 2, normal_samples),            
        'target': 0  
    })

    
    
    fail_vib_samples = int(samples * 0.15)
    df_vib = pd.DataFrame({
        'current': np.random.normal(2.8, 0.3, fail_vib_samples), 
        'vibration': np.random.normal(0.8, 0.15, fail_vib_samples), 
        'temp': np.random.normal(55, 5, fail_vib_samples),          
        'target': 1  
    })

    
    
    fail_load_samples = int(samples * 0.15)
    df_load = pd.DataFrame({
        'current': np.random.normal(9.5, 1.0, fail_load_samples),   
        'vibration': np.random.normal(0.1, 0.05, fail_load_samples),
        'temp': np.random.normal(85, 8, fail_load_samples),         
        'target': 1  
    })

    
    dataset = pd.concat([df_normal, df_vib, df_load]).sample(frac=1).reset_index(drop=True)
    dataset.to_csv('sensor_training_data.csv', index=False)
    print("Dataset generated: sensor_training_data.csv")

generate_motor_data()