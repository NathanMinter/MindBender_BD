from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('capstone', default_args=default_args, description='Run Capstone pipeline', schedule_interval='5 13 * * *')

zookeeper = "zookeeper-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/zookeeper.properties"
kafka = "kafka-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/server1.properties"
consumer = "kafka-console-consumer.sh --bootstrap-server localhost:9099 --topic capstone"
spark = "spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1,org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.2 ~/opt/MindBender_BD/capstone/consumer.py"
latest = "python3 /home/n/opt/MindBender_BD/capstone/latest.py"

## Start Zookeeper
t1 = BashOperator(task_id="zookeeper", bash_command=zookeeper, dag=dag, trigger_rule=TriggerRule.ALL_DONE)

## Start Kafka server
t2 = BashOperator(task_id="kafka", bash_command=kafka, dag=dag, trigger_rule=TriggerRule.ALL_DONE)

## Start Kafka consumer
t3 = BashOperator(task_id="consumer", bash_command=consumer, dag=dag, trigger_rule=TriggerRule.ALL_DONE)

## Start Spark
t4 = BashOperator(task_id="spark", bash_command=spark, dag=dag, trigger_rule=TriggerRule.ALL_DONE)

## Start latest producer
t5 = BashOperator(task_id="latest", bash_command=latest, dag=dag)

## Run correlation matrix
t6 = BashOperator(task_id='correlation', depends_on_past=False, bash_command='python3 /home/n/opt/MindBender_BD/capstone/correlation.py', dag=dag)

## Simultaneously run equation tranformer
t7 = BashOperator(task_id='equation', depends_on_past=False, bash_command='python3 /home/n/opt/MindBender_BD/capstone/transformer.py', dag=dag)

dag.doc_md = __doc__

## Run in order, both correlation and equation can run simultaneously
t1 >> t2 >> t3 >> t4 >> t5 >> [t6, t7]



"""
## Start up Kafka and Spark (if not already running), then run latest script to send latest movies to Kafka
t1 = BashOperator(task_id='start_project', bash_command='bash /home/n/opt/MindBender_BD/capstone/capstone.sh', dag=dag)

## Run correlation matrix
t2 = BashOperator(task_id='correlation', depends_on_past=False, bash_command='python3 /home/n/opt/MindBender_BD/capstone/correlation.py', dag=dag)

## Simultaneously run equation tranformer
t3 = BashOperator(task_id='equation', depends_on_past=False, bash_command='python3 /home/n/opt/MindBender_BD/capstone/transformer.py', dag=dag)

dag.doc_md = __doc__

## Start tasks 2 and 3 after task 1
t1 >> [t2, t3]
"""
