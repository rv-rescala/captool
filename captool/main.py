import argparse
from catswalk.scraping.webdriver import CWWebDriver
from catswalk.scraping.types.type_webdriver import *
from captool.order import *
import json
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='cp tool')
    parser.add_argument('conf', help='conf')
    parser.add_argument('order', help='order')
    args = parser.parse_args()
    print(args)

    conf_tool_common = f"{args.conf}/tool/common.json"
    conf_tool_specific = f"{args.conf}/tool/{args.order}.json"
    conf_url = f"{args.conf}/url/{args.order}.csv"
    conf_order = f"{args.conf}/order/{args.order}.od"
    conf_lark = f"{args.conf}/lark/grammar.lark"
    print(f"conf_tool_common: {conf_tool_common}, conf_tool_specific: {conf_tool_specific},conf_url: {conf_url},conf_order: {conf_order},conf_lark: {conf_lark}")
    
    # common setting
    with open(conf_tool_common, "r") as f:
        j = json.load(f)
        binary_location = j["binary_location"]
        executable_path = j["executable_path"]
        execution_env = EXECUTION_ENV.str_to_enum(j["execution_env"])
        output_path = j["output_path"]

    # order specific setting
    with open(conf_tool_specific, "r") as f:
        j = json.load(f)
        device = DEVICE.str_to_enum(j["device"])

    # url_path_list
    with open(conf_url, "r") as f:
        reader = csv.DictReader(f)
        input_list =  [row for row in reader]
    

    #request = CWWebDriver(binary_location=binary_location, executable_path=executable_path, execution_env=execution_env,  device = device)
    request = None
    path_list = [execute(request=request, grammar_path=conf_lark, order_path=conf_order, url=i["url"],output_path=output_path, filename=i["filename"]) for i in input_list]
    #request.close()
    print(path_list)

    #request.close
    # tool setting