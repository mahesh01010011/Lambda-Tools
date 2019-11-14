import argparse
import json
import os

import requests
from tqdm import tqdm

import utils


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--all', help='download all functions; overridden by `name` if both are used', action='store_true')
parser.add_argument('-d', '--dont_download', help='do not download the zip files; merely update the config file', action='store_true')
parser.add_argument('-n', '--name', help='name of the function to download')
args = parser.parse_args()

os.makedirs('Downloads', exist_ok=True)

client = utils.aws_client('lambda')

if args.name:
    functions = [args.name]
else:
    d = client.list_functions()
    functions = [i['FunctionName'] for i in d['Functions']]
    if not args.all:
        functions = [functions[0]]

function_configurations = {}
for f in tqdm(functions):
    function_details = client.get_function(FunctionName=f)
    function_configurations[f] = function_details['Configuration']
    if args.dont_download:
        continue
    
    url = function_details['Code']['Location']
    r = requests.get(url)
    with open(f'Downloads/{f}.zip', 'wb') as fw:
        fw.write(r.content)

with open('Downloads/config.json', 'w') as fw:
    json.dump(function_configurations, fw)
