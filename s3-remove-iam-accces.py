from email import policy
from http.client import ResponseNotReady
import resource
import boto3
import os
import json

#
# Desccription
# [S3.12] S3 access control lists (ACLs) should not be used to manage user access to buckets - Sev [Medium]
#


# {
#   "eventId": "<uuid>",
#   "resourceId": "my-sg",
#   "awsAccountId": "1234567890",
#   "awsRegion": "us-east-1",
#   "securityRuleType": "restricted-ssh",
#   "ruleName": "INCOMING_SSH_DISABLED",
#   "dateTimeStamp": "2021-12-29T15:51:27.948166",
#   "service": "AWS::EC2::SecurityGroup",
#   "sourceListener": "aws.config",
#   "remediated": "False"
# }

def remove_non_compliant_statements(policy_statements):
  updated_bucket_policy = [statements for statements in policy_statements if "arn:aws:iam::{0}:user/".format(accountId) not in statements["Principal"]["AWS"]]
  return updated_bucket_policy

if __name__ == '__main__':
  
  resourceId = "s3.12-finding-remediator-test"
  accountId  = ""

  session = boto3.Session()
  s3_client = session.client(
    's3',
    region_name='eu-west-1'
  ) 

  response = s3_client.get_bucket_policy(Bucket=resourceId)

  bucket_policy = json.loads(response["Policy"])
  updated_bucket_policy = []
  # iterating through Bucket Policy to idenitify which Statements should be removed
  policy_statements = json.loads(response["Policy"])["Statement"]
  for statements in policy_statements:
    if "arn:aws:iam::{0}:user/".format(accountId) in statements["Principal"]["AWS"]:
      print("[S3.12] S3 access control lists (ACLs) should not be used to manage user access to buckets")
      print("Statement with Sid:{0} flagged for removal. Principal is an IAM user of accountId:{1}. Access should be managed via IAM policies".format(statements["Sid"], accountId))
  
  # remove non-compliant statements
  updated_bucket_policy_statement = remove_non_compliant_statements(policy_statements)
  bucket_policy["Statement"] = updated_bucket_policy_statement

  response = s3_client.put_bucket_policy(Bucket=resourceId, Policy=json.dumps(bucket_policy))
  # update bucket policy
  print(bucket_policy)

