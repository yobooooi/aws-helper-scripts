import os
import json

# generator_id = "aws-foundational-security-best-practices/v/1.0.0/EC2.6"

# environment = {"REGION": "us-east-1", "EXEMPTION_DYNAMODB_TABLE_NAME": "table_name"}
# supported_generator_control_map = {
#     "aws-foundational-security-best-practices": "ControlId",
#     "cis-aws-foundations-benchmark": "RuleId",
# }


environment_vars={"REGION": "us-east-1", "EXEMPTION_DYNAMODB_TABLE_NAME": "table_name"}

placeholder_dictionary = [
    {
        "abv": "sechubbestprac",
        "generator": "aws-foundational-security-best-practices",
        "global_policy_id": "ControlId"
    },
    {
        "abv": "cisfoundation",
        "generator": "cis-aws-foundations-benchmark",
        "global_policy_id": "RuleId"
    }
]
for supported_generator in placeholder_dictionary:
    abbreviation, generator, global_policy_id = supported_generator.values()
    print(abbreviation, generator, global_policy_id)
    print(f"{abbreviation}_generator")
    # environment_vars[f"{abbreviation}_generator"] = generator
    # environment_vars[f"{abbreviation}_global_policy_id"] = global_policy_id

# for generator, control_id in supported_generator_control_map.items():
#     #print(generator, control_id)
#     environment[generator] = control_id

print(environment_vars)
# for i in supported_generator_control_map.items():
#     print(i[0])
# environment.update(supported_generator_control_map)

# for key, value in environment.items():
#     os.environ[key] = value

# os.environ
# print([ value for key, value in os.environ.items() if key.lower() in generator_id ][0])

# prefix_list = []
# for key, value in supported_generator_control_map.items():
#     prefix_list.append({
#         "prefix" : key
#     })

# print(prefix_list)