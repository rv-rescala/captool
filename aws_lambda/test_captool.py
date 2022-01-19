from catswalk.scraping.webdriver import CWWebDriver
import time
from catswalk.scraping.types.type_webdriver import *
import boto3
import os
import json
from captool.order import *
import csv
import os

BUKET = "captool-gatsby"
ORDER = "unext_list"

def s3_upload(local_fullpath):
    filename = local_fullpath.split("/")[-1]
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_fullpath, BUKET, f"dataset/output/{ORDER}/{filename}")
    os.remove(local_fullpath)
    return f"s3://{BUKET}/dataset/output/{ORDER}/{filename}"
    
def get_input_list() -> str:
    s3_client = boto3.client('s3')
    tmp_path = f"/tmp/test_{ORDER}.csv"
    # get csv
    s3_client.download_file(BUKET, f"dataset/input/{ORDER}.csv", tmp_path)
    with open(tmp_path, "r") as f:
        reader = csv.reader(f)
        input_list =  [row for row in reader]
    return input_list
    
def grammar_path() -> str:
    s3_client = boto3.client('s3')
    tmp_path = f"/tmp/grammar.lark"
    s3_client.download_file(BUKET, f"conf/common/grammar.lark", tmp_path)
    return tmp_path
    
def order_path() -> str:
    s3_client = boto3.client('s3')
    tmp_path = f"/tmp/{ORDER}_command.od"
    s3_client.download_file(BUKET, f"conf/order/{ORDER}/command.od", tmp_path)
    return tmp_path
    
def device() -> str:
    s3_client = boto3.client('s3')
    tmp_path = f"/tmp/{ORDER}_browser.json"
    s3_client.download_file(BUKET, f"conf/order/{ORDER}/browser.json", tmp_path)
    # order specific setting
    with open(tmp_path, "r") as f:
        j = json.load(f)
        device = DEVICE.str_to_enum(j["device"])
    return device

def lambda_handler(event, context):
    request = CWWebDriver(execution_env=EXECUTION_ENV.AWS_LAMBDA, device = device())
    output_path = f"/tmp"
    os.makedirs(output_path, exist_ok=True)
    path_list = [execute(request=request, order_name=ORDER, grammar_path=grammar_path(), order_path=order_path(), url=i[0],output_path=output_path, filename=i[1]) for i in get_input_list()]
    print(path_list)
    [s3_upload(i) for i in path_list]
    request.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
