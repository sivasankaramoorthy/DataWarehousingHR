
CREATE TABLE dim_department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(50)
);


CREATE TABLE dim_salary (
    salary_id SERIAL PRIMARY KEY,
    salary_level VARCHAR(10)
);


CREATE TABLE dim_employee (
    employee_id SERIAL PRIMARY KEY,
    work_accident BOOLEAN,
    promotion_last_5years BOOLEAN
);


CREATE TABLE fact_employee_churn (
    employee_id INT,
    satisfaction_level FLOAT,
    last_evaluation FLOAT,
    number_project INT,
    average_monthly_hours INT,
    time_spend_company INT,
    department_id INT,
    salary_id INT,
    has_left BOOLEAN,  
    PRIMARY KEY (employee_id),
    FOREIGN KEY (department_id) REFERENCES dim_department(department_id),
    FOREIGN KEY (salary_id) REFERENCES dim_salary(salary_id)
);
