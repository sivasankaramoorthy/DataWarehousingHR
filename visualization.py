import psycopg2
import pandas as pd
import matplotlib.pyplot as plt


def create_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",       
            port="5432",       
            database="hr", 
            user="postgres",       
            password="***" 
        )
        return connection
    except Exception as error:
        print(f"Error: Unable to connect to the database. {error}")
        return None


def execute_query(query):
    connection = create_connection()
    if connection is None:
        return None

    try:
        
        df = pd.read_sql_query(query, connection)
        
        
        print("Columns in DataFrame:", df.columns)
        
        return df
    except Exception as error:
        print(f"Error executing query: {error}")
        return None
    finally:
        connection.close()


def plot_churn_rate_by_department():
    query = """
    SELECT 
        dd."Departments" AS department,
        COUNT(CASE WHEN fec.has_left = 1 THEN 1 END) * 100.0 / COUNT(*) AS churn_rate
    FROM 
        fact_employee_churn fec
    JOIN 
        dim_department dd ON fec.department_id = dd.department_id
    GROUP BY 
        dd."Departments"
    ORDER BY 
        churn_rate DESC;
    """
    df = execute_query(query)
    if df is not None:
        df.plot(kind='bar', x='department', y='churn_rate', color='skyblue', legend=False)
        plt.title("Churn Rate by Department")
        plt.xlabel("Department")
        plt.ylabel("Churn Rate (%)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()


def plot_avg_satisfaction_by_department():
    query = """
    SELECT 
        dd."Departments" AS department,
        AVG(fec.satisfaction_level) AS avg_satisfaction_level
    FROM 
        fact_employee_churn fec
    JOIN 
        dim_department dd ON fec.department_id = dd.department_id
    GROUP BY 
        dd."Departments"
    ORDER BY 
        avg_satisfaction_level DESC;
    """
    df = execute_query(query)
    if df is not None:
        df.plot(kind='bar', x='department', y='avg_satisfaction_level', color='lightgreen', legend=False)
        plt.title("Average Satisfaction Level by Department")
        plt.xlabel("Department")
        plt.ylabel("Average Satisfaction Level")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()


def plot_top_churned_departments():
    query = """
    SELECT 
        dd."Departments" AS department,
        COUNT(CASE WHEN fec.has_left = 1 THEN 1 END) AS churned_employees
    FROM 
        fact_employee_churn fec
    JOIN 
        dim_department dd ON fec.department_id = dd.department_id
    GROUP BY 
        dd."Departments"
    ORDER BY 
        churned_employees DESC
    LIMIT 3;
    """
    df = execute_query(query)
    if df is not None:
        df.plot(kind='bar', x='department', y='churned_employees', color='coral', legend=False)
        plt.title("Top 3 Departments with Most Churned Employees")
        plt.xlabel("Department")
        plt.ylabel("Churned Employees")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()


def plot_avg_hours_satisfaction_by_salary():
    query = """
    SELECT 
        ds.salary_level AS salary_level,
        AVG(fec.average_monthly_hours) AS avg_monthly_hours,
        AVG(fec.satisfaction_level) AS avg_satisfaction_level
    FROM 
        fact_employee_churn fec
    JOIN 
        dim_salary ds ON fec.salary_id = ds.salary_id
    GROUP BY 
        ds.salary_level
    ORDER BY 
        avg_satisfaction_level DESC;
    """
    df = execute_query(query)
    if df is not None:
        fig, ax1 = plt.subplots()

        ax1.set_xlabel("Salary Level")
        ax1.set_ylabel("Average Monthly Hours", color='tab:blue')
        ax1.bar(df['salary_level'], df['avg_monthly_hours'], color='tab:blue', alpha=0.6, label="Avg Monthly Hours")
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.set_ylabel("Average Satisfaction Level", color='tab:green')
        ax2.plot(df['salary_level'], df['avg_satisfaction_level'], color='tab:green', marker='o', label="Avg Satisfaction Level")
        ax2.tick_params(axis='y', labelcolor='tab:green')

        plt.title("Average Monthly Hours and Satisfaction by Salary Level")
        plt.tight_layout()
        plt.show()


def plot_churn_rate_by_tenure():
    query = """
    SELECT 
        fec.time_spend_company AS years_spent,
        COUNT(CASE WHEN fec.has_left = 1 THEN 1 END) * 100.0 / COUNT(*) AS churn_rate
    FROM 
        fact_employee_churn fec
    GROUP BY 
        fec.time_spend_company
    ORDER BY 
        years_spent;
    """
    df = execute_query(query)
    if df is not None:
        df.plot(kind='line', x='years_spent', y='churn_rate', marker='o', color='purple')
        plt.title("Churn Rate by Time Spent at the Company")
        plt.xlabel("Years Spent at the Company")
        plt.ylabel("Churn Rate (%)")
        plt.tight_layout()
        plt.show()


def main():
    plot_churn_rate_by_department()
    plot_avg_satisfaction_by_department()
    plot_top_churned_departments()
    plot_avg_hours_satisfaction_by_salary()
    plot_churn_rate_by_tenure()

if __name__ == "__main__":
    main()
