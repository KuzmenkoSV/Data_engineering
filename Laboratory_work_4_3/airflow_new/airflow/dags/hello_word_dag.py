from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'KuzmenkoSV',
    'start_date': days_ago(1),
}


with DAG(
    dag_id='hello_world',
    default_args=default_args,
    max_active_runs=1,
    catchup=False
) as dag:

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')
    task = BashOperator(task_id='hello_world', bash_command='echo hello world!')

    start >> task >> end