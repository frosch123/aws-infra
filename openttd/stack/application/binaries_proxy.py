from aws_cdk.core import (
    Construct,
    Stack,
    Tags,
)
from aws_cdk.aws_ecs import ICluster

from openttd.construct.ecs_https_container import ECSHTTPSContainer
from openttd.construct.policy import Policy
from openttd.enumeration import Deployment


class BinariesProxyStack(Stack):
    application_name = "BinariesProxy"
    subdomain_name = "proxy.binaries"

    def __init__(self,
                 scope: Construct,
                 id: str,
                 *,
                 deployment: Deployment,
                 policy: Policy,
                 cluster: ICluster,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        Tags.of(self).add("Application", self.application_name)
        Tags.of(self).add("Deployment", deployment.value)

        policy.add_stack(self)

        if deployment == Deployment.PRODUCTION:
            desired_count = 2
            priority = 20
        else:
            desired_count = 1
            priority = 120

        ECSHTTPSContainer(self, self.application_name,
            subdomain_name=self.subdomain_name,
            deployment=deployment,
            policy=policy,
            application_name=self.application_name,
            image_name="openttd/binaries-proxy",
            port=80,
            memory_limit_mib=16,
            desired_count=desired_count,
            cluster=cluster,
            priority=priority,
            )
