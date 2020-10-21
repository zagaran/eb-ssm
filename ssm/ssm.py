import argparse
import subprocess

from cement.utils.misc import minimal_logger
from ebcli.core import io
from ebcli.lib import aws, utils
from ebcli.operations.commonops import (get_current_branch_environment, get_default_profile,
                                        get_default_region, get_instance_ids)


LOG = minimal_logger(__name__)


class SSMWrapper:
    def __init__(self):
        args = self._parse_args()
        
        self.environment_name = args.environment_name or get_current_branch_environment()
        self.profile = args.profile or get_default_profile()
        self.region = args.region or get_default_region()
    
    def _parse_args(self):
        parser = argparse.ArgumentParser(description="SSH onto an Elastic Beanstalk Server")
        parser.add_argument(
            "environment_name",
            default=None,
            help="Elastic Beanstalk environment name (uses the branch default if not specified)",
            nargs="?",
        )
        parser.add_argument(
            "-p", "--profile",
            default=None,
            help="use a specific profile from your credential file",
        )
        parser.add_argument(
            "-r", "--region",
            default=None,
            help="use a specific region",
        )
        return parser.parse_args()
        
    def ssh(self):
        aws.set_region(self.region)
        aws.set_profile(self.profile)
        
        instances = get_instance_ids(self.environment_name)
        if len(instances) == 1:
            instance = instances[0]
        else:
            io.echo()
            io.echo('Select an instance to ssh into')
            instance = utils.prompt_for_item_in_list(instances)
        
        params = [
            "aws", "ssm", "start-session",
            "--document-name", "AWS-StartInteractiveCommand",
            "--parameters", "command='bash -l'"
            "--profile", self.profile,
            "--region", self.region,
            "--target", instance,
        ]
        subprocess.call(params)


def main():
    SSMWrapper().ssh()
