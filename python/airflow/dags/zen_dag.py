"""
ZenCODE Dag
===========

Here be the first ZenCODE Dag.
"""
from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

def print_hello(text):
    return 'Hello {0} Zen!'.format(text)

dag = DAG('ZenHello', description='Simple tutorial DAG',
          schedule_interval='*/5 * * * *',
          start_date=datetime(2019, 8, 10), catchup=False)
dag.doc_md = __doc__

sleep_operation = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

hello = PythonOperator(task_id='hello_task',
                       python_callable=lambda: print_hello(""),
                       dag=dag)

hello_again = PythonOperator(task_id='hello_again_task',
                             python_callable=lambda: print_hello("again"),
                             dag=dag)

hello_again.set_upstream(sleep_operation)
sleep_operation.set_upstream(hello)
