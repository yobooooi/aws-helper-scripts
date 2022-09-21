from ctypes.wintypes import PLARGE_INTEGER
import boto3
import json

#
# Author: Adan Patience
# Date: 24 November 2020
# Description:
# List AWS accounts via Organisation
#
# List AWS accounts via Organisation
#
profile = ''
region =  'us-east-1'

if __name__ == '__main__':
    
    session = boto3.Session()
    
    org_client = session.client(
      'organizations',
      region_name=region
    )
    paginator = org_client.get_paginator('list_children') #get paginator resource for the list_aggregate_discovered_resources method
    
    page_iterator = paginator.paginate(
      ParentId='ou-39up-e0vrb3ep',
      ChildType='ACCOUNT',
      PaginationConfig={
        'MaxItems': 10,
        'PageSize': 10
    })

    associated_accounts = []
    
    for aggregated_resources in page_iterator:
      for child in aggregated_resources['Children']:
        associated_accounts.append(child['Id'])
    print(associated_accounts)