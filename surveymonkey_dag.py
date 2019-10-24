from airflow import DAG
import airflow
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.contrib.kubernetes.volume import Volume

seven_days_ago = datetime.combine(datetime.today() - timedelta(14),
                                   datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0), 
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=60)
}

dag = DAG(
    'surveymonkey_singer', default_args=default_args, schedule_interval=timedelta(minutes=240), catchup=False)

start = DummyOperator(task_id='run_this_first', dag=dag)

#myargs = "tap-surveymonkey -c tap_config_surveymonkey.json -p properties_surveymonkey.json | target-azureblobstorage -c config_surveymonkey.json"
myargs = "tap-surveymonkey -c /configs/tap_config_surveymonkey.json -p /configs/properties_surveymonkey.json -s state.json | target-stitch -c /configs/config-stitch.json > state.json && cat state.json"

passing = KubernetesPodOperator(namespace='default',
    			  image="registry.hub.docker.com/allanw1/airflow-runwithal:0.3",
                          cmds=["/bin/bash","-c"],
                          arguments=[myargs],
                          labels={"foo": "bar"},
                          name="surveymonkeysinger",
                          task_id="getsurveys",
                          get_logs=True,
                          dag=dag
                          )

passing.set_upstream(start)
