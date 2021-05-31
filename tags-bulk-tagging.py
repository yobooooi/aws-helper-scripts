import boto3
import os
import json

#
# Author: Adan Patience
# Date: 31 May 2021
# Description: Script to bulk tag different AWS resources given a file
# 
#
#
profile = 'internal-dev'
region =  'eu-west-1'

if __name__ == '__main__':
    file_name = "resources_to_tag.txt"
    tags = {
      "what": "demo",
      "who" : "adan"
    }
    f = open(file_name)
    resources = f.readlines()
    resources = [line.rstrip('\n') for line in resources]

    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'
    session = boto3.Session(profile_name=profile) #profile of the adminstrator account details
    
    tagging_client = session.client(
      'resourcegroupstaggingapi',
      region_name=region
    )

    response = tagging_client.tag_resources(
      ResourceARNList = resources,
      Tags=tags
    )
