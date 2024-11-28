import boto3
from flask import Flask
from prometheus_client import Gauge, generate_latest
import os
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
engine_version_gauge = Gauge('custom_engine_version', 'RDS Engine Version', ['instance_identifier'])

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID' 'awsaccesskey')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY' 'awssecretkey')
REGION = os.getenv('REGION','eu-west-1')

rds_client = boto3.client(
    'rds',
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def get_instances():
    response = rds_client.describe_db_instances()
    instances = response['DBInstances']
    return instances

def update_metrics():
    instances = get_instances()
    for instance in instances:
        instance_identifier = instance['DBInstanceIdentifier']
        engine_version = instance['EngineVersion']
        engine_version_gauge.labels(instance_identifier=instance_identifier).set(float(engine_version.split('.')[0]))

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_metrics, trigger='interval', seconds=15)
    scheduler.start()

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    start_scheduler()
    app.run(host='0.0.0.0', port=8080)