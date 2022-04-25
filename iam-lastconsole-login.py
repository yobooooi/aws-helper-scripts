import boto3
from datetime import datetime, timezone
import dateutil.parser
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
master_account_id = ''

profile = ''
region  =  'eu-west-1'

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'
session = boto3.Session(profile_name=profile) #profile of the adminstrator account details

console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Account Name", justify="right")
table.add_column("Account ID", justify="right")
table.add_column("UserName")
table.add_column("PasswordLastUsed", justify="right")

def get_lastconsole_login(account_id, account_name):
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
        try:
          password_lastused_date = user['PasswordLastUsed']
          time_delta = datetime.now(timezone.utc) - password_lastused_date
          print(time_delta.days)
          if time_delta.days > 7:
            table.add_row(
              "{0}".format(account_name),
              "{0}".format(account_id),
              "[yellow]{0}[/yellow]".format(user['UserName']),
              "[green]{0}[/green]".format(user['PasswordLastUsed'])
              )
          else:
            table.add_row(
              "{0}".format(account_name),
              "{0}".format(account_id),
              "[yellow]{0}[/yellow]".format(user['UserName']),
              "[red]{0}[/red]".format(user['PasswordLastUsed'])
              )
        except KeyError: pass
  return True

if __name__ == '__main__':
    organization = session.client('organizations')

    org_paginator = organization.get_paginator('list_accounts')
    org_iterator = org_paginator.paginate()
    for org in org_iterator:
      for account in track(org['Accounts']):
        if account['Id'] != master_account_id:
          get_lastconsole_login(account_id = account['Id'], account_name=account['Name'])
    console.print(table)
