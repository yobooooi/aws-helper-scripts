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
# profile = 'clickcart_dev'
region  =  'us-east-1'

# os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'
session = boto3.Session() #profile of the adminstrator account details

console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Account ID", justify="right")
table.add_column("Security Group ID", style="dim")
table.add_column("Description", style="dim")
table.add_column("Network Interface", style="dim")

account_id = '828605012785'

if __name__ == '__main__':
  ec2 = session.client('ec2', region_name=region)

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
            "[yellow]{0}[/yellow]".format("COMPLIANT"),
            "{0}".format(interface['NetworkInterfaceId']),
          )
      else:
        table.add_row(
          "[red]{0}[red]".format(account_id),
          "{0}".format(security_group_id),
          "[yellow]{0}[/yellow]".format('NON_COMPLIANT'),
          "{0}".format('N/A'),
          )
  console.print(table)