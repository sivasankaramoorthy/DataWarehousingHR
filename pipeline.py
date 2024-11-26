from extract import extract_data
from transform import transform_data
from load import load_data


CSV_FILE_PATH = "HR_Dataset.csv"
DB_URL = "postgresql://postgres:***@localhost:5432/hr"

def etl_pipeline():
    
    try:

        data = extract_data(CSV_FILE_PATH)

        transformed_data = transform_data(data)


        load_data(transformed_data, DB_URL)

        print("ETL pipeline completed successfully.")
    except Exception as e:
        print(f"ETL pipeline failed: {e}")

if __name__ == "__main__":
    etl_pipeline()



