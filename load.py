from sqlalchemy import create_engine

def load_data(tables, db_url):
   
    try:
        engine = create_engine(db_url)
        for table_name, data in tables.items():
            data.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Loaded table {table_name} successfully.")
    except Exception as e:
        print(f"Error in loading data: {e}")
        raise
