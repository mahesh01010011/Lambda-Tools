# Lambda Tools

Tools for making our lives easier when working with AWS Lambda:

* **Update Lambda**: Easily update lambdas after making changes to the local copy

* **Download Lambda**: Download lambdas as zip files

* **Download Logs**: Download logs of lambda execution

---

# Update Lambda

Easily update code in AWS Lambda from local machine, without having to open the lambda console.

Use the `-a` / `--admin` switch if it's been configured separately in the `py_config.ini` file.

## Pre-requisites

* It is assumed that you have a folder that contains all the files in a lambda function.
    
    To avoid any accidental omissions, it's a good idea to export the function to a zip file from within lambda console.

* After making changes to code in the local folder, run the `update_lambda.py` script (see next section).


## Recommended Usage

If the folder in which you're working has the same name as the lambda function in AWS, the following command will be sufficient to update the code:

    python update_lambda.py local_folder_name

If it's not, you'll have to pass an additional argument, like this:

    python update_lambda.py local_folder_name -n lambda_name

## Command Line Help

Use `-h` / `--help` like this...

    python update_lambda.py -h

... to show help message:

    usage: update_lambda.py [-h] [-n NAME] [-a] folder

    positional arguments:
      folder                folder to upload

    optional arguments:
      -h, --help            show this help message and exit
      -n NAME, --name NAME  name of the function (if not same as folder name)
      -a, --admin           use admin credentials

## Additional Tip

You can save the command in a batch script and double-click that instead of running in the command line/prompt.

---

# Download Lambda

Download lambdas as zip files.

## Usage

Pass the name of the lambda you want to download:

    python download_lambda.py -n some_lambda_function

If you want to download all the lambdas, pass the `-a` / `--all` switch:

    python download_lambda.py -a

**NOTE:** The `-n` / `--name` command line switch will override `-a` / `--all` switch.

**NOTE:** If you run the program without any command line switches, it'll download the first available lambda.

**WARNING:** The program will create a `Downloads` folder. So, if you already have content in it, they'll get mixed up with these downloads.

## Command Line Help

Use `-h` / `--help` like this...

    python download_lambda.py -h

... to show help message:

    usage: download_lambda.py [-h] [-a] [-d] [-n NAME]

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             download all functions; overridden by `name` if both
                            are used
      -d, --dont_download   do not download the zip files; merely update the
                            config file
      -n NAME, --name NAME  name of the function to download

---

# Download Logs

Download all log events (for every log stream) pertaining to a group (such as a lambda function).

## Usage

Pass the name of the group (e.g., lambda function) for which you want to download the logs:

    python download_logs.py -g some_lambda_function

You can specify the output directory for the logs to be stored, like this:

    python download_logs.py -g some_lambda_function -o path\to\output_dir

**NOTE:** If you run the program without any command line switches, it'll download the logs for the first available group.

**WARNING:** The program will create a `Logs` folder (if `-o` / `--output_dir` has not been specified). So, if you already have content in it, they'll get mixed up with the logs.

## Command Line Help

Use `-h` / `--help` like this...

    python download_logs.py -h

... to show help message:

    usage: download_logs.py [-h] [-f] [-g GROUP] [-o OUTPUT_DIR] [-p PREFIX] [-d]
                            [-b]

    optional arguments:
      -h, --help            show this help message and exit
      -f, --force_all       force download all log streams even if output_dir is
                            provided
      -g GROUP, --group GROUP
                            name of the group (e.g., lambda function) for which
                            logs are to be fetched
      -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            output folder for logs
      -p PREFIX, --prefix PREFIX
                            prefix for the group name (default: /aws/lambda/)
      -d, --delete          delete log stream after downloading it
      -b, --beautify        store JSON with indentation
