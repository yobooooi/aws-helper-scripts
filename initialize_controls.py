REMEDIATION_PARAMS_VALUE = '{"CentralLoggingTargetBucket": "central-logging-target-bucket","CentralAccount": "222222", "MaxCredentialUsageAge": "85"}'
FINDING_PARAMS_VALUE = '{"maxCredentialUsageAge": "35", "amiIds":["ami-006dcf34c09e50022"]}'


import logging
import json
import yaml


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_remediation_controls(path=None) -> {}:
    if path is None:
        path = "remediation_controls.yaml"
    rules_data = {}
    with open(path, "r") as stream:
        try:
            rules_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error(str(exc))

    return rules_data

def create_remediation_configuration(remdiation_control):

    string_of_control = json.dumps(remediation_control)
    print(string_of_control)
    substituted_control = string_of_control%json.loads(REMEDIATION_PARAMS_VALUE)

    print(substituted_control)
    replaced_json = json.loads(substituted_control)
    return replaced_json

if __name__ == '__main__':
    config_rules_names = get_remediation_controls()
    for remediation_control in config_rules_names["Remediations"]["ManagedRules"]:
        print(remediation_control)
        control = create_remediation_configuration(remediation_control)
        
        print(json.dumps(control, indent=4))