import boto3
import os
import json

#
# Author: Adan Patience
# Date: 24 November 2020
# Description:
# Using the aws-controltower-GuardrailsComplianceAggregator, the script lists all EC2 instances in the account in the following format:
# accountId, instanceId, privateIpAddress, subnetId, vpcId
#
# An easy means to audit the EC2 resources in an AWS Organiztion
#
profile = 'master'
region =  'eu-west-1'

if __name__ == '__main__':
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'

    session = boto3.Session(profile_name=profile) #profile of the adminstrator account details
    
    config_service_client = session.client(
      'config',
      region_name=region
    )
    paginator = config_service_client.get_paginator('list_aggregate_discovered_resources') #get paginator resource for the list_aggregate_discovered_resources method
    operation_params = {
      'ConfigurationAggregatorName':'aws-controltower-GuardrailsComplianceAggregator',
      'ResourceType':'AWS::EC2::Instance'
    }
    print('accountId, instanceId, privateIpAddress, subnetId, vpcId')
    page_iterator = paginator.paginate(**operation_params) #create paginator and parse parameters and iterate over results in for loop
  
    for aggregated_resources in page_iterator:
      resource_configs = config_service_client.batch_get_aggregate_resource_config(
        ConfigurationAggregatorName='aws-controltower-GuardrailsComplianceAggregator',
        ResourceIdentifiers=aggregated_resources['ResourceIdentifiers']
      )
      for resource_id in resource_configs['BaseConfigurationItems']:
        parsed_config = json.loads(resource_id['configuration'])
        print('{0}, {1} ,{2} ,{3}, {4}'.format(
          resource_id['accountId'],
          parsed_config['instanceId'],
          parsed_config['privateIpAddress'],
          parsed_config['subnetId'],
          parsed_config['vpcId']
        ))