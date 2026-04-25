import pandas as pd
import os

def prepare_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(base_dir, 'dataset.csv')
    file2 = os.path.join(base_dir, 'dataset_expanded.csv')
    
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Merge datasets
    df = pd.concat([df1, df2], ignore_index=True)
    
    # Ensure lowercase labels
    df['label'] = df['label'].str.strip().str.lower()
    
    # Fruits and non-veg/grain crops to exclude from main training set
    fruits_to_exclude = [
        'papaya', 'orange', 'apple', 'muskmelon', 'watermelon', 
        'grapes', 'mangoes', 'banana', 'pomegranate', 'coconut', 'coffee'
    ]
    
    # Filter out excluded fruits
    df_filtered = df[~df['label'].isin(fruits_to_exclude)]
    
    # Drop duplicates
    df_filtered = df_filtered.drop_duplicates()
    
    out_file = os.path.join(base_dir, 'dataset_mixed.csv')
    df_filtered.to_csv(out_file, index=False)
    print(f"Original merged shape: {df.shape}")
    print(f"Filtered, distinct shape: {df_filtered.shape}")
    print(f"Saved merged dataset to {out_file}")
    
    print("Remaining crops:", sorted(df_filtered['label'].unique()))

if __name__ == "__main__":
    prepare_data()
