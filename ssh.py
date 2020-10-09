import subprocess
import argparse

from cement.utils.misc import minimal_logger

from ebcli.lib import utils, aws
from ebcli.core import io
from ebcli.operations.commonops import get_default_region, get_default_profile, get_instance_ids


LOG = minimal_logger(__name__)


def prepare_for_ssh(environment_name):
    region = get_default_region()
    profile = get_default_profile()
    aws.set_region(region)
    aws.set_profile(profile)
    instances = get_instance_ids(environment_name)
    if len(instances) == 1:
        instance = instances[0]
    else:
        io.echo()
        io.echo('Select an instance to ssh into')
        instance = utils.prompt_for_item_in_list(instances)
    params = [
        "aws", "ssm", "start-session", "--region", region, "--target", instance,
        "--profile", profile, "--document-name", "AWS-StartInteractiveCommand",
        "--parameters", "command='bash -l'"
    ]
    subprocess.call(params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH onto an Elastic Beanstalk Server")
    parser.add_argument("environment_name", help="Elastic Beanstalk Environment name")
    args = parser.parse_args()
    args_dict = vars(args)
    prepare_for_ssh(**args_dict)
