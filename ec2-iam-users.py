import boto3
import os
import json
from rich import console

from rich.console import Console
from rich.table import Table
from rich.progress import track
#
# Author: Adan Patience
# Date: 24 November 2020
# Description: List all users with access keys and last date used
# 
# UserId, UserName, AccessKeyId, LastUsedDate
#
#
profile = 'globee'
region  =  'eu-west-1'

console  = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("UserID", style="dim")
table.add_column("UserName")
table.add_column("AccessKeyId", justify="right")
table.add_column("AccessKeyLastUsed", justify="right")


if __name__ == '__main__':
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'

    session = boto3.Session(profile_name=profile) #profile of the adminstrator account details
    
    iam = session.client(
      'iam',
      region_name=region
    )
    paginator = iam.get_paginator('list_users') #get paginator resource for the list_aggregate_discovered_resources method
    page_iterator = paginator.paginate() #create paginator and parse parameters and iterate over results in for loop

    for aggregated_resources in page_iterator:
      for user in track(aggregated_resources['Users']):
        response_access_keys = iam.list_access_keys(
          UserName=user['UserName']
        )
        for access_keys in response_access_keys['AccessKeyMetadata']:
          last_used = iam.get_access_key_last_used(
            AccessKeyId=access_keys['AccessKeyId']
          )
          if 'LastUsedDate'in last_used['AccessKeyLastUsed']:
            table.add_row(
              "{0}".format(user['UserId']),
              "[yellow]{0}[/yellow]".format(user['UserName']),
              "{0}".format(access_keys['AccessKeyId']),
              "{0}".format(last_used['AccessKeyLastUsed']['LastUsedDate'])
            )
    console.print(table)