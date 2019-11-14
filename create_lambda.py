import argparse
import json
import os
import shutil

from tqdm import tqdm

import utils


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--folder', help='folder representing the lambda function')
group.add_argument('-a', '--all_folders', help='folder containing subfolders each representing lambda function (bulk create)')
parser.add_argument('-c', '--config', help='location of config file (looks for config file in the folder passed to --folder / --all_folders option if not specified)')
args = parser.parse_args()

if args.folder:
    abs_path_parent = os.path.dirname(os.path.abspath(args.folder))
    folders = [os.path.basename(
        os.path.normpath(
            args.folder.replace('"', '')
        )
    )]
else:
    abs_path_parent = os.path.abspath(args.all_folders)
    folders = next(os.walk(abs_path_parent))[1]

path_config = os.path.join(args.config or abs_path_parent, 'config.json')
with open(path_config, 'r') as fr:
    config = json.load(fr)


def zipped_contents(root):
    shutil.make_archive(
        root,
        'zip',
        root,
    )
    with open(f'{root}.zip', 'rb') as fr:
        code = fr.read()
    return code

client = utils.aws_client('lambda')

for folder in tqdm(folders):
    code = zipped_contents(os.path.join(abs_path_parent, folder))
    d = config[folder]
    response = client.create_function(
        FunctionName=folder,
        Runtime=d['Runtime'],
        Role=d['Role'],
        Handler=d['Handler'],
        Timeout=d['Timeout'],
        MemorySize=d['MemorySize'],
        Code={
            'ZipFile': code,
        }
    )
    
    assert response['ResponseMetadata']['HTTPStatusCode'] == 201
    # try:
        # if response['ResponseMetadata']['HTTPStatusCode'] == 201:
            # pass
    # except KeyError:
        # print(response)
        # raise AssertionError('Failed to create function.')
