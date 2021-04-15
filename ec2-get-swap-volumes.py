import boto3
import os
import json

instance_id = "i-01249f477ae3d6a03"
volumes = []

if __name__ == '__main__':
  
  os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'

  session = boto3.Session(profile_name='pnp')
  ec2_client = session.client(
    'ec2',
    region_name='eu-west-1'
  )

  instances = ec2_client.describe_instances(
    InstanceIds=[
        instance_id
    ]
)
  for instance in instances['Reservations'][0]['Instances']:
    for volume in instance['BlockDeviceMappings']:
      print(volume['Ebs']['VolumeId'])