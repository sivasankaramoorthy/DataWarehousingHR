def transform_data(data):
    
    try:
        
        data.rename(columns={
            'Departments ': 'Departments',
            'average_montly_hours': 'average_monthly_hours',
            'left': 'has_left'  
        }, inplace=True)

        
        dim_department = data[['Departments']].drop_duplicates().reset_index(drop=True)
        dim_department['department_id'] = dim_department.index + 1

        
        dim_salary = data[['salary']].drop_duplicates().reset_index(drop=True)
        dim_salary.columns = ['salary_level']
        dim_salary['salary_id'] = dim_salary.index + 1

        
        dim_employee = data[['Work_accident', 'promotion_last_5years']].drop_duplicates().reset_index(drop=True)
        dim_employee['employee_id'] = dim_employee.index + 1

        
        fact_employee_churn = data.merge(dim_department, how='left', on='Departments') \
            .merge(dim_salary, how='left', left_on='salary', right_on='salary_level') \
            .merge(dim_employee, how='left', on=['Work_accident', 'promotion_last_5years'])

        
        fact_employee_churn = fact_employee_churn[[
            'employee_id', 'satisfaction_level', 'last_evaluation', 'number_project',
            'average_monthly_hours', 'time_spend_company', 'department_id', 'salary_id', 'has_left'
        ]]

        print("Data transformed successfully.")
        return {
            'fact_employee_churn': fact_employee_churn,
            'dim_department': dim_department,
            'dim_salary': dim_salary,
            'dim_employee': dim_employee
        }
    except Exception as e:
        print(f"Error in transforming data: {e}")
        raise
