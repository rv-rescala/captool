from catswalk.scraping.webdriver import CWWebDriver
import time
from catswalk.scraping.types.type_webdriver import *
import boto3
import os
import json
from captool.order import *
import csv
import os
from datetime import datetime
from lambda_actor.actor_driver import *
from lambda_actor.actor_executor import *
from lambda_actor.types.type_conf import ActorConf
from lambda_actor.types.type_actor_message import *

BUCKET = "captool-gatsby"

def s3_upload(local_fullpath):
    filename = local_fullpath.split("/")[-1]
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_fullpath, BUCKET, f"dataset/output/{order}/{filename}")
    os.remove(local_fullpath)
    return f"s3://{BUCKET}/dataset/output/{order}/{filename}"
    
def get_input_list(order) -> str:
    s3_client = boto3.client('s3')
    tmp_path = f"/tmp/test_{order}.csv"
    # get csv
    s3_client.download_file(BUCKET, f"dataset/input/{order}.csv", tmp_path)
    with open(tmp_path, "r") as f:
        reader = csv.reader(f)
        input_list =  [row for row in reader]
    return input_list
    
def grammar_path() -> str:
    s3_client = boto3.client('s3')
    tmp_path = f"/tmp/grammar.lark"
    s3_client.download_file(BUCKET, f"conf/common/grammar.lark", tmp_path)
    return tmp_path
    
def order_path(order) -> str:
    s3_client = boto3.client('s3')
    tmp_path = f"/tmp/{order}_command.od"
    s3_client.download_file(BUCKET, f"conf/order/{order}/command.od", tmp_path)
    return tmp_path
    
def device(order) -> str:
    s3_client = boto3.client('s3')
    tmp_path = f"/tmp/{order}_browser.json"
    s3_client.download_file(BUCKET, f"conf/order/{order}/browser.json", tmp_path)
    # order specific setting
    with open(tmp_path, "r") as f:
        j = json.load(f)
        device = DEVICE.str_to_enum(j["device"])
    return device

def lambda_handler(event, context):
    try:
        executor_trigger_message_str = event["Records"][0]["body"]
        print(executor_trigger_message_str)
        executor_trigger_message = ExecutorTriggerMessage.decode(executor_trigger_message_str[0])
        request = CWWebDriver(execution_env=EXECUTION_ENV.AWS_LAMBDA, device = device(executor_trigger_message.task_groupid))
    except:
        executor_trigger_message_str = None
        # for debug
        request = CWWebDriver(execution_env=EXECUTION_ENV.AWS_LAMBDA, device = device("unext_list"))
    
    def execution_func(task_message):
        output_path = f"/tmp"
        message = task_message.message
        url = message.split(",")[0]
        filename = message.split(",")[1]
        order_name = task_message.task_groupid
        print(f"execution_func: {url},{filename},{order_name}")
        path = execute(request=request, order_name=order_name, grammar_path=grammar_path(), order_path=order_path(order_name), url=url,output_path=output_path, filename=filename)
        print(f"execution_func: {path}")

    def success_func(message):
        print(f"success_func: {message}")
        return f"successed: {message}"
    
    def failed_func(message):
        print(f"failed_func: {message}")
        return f"failed: {message}"

    actor_executor(bucket=BUCKET, prefix="conf", actor_conf_file="actor_conf.json", execution_func=execution_func, success_func=success_func, failed_func=failed_func, executor_trigger_message_str=executor_trigger_message_str)
    request.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
