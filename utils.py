import configparser
import os

import boto3
import botocore.client


__all__ = ['aws_client']


def aws_client(client_type, admin=False):
    cnfg = configparser.ConfigParser()
    cnfg.read(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'py_config.ini',
        )
    )
    
    try:
        connect_timeout = cnfg.getint('aws', 'connect_timeout')
    except ValueError:
        connect_timeout = 60
    try:
        read_timeout = cnfg.getint('aws', 'read_timeout')
    except ValueError:
        read_timeout = 60
    
    boto_config = botocore.client.Config(
        connect_timeout=connect_timeout,
        read_timeout=read_timeout,
    )
    
    if admin:
        config_key = 'aws_admin'
    else:
        config_key = 'aws'
    
    session = boto3.Session(
        aws_access_key_id=cnfg[config_key]['access_key_id'],
        aws_secret_access_key=cnfg[config_key]['secret_key'],
        region_name=cnfg['aws']['region_name'],
    )
    return session.client(client_type, config=boto_config)
