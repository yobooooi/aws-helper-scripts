import boto3
import datetime
import os
import json

from rich import console
from dateutil.tz import tzlocal

from rich.console import Console
from rich.table import Table
from rich.progress import track
#
# Author: Adan Patience
# Date: 24 November 2020
# Description: List all users with access keys and last date used in your account
# 
# Account ID, UserId, UserName, AccessKeyId, LastUsedDate
#
#
master_account_id = ""

profile = 'root'
region  =  'eu-west-1'

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'
session = boto3.Session(profile_name=profile) #profile of the adminstrator account details
    
console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Account ID", justify="right")
table.add_column("UserID", style="dim")
table.add_column("UserName")
table.add_column("AccessKeyId", justify="right")
table.add_column("AccessKeyLastUsed", justify="right")

def get_active_access_keys(account_id):
  sts_client = session.client('sts')
  assumed_role_object=sts_client.assume_role(
    RoleArn="arn:aws:iam::{}:role/AWSControlTowerExecution".format(account_id),
    RoleSessionName="AssumeRoleSession"
  )
  credentials=assumed_role_object['Credentials']

  iam=boto3.client(
    'iam',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken'],
  )
  paginator = iam.get_paginator('list_users') #get paginator resource for the list_aggregate_discovered_resources method
  page_iterator = paginator.paginate() #create paginator and parse parameters and iterate over results in for loop

  for aggregated_resources in page_iterator:
    for user in aggregated_resources['Users']:
      response_access_keys = iam.list_access_keys(
        UserName=user['UserName']
      )
      for access_keys in response_access_keys['AccessKeyMetadata']:
        last_used = iam.get_access_key_last_used(
          AccessKeyId=access_keys['AccessKeyId']
        )
        if 'LastUsedDate'in last_used['AccessKeyLastUsed']:
          table.add_row(
            "[red]{0}[red]".format(account_id),
            "{0}".format(user['UserId']),
            "[yellow]{0}[/yellow]".format(user['UserName']),
            "{0}".format(access_keys['AccessKeyId']),
            "{0}".format(last_used['AccessKeyLastUsed']['LastUsedDate'])
          )
  return True

if __name__ == '__main__':
    organization = session.client('organizations')

    org_paginator = organization.get_paginator('list_accounts') 
    org_iterator = org_paginator.paginate()
    for org in org_iterator:
      for account in track(org['Accounts']):
        if account['Id'] != master_account_id:
          get_active_access_keys(account_id = account['Id'])
    console.print(table)
