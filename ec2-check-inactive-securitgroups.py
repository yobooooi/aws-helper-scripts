import boto3
import os
import json


from rich import console
from dateutil.tz import tzlocal

from rich.console import Console
from rich.table import Table
from rich.progress import track

#
# Author: Adan Patience
# Date: 22 March 2022
# Description:
# Check inactive security groups
#
#
profile = 'clickcart_dev'
region  =  'eu-west-1'

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'
session = boto3.Session(profile_name=profile, region_name=region) #profile of the adminstrator account details

console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Account ID", justify="right")
table.add_column("Security Group ID", style="dim")
table.add_column("Description", style="dim")
table.add_column("Network Interface", style="dim")

account_id = 'N/A'

if __name__ == '__main__':
  ec2 = session.client('ec2')

  ec2_paginator = ec2.get_paginator('describe_security_groups')
  ec2_iterator  = ec2_paginator.paginate()
  for security_groups in ec2_iterator:
    for sg in security_groups['SecurityGroups']:
      security_group_name, security_group_id = sg['GroupName'], sg['GroupId']
      network_interfaces = ec2.describe_network_interfaces(
                        Filters=[
                            {
                                'Name': 'group-id',
                                'Values': [
                                    '{0}'.format(security_group_id),
                                ]
                            }
                        ])
      if len(network_interfaces['NetworkInterfaces']) > 0:
        for interface in network_interfaces['NetworkInterfaces']:
          table.add_row(
            "[red]{0}[red]".format(account_id),
            "{0}".format(security_group_id),
            "[yellow]{0}[/yellow]".format(interface['Description']),
            "{0}".format(interface['NetworkInterfaceId']),
          )
      else:
        table.add_row(
          "[red]{0}[red]".format(account_id),
          "{0}".format(security_group_id),
          "[yellow]{0}[/yellow]".format('N/A'),
          "{0}".format('N/A'),
          )
  console.print(table)