import boto3
import os
import json

if __name__ == '__main__':
  
  os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'

  session = boto3.Session(profile_name='pnp')
  ssm_client = session.client(
    'ssm',
    region_name='eu-west-1'
  )

  ssm_managed_instances = ssm_client.describe_instance_information(
    MaxResults=50
  )
  for instance in ssm_managed_instances['InstanceInformationList']:
    print('{0}, {1}, {2}, {3}'.format(instance['InstanceId'], instance['PlatformType'], instance['PlatformName'], instance['PlatformVersion']))