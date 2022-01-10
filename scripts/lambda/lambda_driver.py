import json
from lambda_actor.actor_driver import *
import boto3
import logging
from lambda_actor.actor_driver import *
from lambda_actor.actor_executor import *

bucket = "captool"
prefix = "conf"
actor_conf_file = "actor_conf.json"

def lambda_handler(event, context):
    print(event)
    event_source = event["Records"][0]["eventSource"]
    if event_source == "aws:s3":
        key = event["Records"][0]["s3"]["object"]["key"]
        trigger_name = key.split(".")[0].split("/")[-1]
        print(trigger_name)
        # init func
        actor_driver_starter(bucket=bucket, prefix=prefix, actor_conf_file=actor_conf_file, trigger_name=trigger_name)
    # aws:s3
    
    try:
        driver_trigger_message_str = event["Records"][0]["body"]
    except:
        driver_trigger_message_str = None

    #actor_driver(bucket="rescala-configuration", prefix="lambda_actor", conf_filename="sample_actor.json", driver_trigger_message_str=driver_trigger_message_str)
 
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
