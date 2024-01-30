import boto3
import os
import pytest
import json

from moto import(
    mock_config,
    mock_ec2
)

from unittest.mock import patch

@pytest.fixture
def mocked_ec2_client():
    with patch.object(boto3, "client") as mock_client:
        yield mock_client


@pytest.fixture(scope="session")
def ec2_client(request):
    mock = mock_ec2()
    mock.start()
    client = boto3.client("ec2", region_name="us-west-2")

    def fin():
        mock.stop()

    request.addfinalizer(fin)
    return client

@pytest.fixture
def create_non_compliant_security_group(ec2_client):

    groups = []

    non_compliant_sg01 = ec2_client.create_security_group(GroupName="non_compliant_sg01", Description="mock non compliant security group non_compliant_sg01")

    ip_perm = [{
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [{
            "CidrIp": "0.0.0.0/0"
        }]
    }]
    ec2_client.authorize_security_group_ingress(IpPermissions=ip_perm, GroupId="non_compliant_sg01")

    groups.append(non_compliant_sg01)

    yield groups


@mock_config
def test_non_compliant_rds_security_group_ports(
    create_non_compliant_security_group,
    ec2_client,
    mocked_ec2_client):

    # this value will be used to patch the API used to further inspect
    # security group in the function used to evaluate compliance
    mocked_security_groups = ec2_client.describe_security_groups(
        GroupNames=[
            'non_compliant_sg01',
        ],
    )
    with patch.object(ec2_client, "describe_security_groups") as mock_describe:
        def side_effect(*args, **kwargs):
            return mocked_security_groups

        mock_describe.side_effect = side_effect

        # performing API calls with filters
          sgs_filter = ec2_client.describe_security_groups(
              GroupIds=[
                  'sg-903004f8',
              ],
          )

        print(json.dumps(sgs_filter, indent=True))
    
    #
    # configuration item in the invoking event is the configuration item in config
    #

    # from bin.scf_constructs.lcr.runtime.custom_config_evaluators.rds.non_standard_rds_sg_ports.non_standard_rds_sg_ports import lambda_handler

    # event = {
    #     "version":"1.0",
    #     "invokingEvent":"{\"configurationItemDiff\":null,\"configurationItem\":{\"version\":\"1.3\",\"accountId\":\"828605012785\",\"configurationItemCaptureTime\":\"2023-05-17T08:55:14.569Z\",\"configurationItemStatus\":\"OK\",\"configurationStateId\":\"1684313714569\",\"configurationItemMD5Hash\":\"\",\"arn\":\"arn:aws:rds:us-east-1:828605012785:db:database-2\",\"resourceType\":\"AWS::RDS::DBInstance\",\"resourceId\":\"db-LYXUCEJAOMO72P53OXOD4CW2GE\",\"resourceName\":\"database-2\",\"awsRegion\":\"us-east-1\",\"availabilityZone\":\"us-east-1a\",\"resourceCreationTime\":\"2023-03-09T12:03:33.846Z\",\"tags\":{},\"relatedEvents\":[],\"relationships\":[{\"resourceType\":\"AWS::EC2::SecurityGroup\",\"resourceId\":\"sg-0eec387005aef1c32\",\"relationshipName\":\"Is associated with SecurityGroup\"},{\"resourceType\":\"AWS::EC2::SecurityGroup\",\"resourceId\":\"sg-04f980b65eb95aa88\",\"relationshipName\":\"Is associated with SecurityGroup\"},{\"resourceType\":\"AWS::RDS::DBSubnetGroup\",\"resourceId\":\"default-vpc-0de241aa8f83b32e2\",\"relationshipName\":\"Is associated with DBSubnetGroup\"},{\"resourceType\":\"AWS::EC2::SecurityGroup\",\"resourceId\":\"sg-0b2f907f108583015\",\"relationshipName\":\"Is associated with SecurityGroup\"}],\"configuration\":{\"dBInstanceIdentifier\":\"database-2\",\"dBInstanceClass\":\"db.t3.micro\",\"engine\":\"mysql\",\"dBInstanceStatus\":\"available\",\"masterUsername\":\"admin\",\"endpoint\":{\"address\":\"database-2.culp3ehhu8t4.us-east-1.rds.amazonaws.com\",\"port\":3306,\"hostedZoneId\":\"Z2R2ITUGPM61AM\"},\"allocatedStorage\":20,\"instanceCreateTime\":\"2023-03-09T12:03:33.846Z\",\"preferredBackupWindow\":\"05:38-06:08\",\"backupRetentionPeriod\":7,\"dBSecurityGroups\":[],\"vpcSecurityGroups\":[{\"vpcSecurityGroupId\":\"sg-0eec387005aef1c32\",\"status\":\"active\"},{\"vpcSecurityGroupId\":\"sg-04f980b65eb95aa88\",\"status\":\"active\"},{\"vpcSecurityGroupId\":\"sg-0b2f907f108583015\",\"status\":\"active\"}],\"dBParameterGroups\":[{\"dBParameterGroupName\":\"default.mysql8.0\",\"parameterApplyStatus\":\"in-sync\"}],\"availabilityZone\":\"us-east-1a\",\"dBSubnetGroup\":{\"dBSubnetGroupName\":\"default-vpc-0de241aa8f83b32e2\",\"dBSubnetGroupDescription\":\"Created from the RDS Management Console\",\"vpcId\":\"vpc-0de241aa8f83b32e2\",\"subnetGroupStatus\":\"Complete\",\"subnets\":[{\"subnetIdentifier\":\"subnet-0367b32db29bef597\",\"subnetAvailabilityZone\":{\"name\":\"us-east-1a\"},\"subnetOutpost\":{},\"subnetStatus\":\"Active\"},{\"subnetIdentifier\":\"subnet-04b01f498abdedc49\",\"subnetAvailabilityZone\":{\"name\":\"us-east-1b\"},\"subnetOutpost\":{},\"subnetStatus\":\"Active\"},{\"subnetIdentifier\":\"subnet-09adce736a71340ce\",\"subnetAvailabilityZone\":{\"name\":\"us-east-1a\"},\"subnetOutpost\":{},\"subnetStatus\":\"Active\"},{\"subnetIdentifier\":\"subnet-0b3e1ecf9d73d0ad8\",\"subnetAvailabilityZone\":{\"name\":\"us-east-1b\"},\"subnetOutpost\":{},\"subnetStatus\":\"Active\"}]},\"preferredMaintenanceWindow\":\"mon:09:14-mon:09:44\",\"pendingModifiedValues\":{\"processorFeatures\":[]},\"latestRestorableTime\":\"2023-05-17T08:50:00.000Z\",\"multiAZ\":false,\"engineVersion\":\"8.0.28\",\"autoMinorVersionUpgrade\":true,\"readReplicaDBInstanceIdentifiers\":[],\"readReplicaDBClusterIdentifiers\":[],\"licenseModel\":\"general-public-license\",\"optionGroupMemberships\":[{\"optionGroupName\":\"default:mysql-8-0\",\"status\":\"in-sync\"}],\"publiclyAccessible\":false,\"statusInfos\":[],\"storageType\":\"gp2\",\"dbInstancePort\":0,\"storageEncrypted\":false,\"dbiResourceId\":\"db-LYXUCEJAOMO72P53OXOD4CW2GE\",\"cACertificateIdentifier\":\"rds-ca-2019\",\"domainMemberships\":[],\"copyTagsToSnapshot\":true,\"monitoringInterval\":0,\"dBInstanceArn\":\"arn:aws:rds:us-east-1:828605012785:db:database-2\",\"iAMDatabaseAuthenticationEnabled\":false,\"performanceInsightsEnabled\":false,\"enabledCloudwatchLogsExports\":[],\"processorFeatures\":[],\"deletionProtection\":true,\"associatedRoles\":[],\"tagList\":[],\"dBInstanceAutomatedBackupsReplications\":[],\"customerOwnedIpEnabled\":false},\"supplementaryConfiguration\":{\"Tags\":[]},\"resourceTransitionStatus\":\"None\"}}",
    #     "ruleParameters":"{}",
    #     "resultToken":"eyJlbmNyeXB0ZWREYXRhIjpbNTEsLTYzLC0xMDcsLTM2LDExLDExMSwtODksLTM0LDQ1LDEyMyw0LC0xMDgsLTMsMjMsLTIsLTQsMTI2LDExNSwtNDAsMTAyLC02NCw5NSwxMywtOTMsMjUsLTI2LC03MywtNyw0MywxMTUsLTExNiw0OSwtMjcsLTYsMzUsNDYsLTg2LC01OCwtMzQsNzAsMzIsMiwtMTgsODMsMTE2LC01MywtNzIsNjcsMzIsNDgsODksMTEwLC00LDUsNTgsMjEsMTI1LC00NCwxMTcsLTc0LC0zMyw1LC0yMSwtMTEsOTksMTEzLDc5LDExOCwtMTksLTEyMCw5NywxMjAsODIsLTgwLDQ2LDE5LDc0LC05NiwxNCwtNywxMTYsLTEyNyw3OSwtMTYsNjQsOTMsMjIsLTExMCwtNDUsNTcsMzgsLTEyMSwtNzUsMTMsLTEwNCw4MiwtNjAsMTYsLTEsMSwtMzYsLTU2LDk3LDYxLC0zOCw2MCwxMTMsLTEwMywtMTAyLDEyNCwtODAsOTMsLTEyNSw0MCwxMDMsMTI3LC04LC0xMTgsMzIsLTMwLDQ5LC00NCwtNjMsMjIsNjIsLTUwLC0xMjEsLTEyNCwtNDksNDgsLTU5LDcsOTMsLTk5LDgxLC00NiwtMTA3LC00MiwtNzcsLTkxLC0xMTYsLTkyLDEzLC0xMSwtNzIsLTk1LC00NywxMDQsMTcsLTExMCw3NSwtMTYsLTk1LDkxLDEwNSwtMTQsLTg2LDE2LC03MSwtNDEsLTg3LC01MSwtMTI3LDE3LC0xMTEsNDgsMTA3LC0yNCwtNiwtMzAsOTgsMzAsLTMxLC0zNywyNywtNDcsLTM2LDU3LDM2LDEwNCw3Nyw5NCwtMTMsLTM4LC0yMywyOCwtNzMsMTQsLTIsNDgsLTEzLDg4LDIsLTExMywtOTEsLTc4LC0xOSwtMTIzLDEzLC0xMDAsOTYsNDcsLTY4LDQxLDUzLDEwMiw3NCwxNyw4OSwtMTcsLTY4LDYwLDUyLDgwLDIwLDM2LDY4LC0xNiwtNTksOTksMzAsMTIxLDYwLC04MSwtNjksOTgsLTgxLDQsLTIyLDc4LDIzLDI1LDU5LC03Myw1OCw5Myw4MywtNzIsLTYwLC05MSwzMiwtMTExLC0xMjMsLTY4LC01NiwtNzcsMTAyLC01OCwtNDMsMzksNTMsLTIzLDEyLC0xMTgsLTYyLDY3LC02MiwtMzAsMTE3LDEwMiw0MiwtNTcsLTg0LDQzLDY4LDEwNywtNiwtMTEyLC03NywtNTgsNTgsLTEzLDgyLC05MCw3MCw0NSwtNDQsODcsNjQsNzUsNjYsMjgsLTM5LC0xMCw3MiwxMDQsMjUsLTkwLC0zOCw4NywtNDksLTI0LDU2LDk3LDExMyw3OCw3NCw1MSw0NywtOTUsMjEsLTg2LC0xMDEsMzIsMTUsLTI4LC0xMTAsLTEyNiwtNTUsLTMzLDEsNjQsLTcsODEsODEsLTQ5LC0xMjgsLTIyLDE5LC0xMTEsNzIsMCw1OSwzMSwtNTEsMTEzLDYxLDk0LC0zNyw4MCwtODYsOTYsODAsMTksMjYsLTYzLC02OCwtMjksLTEyMiwyNCwxMTIsMTA0LC0xMDQsNDYsMTAyLC0xMCw4MywyNCwtMTEzLC00OSwtMzksLTQ0LDUxLDEwMSwxMjMsLTQ4LC0xMTgsNywxMTcsLTE0LDE3LC04NCwyNCwzMCwtODUsLTQyLC0xMTYsNzEsLTk3LDYwLDkwLDYwLC03Myw2NiwtMzMsLTEyMywtODUsMTA5LDE4LC04Myw3MywyNywtOTQsLTE3LDkyLC02MCwxMSwxOSw1OCwtMTA4LC0yNiwtOTEsMTMsMzksMzIsMzUsMzYsLTI4LDIwLC05MCwtMzMsNjQsODYsLTUzLDg1LC05MywtMzMsMTE0LC0zNyw1NSwtMTAyLDAsNzAsLTEyMywtNDksMjMsOTEsLTcsNTcsLTEyMCwzNywtNzEsLTMyLDExNiw1Niw2OSw2MSw5Nyw3NSwxMDAsLTE5LDEsNjgsMTI2LDU0LDg0LC0xMTgsMjMsLTI2LDk1LDM3LC0xMjEsNzAsODUsNDAsLTgsMTAzLC00MSw2MiwtOCw4LDg4LDk3LC0xLC0yLDYyLC02MywxMDcsNjgsLTQ1LDgyLC0xMTIsLTc3LC0zLC03OCwxMTIsNDgsMjIsOTYsMiwtMzYsLTEsOTIsMzAsNjMsLTUwLC0xMTUsLTIsLTQsLTEyOCw5NSw4NCw1MiwyOCwxMTYsNzEsODIsLTgyLDEyMywtOTgsNywtMzcsLTY2LC0xMjEsMTA2LDUsNjIsNTIsMzcsNDAsODgsLTUzLC03MywtMTA4LC04NCw2Myw4OSw0Myw1NiwtNTEsOTIsLTEyMCwtMzksNTMsNjEsLTEyOCwtNDUsLTMzLDQ0LC0xMywtMTE4LDYsMTA4LDMzLDEwMCwxLDE4LC0xMTAsOTgsLTgwLC04Miw3OSwtOSwtODQsLTkzLDQ3LDQ0LDQsNDQsNjksMTA5LC0yNSw1MiwtNDYsLTYwLC05LC0yNSwtMTksNzksLTQxLC0xMjYsMjYsMjUsLTQyLDEwOCwyNSwzOCw3NSw1MiwtMSwtMiw5OSwtMTAsLTEwNywtMjEsLTQxLDEyMywtNCw5OSwxMDksMTIxLDEyMywtMjcsNDAsLTEwNiw1NywxMDcsMTIxLC04MCw2MywtMjQsMTI2LDE0LC0xMjIsLTEyLC0yMSwtNTAsMTgsLTkxLC05MiwtMzMsOTIsMywtNDYsNSwtMzYsLTU2LDEyMiwtMjIsLTEyMCwtNjksNzAsODAsNDUsNjgsMTcsNjEsLTY3LDEyMywxMjUsLTE0LDYwLC0zOCwxMDcsNTUsLTQ2LDEyMSwtMjIsLTEyMiwtMTIwLC0yNSwyOSw0NCwxNCwtNDUsLTYzLC0xMjIsLTYwLDEwMSwtNjIsLTQ1LC00MSw4MywtODksLTg2LC05LDM2LDEwNSwtMywtMTI2LC03Myw3NiwtOTAsOSw5NCwxMTYsLTMzLDEwLC0xMDEsLTExNSwyNl0sIm1hdGVyaWFsU2V0U2VyaWFsTnVtYmVyIjoxLCJpdlBhcmFtZXRlclNwZWMiOnsiaXYiOlsxMCwtNDYsMTE4LC04MCwtOTQsLTY2LC0xMDIsODQsNzgsMTExLC02NSwtOTEsLTQyLC03NSw1OSw3MV19fQ==",
    #     "eventLeftScope":False,
    #     "executionRoleArn":"arn:aws:iam::828605012785:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig",
    #     "configRuleArn":"arn:aws:config:us-east-1:828605012785:config-rule/config-rule-pcwdna",
    #     "configRuleName":"SG_CHECK",
    #     "configRuleId":"config-rule-pcwdna",
    #     "accountId":"828605012785",
    #     "evaluationMode":"DETECTIVE",
    #     "TestMode": True
    # }

    # compliance_status = lambda_handler(event, {})
    # assert compliance_status == "NON_COMPLIANT"