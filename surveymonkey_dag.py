from airflow import DAG
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
    'start_date': seven_days_ago,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=60)
}

dag = DAG(
    'surveymonkey_singer', default_args=default_args, schedule_interval=timedelta(minutes=10))

start = DummyOperator(task_id='run_this_first', dag=dag)

volume_mount = VolumeMount('airflow-dags',
                            mount_path='/dags',
                            sub_path='dags',
                            read_only=True)

volume_config = {
    'persistentVolumeClaim':
        {
            'claimName': 'airflow-dags'
        }
}

volume = Volume(name='airflow-dags', configs=volume_config)
file_path = "/root/kubeconfig/kubeconfig"

#myargs = "tap-surveymonkey -c tap_config_surveymonkey.json -p properties_surveymonkey.json | target-azureblobstorage -c config_surveymonkey.json"
myargs = "tap-surveymonkey"

passing = KubernetesPodOperator(namespace='default',
    			  image="registry.hub.docker.com/allanw1/airflow-runwithal:0.1",
                          cmds=["/bin/bash", "-c"],
                          arguments=[myargs],
                          labels={"foo": "bar"},
                          name="surveymonkeysinger",
                          task_id="getsurveys",
                          volume_mounts=[volume_mount],
                          volumes=[volume],
                          get_logs=True,
                          in_cluster=True,
                          dag=dag
                          )

passing.set_upstream(start)
