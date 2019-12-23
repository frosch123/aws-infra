from aws_cdk.core import (
    Construct,
    Stack,
    Tag,
)
from aws_cdk.aws_ecs import ICluster

from openttd.construct.ecs_https_container import ECSHTTPSContainer
from openttd.enumeration import Deployment
from openttd.stack.common import external


class BinariesProxyStack(Stack):
    application = "BinariesProxy"

    def __init__(self,
                 scope: Construct,
                 id: str,
                 *,
                 deployment: Deployment,
                 cluster: ICluster,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        Tag.add(self, "Application", self.application)
        Tag.add(self, "Deployment", deployment.value)

        external.add_stack(self)

        desired_count = 1
        if deployment == Deployment.PRODUCTION:
            desired_count = 2

        ECSHTTPSContainer(self, self.application,
            subdomain_name="binaries-proxy",
            application_name=f"{deployment.value}-{self.application}",
            image_name="openttd/binaries-proxy",
            port=80,
            memory_limit_mib=128,
            desired_count=desired_count,
            cluster=cluster,
            )