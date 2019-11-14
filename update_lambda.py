import argparse
import os
import shutil

import utils


parser = argparse.ArgumentParser()
parser.add_argument('folder', help='folder to upload')
parser.add_argument('-n', '--name', help='name of the function (if not same as folder name)')
parser.add_argument('-a', '--admin', help='use admin credentials', action='store_true')
args = parser.parse_args()

folder = os.path.basename(
    os.path.normpath(
        args.folder.replace('"', '')
    )
)
abs_path_parent = os.path.dirname(os.path.abspath(args.folder))
name = args.name or folder

destination_zip = os.path.join(abs_path_parent, name)
shutil.make_archive(
    destination_zip,
    'zip',
    os.path.join(abs_path_parent, folder),
)
with open(f'{destination_zip}.zip', 'rb') as fr:
    code = fr.read()

client = utils.aws_client('lambda', admin=args.admin)
response = client.update_function_code(
    FunctionName=name,
    ZipFile=code,
)

try:
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        pass
except KeyError:
    print(response)
    raise AssertionError('Failed to update code.')
