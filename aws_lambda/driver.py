import json
from lambda_actor.actor_driver import *
import boto3
import logging
from lambda_actor.actor_driver import *
from lambda_actor.actor_executor import *
from regoogle.drive import *

bucket = "test-captool-gatsby"
prefix = "conf"
actor_conf_file = "actor_conf.json"
MANUAL_TRIGGER_NAME = ["cmoa_top"]
MANUAL = False

GDRIVE_CONF_PATH = "conf/google/gdrive.json"

def get_id_by_key(gdrive, key: str):
    kis = gdrive.list_key_id()
    print(kis)
    for ki in kis:
        _key = ki["name"]
        id = ki["id"]
        if key == _key:
            return id
    return None

def gdrive_init():
    # gconf
    gconf = "/tmp/gdrive.json"
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket, GDRIVE_CONF_PATH, "/tmp/gdrive.json")
    
    with open(gconf, 'r') as f:
        gconf_j = json.load(f)
        key_name = gconf_j["key"]
        parents = gconf_j["folder"]
        print(f"gdrive_init, {key_name}, {parents}")
        local_key = f"/tmp/{key_name}"
        s3_client.download_file(bucket, f"conf/google/{key_name}", f"/tmp/{key_name}")
    return GoogleDrive(local_key, parents)

def gdrive_folder_init(gdrive, key):
    folder_id = get_id_by_key(gdrive, key)
    print(f"folder_id: {folder_id}")
    if folder_id:
        gdrive.delete(folder_id)
    parents = gdrive.create_folder(key)
    return parents
    
def lambda_handler(event, context):
    print(event)
    if not MANUAL:
        event_source = event["Records"][0]["eventSource"]
        if event_source == "aws:s3":
            print(event_source)
            key = event["Records"][0]["s3"]["object"]["key"]
            trigger_name = key.split(".")[0].split("/")[-1]
            print(trigger_name)
            print("event_source from s3 end")
            # gdrive init
            #gdrive = gdrive_init()
            #parents = gdrive_folder_init(gdrive, trigger_name)
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
        for t in MANUAL_TRIGGER_NAME:
            actor_driver_starter(bucket=bucket, prefix=prefix, actor_conf_file=actor_conf_file, trigger_name=t)
        print("event_source from manural end")
        
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
