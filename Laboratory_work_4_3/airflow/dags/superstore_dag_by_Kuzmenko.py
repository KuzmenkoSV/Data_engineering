from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'KuzmenkoSV',
    'start_date': days_ago(1),
}

def data_prep():
    import psycopg2
    import pandas as pd

    try:
        # connect to exist database
        connection = psycopg2.connect(
            host="95.131.149.21",
            user="m_01",
            password="ie8smn",
            database="dep1"
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT o.order_id, order_date, ship_date, ship_mode
                          customer_id, customer_name, segment, country, city
                          state, postal_code, o.region, person, product_id, category, 
                          subcategory, product_name, sales, quantity, discount, 
                          profit, returned 
                   FROM orders o
                   LEFT JOIN people p on p.region = o.region
                   LEFT JOIN returns r on r.order_id = o.order_id
                   WHERE r.returned is null'''

            )
            result = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            df = pd.DataFrame(data=result, columns=field_names)
            df.to_csv(r'/opt/airflow/dags/output_superstore.csv', index=False)

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


with DAG(
    dag_id='Superstore_dataprep_kuzmenko',
    default_args=default_args,
    max_active_runs=1,
    catchup=False
) as dag:

    t1 = EmptyOperator(task_id='start')
    t3 = EmptyOperator(task_id='end')
    t2 = PythonOperator(task_id='data_prep_superstore', python_callable=data_prep)


    t1 >> t2 >> t3