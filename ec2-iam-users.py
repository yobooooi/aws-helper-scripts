import boto3
import os
import json

#
# Author: Adan Patience
# Date: 24 November 2020
# Description: List all users with access keys and last date used
# 
# UserId, UserName, AccessKeyId, LastUsedDate
#
#
profile = 'synthesis-internal-dev'
region =  'eu-west-1'

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
      for user in aggregated_resources['Users']:
        response_access_keys = iam.list_access_keys(
          UserName=user['UserName']
        )
        for access_keys in response_access_keys['AccessKeyMetadata']:
          last_used = iam.get_access_key_last_used(
            AccessKeyId=access_keys['AccessKeyId']
          )
          if 'LastUsedDate'in last_used['AccessKeyLastUsed']:
            print(user['UserId'], end=",")
            print(user['UserName'], end=",")
            print(access_keys['AccessKeyId'], end=",")
            print(last_used['AccessKeyLastUsed']['LastUsedDate'])