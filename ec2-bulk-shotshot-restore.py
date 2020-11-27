import boto3
import os
import json


from csv import reader
from datetime import datetime

#
# Author: Adan Patience
# Date: 27 November 2020
# Description:
# Bulk restore snapshots with details in a CSV format
#
# Restore root snpashot volumes from a CSV with the format:
# i-0d98518a6250bc51d,snap-0716b0845d19d05ee,host_name
#
file_name = 'snapshots.csv'
date = datetime.now()
if __name__ == '__main__':
  
  os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'

  session = boto3.Session(profile_name='profile')
  ec2_client = session.client(
    'ec2',
    region_name='eu-west-1'
  )
  
  with open(file_name, 'r') as data:
      snapshots = reader(data)
      for snapshot in snapshots:
        print('Creating Volume of Snapshot: {0} for Instance: {1} - {2}'.format(snapshot[1], snapshot[0], snapshot[2]))
        response = ec2_client.create_volume(
            AvailabilityZone = 'eu-west-1a',
            SnapshotId = snapshot[1],
            TagSpecifications=[
              { 
                'ResourceType':'volume',
                'Tags': [
                  {
                    'Key': 'Name',
                    'Value': 'SP2-Upgrade-Test-Volume of-{0}'.format(snapshot[2])
                  },
                  {
                    'Key': 'Device',
                    'Value': 'root'
                  },
                  {
                    'Key': 'Date',
                    'Value': '{0}'.format(date.strftime("%Y-%m-%d"))
                  },
                  {
                    'Key': 'Type',
                    'Value': 'SP Upgrade - Testing'
                  }
                ]
              },
            ],
          )
