import boto3
import os
import json


from datetime import datetime

#
# Author: Adan Patience
# Date: 27 November 2020
# Description:
# Bulk delete snapshots from a text file
#
# bulk delete snpashots from a text file with the following format:
# snap-0716b0845d19d05ee
# snap-047f5363d3833d567
# snap-0346a160faa4c144c
# snap-01c862d85afdc67c4
# snap-03ce6301ab3d41ca0
# snap-0ec89a8ad4fa028e4
# snap-0624628f3f4afbdc0
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
