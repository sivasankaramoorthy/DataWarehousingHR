import pandas as pd

def extract_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data extracted successfully.")
        return data
    except Exception as e:
        print(f"Error in extracting data: {e}")
        raise
