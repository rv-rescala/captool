import json
import time
import boto3
import os
from datetime import datetime
from lambda_actor.actor_driver import *
from lambda_actor.actor_executor import *

def execution_func(message):
    print(f"execution_func: {message}")
    return f"executed: {message}"

def success_func(message):
    print(f"success_func: {message}")
    return f"successed: {message}"

def failed_func(message):
    print(f"failed_func: {message}")
    return f"failed: {message}"
    

def lambda_handler(event, context):
    try:
        executor_trigger_message_str = event["Records"][0]["body"]
        print(executor_trigger_message_str)
    except:
        executor_trigger_message_str = None
        
    actor_executor(bucket="captool", prefix="conf", actor_conf_file="actor_conf.json", execution_func=execution_func, success_func=success_func, failed_func=failed_func, executor_trigger_message_str=executor_trigger_message_str)
   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
