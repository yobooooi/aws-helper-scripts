import boto3
import os
import json


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
file_name = 'snapshots-to-delete.txt'
date = datetime.now()
if __name__ == '__main__':
  
  os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'

  session = boto3.Session(profile_name='decision-support')
  ec2_client = session.client(
    'ec2',
    region_name='eu-west-1'
  )
  
  with open(file_name, 'r') as f:
      for snapshot in f:
    
        print('Deleting Snapshot: {0}'.format(snapshot.rstrip()))
        response = ec2_client.delete_snapshot(
            SnapshotId = '{0}'.format(snapshot.rstrip())
          )
