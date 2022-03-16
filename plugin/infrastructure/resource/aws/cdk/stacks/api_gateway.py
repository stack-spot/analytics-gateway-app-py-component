from .helpers.file import get_policy, get_api, get_role
from plugin.utils.file import interpolate_json_template
from aws_cdk import core as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_apigateway as apigateway
from aws_cdk.aws_ec2 import CfnSecurityGroup, CfnVPCEndpoint


class ApiGateway(cdk.Stack):
    """
    TO DO
    Args:
        cdk ([type]): [description]
    """

    def create_security_group(self, name: str, eg_blocks_sg: list, ip_blocks_sg: list, vpc_id: str):

        security_group_name = f'SecurityGroup{name}'

        security_group = CfnSecurityGroup(
            self,
            security_group_name,
            group_description="Allow inbound traffic",
            group_name=name,
            security_group_egress=[
                CfnSecurityGroup.EgressProperty(
                    ip_protocol="-1",
                    cidr_ip=cidr_ip,
                    from_port=0,
                    to_port=0
                ) for cidr_ip in eg_blocks_sg
            ],
            security_group_ingress=[
                CfnSecurityGroup.IngressProperty(
                    ip_protocol="all",
                    cidr_ip=cidr_ip,
                    description=f'Allow all traffic from cidr block {cidr_ip}',
                    from_port=0,
                    to_port=65535
                ) for cidr_ip in ip_blocks_sg
            ],
            tags=[
                cdk.CfnTag(
                    key="Name",
                    value=security_group_name
                )
            ],
            vpc_id=vpc_id
        )

        return security_group

    def create_api_gateway(self, account_id: str, name: str, vpc_id: str, vpce: CfnVPCEndpoint, region: str, type_: str):

        policy_kinesis_proxy_event = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "kinesis:PutRecords"
                    ],
                    "Resource": f"arn:aws:kinesis:{region}:{account_id}:stream/{name}-*"
                }
            ]
        }

        role_api_gateway = iam.CfnRole(
            self,
            f"{name}-api-gateway-role",
            role_name=f"{name}-api-gateway",
            assume_role_policy_document=get_role("OsDataRoleApi"),
            policies=[
                iam.CfnRole.PolicyProperty(
                    policy_document=policy_kinesis_proxy_event,
                    policy_name=f"{name}-api-kinesis-proxy-event-policy"
                )
            ]
        )
        kinesis_uri_invocation_arn = f"arn:aws:apigateway:{region}:kinesis:action/PutRecords"
        rest_api_policy = iam.PolicyDocument()
        cfn_rest_api = apigateway.CfnRestApi(
            self,
            f'ApiGatewayRestApi{name}',
            body=interpolate_json_template(
                get_api("OpenApiV2.0"),
                {
                    "name": name,
                    "aws_account_id": cdk.Stack.of(self).account,
                    "api_gateway_role": f'arn:aws:iam::{cdk.Stack.of(self).account}:role/{name}-api-gateway',
                    "kinesis_uri_invocation_arn": kinesis_uri_invocation_arn,
                    "api_gateway_policy": f'arn:aws:execute-api:{region}:{cdk.Stack.of(self).account}:*',
                    "aws_region": region,
                    "aws_vpce": cdk.Fn.ref(vpce.logical_id),
                    "aws_vpc": vpc_id
                }
            ),
            description="REST API to publish events to Data Lake",
            endpoint_configuration=apigateway.CfnRestApi.EndpointConfigurationProperty(
                vpc_endpoint_ids=[
                    cdk.Fn.ref(vpce.logical_id)
                ],
                types=[type_]
            ),
            name=name,
            policy=rest_api_policy,
            tags=[
                cdk.CfnTag(
                    key="Name",
                    value=name
                )
            ]
        )
        rest_api_policy.add_statements(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["execute-api:Invoke"],
                resources=[cdk.Fn.join('', ['execute-api:/', '*'])]
            )
        )
        rest_api_policy.add_statements(
            iam.PolicyStatement(
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["execute-api:Invoke"],
                conditions={
                    "StringNotEquals": {
                        "aws:sourceVpc": vpc_id,
                        "aws:sourceVpce": cdk.Fn.ref(vpce.logical_id)
                    }
                },
                resources=[cdk.Fn.join('', ['execute-api:/', '*'])]
            )
        )
        cfn_rest_api.add_depends_on(role_api_gateway)
        policy_send_event = interpolate_json_template(
            get_policy("OsDataPolicyApiSendEvent"),
            {
                "AwsAccount": self.account,
                "AwsRegion": region,
                "GatewayApiId": cdk.Fn.ref(cfn_rest_api.logical_id)
            }
        )
        iam.CfnRole(
            self,
            f"{name}-api-send-event",
            role_name=f"{name}-api-send-event",
            assume_role_policy_document=get_role("OsDataRoleApi"),
            policies=[
                iam.CfnRole.PolicyProperty(
                    policy_document=policy_send_event,
                    policy_name=f"{name}-api-send-event-policy"
                )
            ]
        )
        cfn_api_key = apigateway.CfnApiKey(
            self,
            f'ApiGatewayApiKy{name}',
            description=f'Api Key - {name}',
            enabled=True,
            name=f'{name}-key',
            tags=[cdk.CfnTag(
                key="Name",
                value=name
            )]
        )
        cfn_deployment = apigateway.CfnDeployment(
            self,
            f'ApiGatewayDeployment{name}',
            rest_api_id=cdk.Fn.ref(cfn_rest_api.logical_id),
            stage_description=apigateway.CfnDeployment.StageDescriptionProperty(
                description="Deployed at",
                method_settings=[
                    apigateway.CfnDeployment.MethodSettingProperty(
                        logging_level="OFF",
                        metrics_enabled=False,
                        http_method="*",
                        resource_path="/*"
                    )
                ]
            ),
            stage_name=f'prd_{name}_stage'
        )
        cfn_usage_plan = apigateway.CfnUsagePlan(
            self,
            f'ApiGatewayUsagePlan{name}',
            api_stages=[
                apigateway.CfnUsagePlan.ApiStageProperty(
                    api_id=cdk.Fn.ref(cfn_rest_api.logical_id),
                    stage=f'prd_{name}_stage'
                )
            ],
            description="description",
            quota=apigateway.CfnUsagePlan.QuotaSettingsProperty(
                        limit=100000,
                        period="DAY"
            ),
            tags=[cdk.CfnTag(
                key="Name",
                value=name
            )],
            throttle=apigateway.CfnUsagePlan.ThrottleSettingsProperty(
                burst_limit=500,
                rate_limit=25
            ),
            usage_plan_name=f'prd_{name}_usage_plan'
        )
        cfn_usage_plan_key = apigateway.CfnUsagePlanKey(
            self,
            f'ApiGatewayUsagePlanKey{name}',
            key_id=cfn_api_key.get_att('APIKeyId').to_string(),
            key_type="API_KEY",
            usage_plan_id=cfn_usage_plan.get_att('Id').to_string()
        )

        cfn_rest_api.add_depends_on(vpce)
        cfn_api_key.add_depends_on(cfn_rest_api)
        cfn_deployment.add_depends_on(cfn_api_key)
        cfn_usage_plan.add_depends_on(cfn_deployment)
        cfn_usage_plan_key.add_depends_on(cfn_deployment)
        return cfn_rest_api

    def create_vpc_endpoint(self, name: str, region: str, subnet_ids: list, security_group_id: str, vpc_id: str):
        vpc_endpoint_name = f'VPCEndpoint{name}'
        vpc_endpoint = CfnVPCEndpoint(
            self,
            vpc_endpoint_name,
            service_name=f'com.amazonaws.{region}.execute-api',
            vpc_id=vpc_id,
            security_group_ids=[security_group_id],
            subnet_ids=subnet_ids,
            vpc_endpoint_type="Interface"
        )
        return vpc_endpoint

    @staticmethod
    def __select_dns_entry(index: int, vpc_endpoint: CfnVPCEndpoint):

        entry = cdk.Fn.select(
            index,
            cdk.Fn.split(
                ":",
                cdk.Fn.select(
                    0,
                    cdk.Token.as_list(
                        cdk.Fn.get_att(
                            logical_name_of_resource=vpc_endpoint.logical_id,
                            attribute_name="DnsEntries"
                        )
                    )
                )
            )
        )

        return entry

    def create_route53_a_record(self, name: str, zone_id: str, zone_name: str, vpc_endpoint: CfnVPCEndpoint):

        vpc_endpoint_dns_name = self.__select_dns_entry(
            index=1,
            vpc_endpoint=vpc_endpoint
        )

        vpc_endpoint_hosted_zone_id = self.__select_dns_entry(
            index=0,
            vpc_endpoint=vpc_endpoint
        )

        record = route53.CfnRecordSet(
            self,
            id=f"dp-route53-{name}",
            hosted_zone_id=zone_id,
            name=f"analytics-{name}.{zone_name}",
            type="A",
            alias_target=route53.CfnRecordSet.AliasTargetProperty(
                dns_name=vpc_endpoint_dns_name,
                hosted_zone_id=vpc_endpoint_hosted_zone_id,
                evaluate_target_health=True
            )
        )

        return record
