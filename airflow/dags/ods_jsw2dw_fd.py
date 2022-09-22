# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from airflow.models import DAG
from datetime import timedelta,datetime
from airflow.utils.dates import days_ago
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
#from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

s = SSHHook(
    # ssh_conn_id='ssid',
    remote_host='datax',
    username='root',
    password='zuY4Pai#',
    # key_file='',
    port=22
)

args = {
    'owner': 'dc',
    'depends_on_past': False,
    'start_date': datetime(2022,7,18,0,0,0),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    "queue": 'default',
    # "priority_weight": 10,
}

dag = DAG(
    dag_id='ods_jsw2dw_fd',
    default_args=args,
    catchup=False,
    schedule_interval='11 3 * * *',
    dagrun_timeout=timedelta(minutes=180),
    tags=['product']
)

run_this_last = DummyOperator(
    task_id='run_this_last',
    dag=dag,
)

# [START howto_operator_bash]
sync = SSHOperator(
    task_id='tbl_sync',
    ssh_hook=s,
    trigger_rule="all_done",
    command="json_dir=/opt/datax/job/ods_jsw2dw_fd;for f in `ls $json_dir`;do python /opt/datax/bin/datax.py $json_dir/$f;done",
    dag=dag,
)

#sync01 = SSHOperator(
#    task_id='navigation_class',
#    ssh_hook=s,
#    trigger_rule="all_done",
#    command="python /opt/datax/bin/datax.py /opt/datax/job/opac-navigation_class.json",
#    dag=dag,
#)

# [END howto_operator_bash]
sync >> run_this_last
