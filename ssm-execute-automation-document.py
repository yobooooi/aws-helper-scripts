import boto3

# Create a boto3 client to the Systems Manager service
client = boto3.client('ssm', region_name='us-east-1')

# Set the parameters for the runbook execution
runbook_name = 'AWS-ConfigureS3BucketVersioning'
document_version = '$LATEST'
parameters = {
    'BucketName': ['test-sh-trigger'],
    'VersioningState': ['Enabled']
}

# Execute the runbook
response = client.start_automation_execution(
    DocumentName=runbook_name,
    DocumentVersion=document_version,
    Parameters=parameters
)

# Print the execution ID
print(response['AutomationExecutionId'])
