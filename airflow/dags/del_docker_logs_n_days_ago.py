# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 17:34:49 2022

@author: chenq
"""

from airflow import DAG
from datetime import timedelta,datetime
#from airflow.utils.dates import days_ago
#from airflow.operators.bash_operator import BashOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
#from airflow.operators.dummy import DummyOperator
#from airflow.operators.generic_transfer import GenericTransfer

args = {
    'owner': 'chq',
    'depends_on_past': False,
    'start_date': datetime(2022,8,22,0,0,0),
#    'start_date': days_ago(1),
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
    "queue": 'default',
}

dag = DAG(
    dag_id='del_docker_logs_n_days_ago',
    default_args=args,
    catchup=False,
    schedule_interval='23 0 */1 * *',
    dagrun_timeout=timedelta(minutes=10),
    tags=['product']
)

delsql01="""
delete from celery_taskmeta where date_done<CURRENT_DATE - interval '3 day';
"""

delsql02="""
delete from dag_run where end_date<CURRENT_DATE - interval '3 day';
"""

delsql03="""
delete from job where end_date<CURRENT_DATE - interval '3 day';
"""

delsql04="""
delete from log where execution_date<CURRENT_DATE - interval '3 day';
"""

delsql05="""
delete from task_instance where end_date<CURRENT_DATE - interval '3 day';
"""

del_task_logs = BashOperator(
    task_id='del_task_logs',
    trigger_rule="all_done",
    bash_command="find /opt/airflow/logs -mtime +10 | xargs rm -rf",
    dag=dag,
)

celery_taskmeta_d = PostgresOperator(
    task_id='celery_taskmeta_d',
    sql=delsql01,
    trigger_rule="all_done",
    postgres_conn_id='local_airflow_meta',
    database='airflow',
    dag=dag
)

dag_run_d = PostgresOperator(
    task_id='dag_run_d',
    sql=delsql02,
    trigger_rule="all_done",
    postgres_conn_id='local_airflow_meta',
    database='airflow',
    dag=dag
)

job_d = PostgresOperator(
    task_id='job_d',
    sql=delsql03,
    trigger_rule="all_done",
    postgres_conn_id='local_airflow_meta',
    database='airflow',
    dag=dag
)

log_d = PostgresOperator(
    task_id='log_d',
    sql=delsql04,
    trigger_rule="all_done",
    postgres_conn_id='local_airflow_meta',
    database='airflow',
    dag=dag
)

task_instance_d = PostgresOperator(
    task_id='task_instance_d',
    sql=delsql05,
    trigger_rule="all_done",
    postgres_conn_id='local_airflow_meta',
    database='airflow',
    dag=dag
)

# [FORM DAG JOB]
del_task_logs >> celery_taskmeta_d >> dag_run_d >> job_d >> log_d >> task_instance_d
