import argparse
import json
import os

from tqdm import tqdm

import utils


def log_streams_of_a_group(client, group_name):
    response = client.describe_log_streams(
        logGroupName=group_name,
        orderBy='LastEventTime',
        descending=True,
    )
    streams = [i['logStreamName'] for i in response['logStreams']]
    while 'nextToken' in response:
        response = client.describe_log_streams(
            logGroupName=group_name,
            orderBy='LastEventTime',
            descending=True,
            nextToken=response['nextToken'],
        )
        try:
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                pass
        except KeyError:
            print(response)
            raise AssertionError('Failed to fetch log streams.')
        streams.extend([i['logStreamName'] for i in response['logStreams']])
    
    return streams


def log_events_of_a_stream(client, group_name, stream_name):
    response = client.get_log_events(
        logGroupName=group_name,
        logStreamName=stream_name,
    )
    events = response['events']
    while 'nextForwardToken' in response:
        response = client.get_log_events(
            logGroupName=group_name,
            logStreamName=stream_name,
            nextToken=response['nextForwardToken'],
        )
        if not response['events']:
            break
        try:
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                pass
        except KeyError:
            print(response)
            raise AssertionError('Failed to fetch log events.')
        events.extend(response['events'])
    
    return events


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--force_all', help='force download all log streams even if output_dir is provided', action='store_true')
parser.add_argument('-g', '--group', help='name of the group (e.g., lambda function) for which logs are to be fetched')
parser.add_argument('-o', '--output_dir', help='output folder for logs')
parser.add_argument('-p', '--prefix', help='prefix for the group name (default: /aws/lambda/)')
parser.add_argument('-d', '--delete', help='delete log stream after downloading it', action='store_true')
parser.add_argument('-b', '--beautify', help='store JSON with indentation', action='store_true')
args = parser.parse_args()

if args.output_dir:
    output_dir = os.path.abspath(args.output_dir.replace('"', ''))
else:
    output_dir = 'Logs'

os.makedirs(output_dir, exist_ok=True)
already_downloaded = os.listdir(output_dir)

client = utils.aws_client('logs')

if args.group:
    prefix = args.prefix or '/aws/lambda/'
    group_name = prefix + args.group
else:
    log_groups = client.describe_log_groups()
    group_name = log_groups['logGroups'][0]['logGroupName']

if args.beautify:
    output_indent = 4
else:
    output_indent = None

log_streams = log_streams_of_a_group(client, group_name)
for stream_name in tqdm(log_streams):
    file_name = stream_name.replace('/', '-') + '.log'
    
    if args.force_all or file_name not in already_downloaded:
        events = log_events_of_a_stream(client, group_name, stream_name)
        with open(os.path.join(output_dir, file_name), 'w') as fw:
            json.dump(events, fw, indent=output_indent)
        
    if args.delete:
        client.delete_log_stream(
            logGroupName=group_name,
            logStreamName=stream_name,
        )
