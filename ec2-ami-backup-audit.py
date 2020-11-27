import configparser
import boto3
import os
import json
import re

#
# Author: Adan Patience
# Date: 24 November 2020
# Description:
# Retrieve the lastest AMI backup details per running instance in an account. Output as follows :
# instanceId, ami, date
#
# An easy means to audit the ami backups of running instances in an account
#

#
# Method to retrieve the details of the root device, give the Block Mapings and the device name
#
def get_snapshot_from_BlockDeviceMappings(BlockDeviceMappings, device_name):
    for device in BlockDeviceMappings:
        if device['DeviceName'] == device_name:
            return device['Ebs']['SnapshotId']

#
# Method to retreive the instance associated to the snapshot taken
#
def get_details_from_Snapshot(Snapshot):
    instance_id = re.search(r"(?<=CreateImage\().*?(?=\))", Snapshot['Description']).group(0)
    date = Snapshot['StartTime']
    return instance_id, date

if __name__ == '__main__':
    print("InsanceID, AMI, DateTaken, SnapshotID")
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'

    session = boto3.Session(profile_name='pnp') #profile of the adminstrator account details
    aws_regions = [ 'eu-west-1' ]
    
    for region_name in aws_regions:
        # iterating to the aws_region list, and instantiating a resource factory for each region using the temprorary credentials from the STS assume
        ec2_client = session.client(
            'ec2',
            region_name=region_name
        )
        # request to get all AMIs owned by the account
        amis = ec2_client.describe_images(Owners=['self'])
        for ami in amis['Images']:
            image_id = ami['ImageId']
            
            root_device_name = ami['RootDeviceName']
            root_snapshot_id = get_snapshot_from_BlockDeviceMappings(ami['BlockDeviceMappings'], root_device_name)
            snapshot_details = ec2_client.describe_snapshots(SnapshotIds=[root_snapshot_id])
            instace_id, date = get_details_from_Snapshot(snapshot_details['Snapshots'][0])
            
            print("{0}, {1}, {2}, {3}".format(instace_id, image_id, date, root_snapshot_id))
            



