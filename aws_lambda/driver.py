import json
from lambda_actor.actor_driver import *
import boto3
import logging
from lambda_actor.actor_driver import *
from lambda_actor.actor_executor import *

bucket = "captool-gatsby"
prefix = "conf"
actor_conf_file = "actor_conf.json"
MANUAL_TRIGGER_NAME = "unext_list"
MANUAL = True

def lambda_handler(event, context):
    print(event)
    if not MANUAL:
        event_source = event["Records"][0]["eventSource"]
        if event_source == "aws:s3":
            key = event["Records"][0]["s3"]["object"]["key"]
            trigger_name = key.split(".")[0].split("/")[-1]
            print(trigger_name)
            print("event_source from s3 end")
            # init func
            actor_driver_starter(bucket=bucket, prefix=prefix, actor_conf_file=actor_conf_file, trigger_name=trigger_name)
        elif event_source == "aws:sqs":
            driver_trigger_message_str = event["Records"][0]["body"]
            actor_driver(bucket=bucket, prefix=prefix, actor_conf_file=actor_conf_file, driver_trigger_message_str=driver_trigger_message_str)
            print("event_source from sqs end")
        else:
            raise Exception("illegal source")
    else:
        driver_trigger_message_str = None
        actor_driver_starter(bucket=bucket, prefix=prefix, actor_conf_file=actor_conf_file, trigger_name=MANUAL_TRIGGER_NAME)
        print("event_source from manural end")
        
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
