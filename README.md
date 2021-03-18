# EB SSM

This simple script helps you SSH into an Elastic Beanstalk server using AWS SSM.

eb-ssm is desinged to combine tools from the EB CLI and the AWS CLI to provide a better alternaitve to `eb ssh`.

It's a pip library, installed by `pip install eb-ssm`.

Once it's set up, you can SSH into your Elastic Beanstalk servers with `eb-ssm [ENVIRONMENT_NAME]`.


## Why you should use it

While `eb ssh` exists, it requires each individual user to have the EC2 instance private keys locally. This is unideal
from both an information security and access management standpoint. If you've configured SSM, users will no longer need
SSH keys to SSH into Elastic Beanstalk instances and instead have their access managed via IAM.

The main advantages of eb-ssm are the following:

1. **Server SSH access is managed through IAM.**  Normally, you have to manage SSH access to Elastic Beanstalk environments yourself.  IAM is where AWS manages user access for everything else, and with eb-ssm, you can manage server SSH access for EB environments there as well.

2. **No shared SSH keys.**  Sharing, tracking, and rotating SSH keys is a pain.  Using eb-ssm, you there are no SSH keys, so these problems go away.

3. **No mucking around with port 22.**  The EB CLI is supposed to open port 22 just for the SSH session but it doesn't close it in the event of non-graceful termination of the SSH session.  eb-ssm does one better by never opening port 22 in the first place.

4. **Audit log of SSH sessions.**  AWS SSM keeps a log of SSH sessions.  This is one more benefit that comes from using it over native SSH.

5. **Ability to access non-public servers.**  If you have servers in a privative subnet, you can use eb-ssm to SSH into them without needing a bastion host.


## Prerequisites

### Set up your Elastic Beanstalk Environment to allow SSH via AWS SSM

The following steps need to be done once per environment.

1. Go to Elastic Beanstalk > ENVIRONEMNT_NAME > Configuration > Security and find the "IAM instance profile" (by default, this is "aws-elasticbeanstalk-ec2-role").  This is ROLE_NAME in step 2.

2. Go to IAM > Roles > ROLE_NAME.  Under permissions, add "AmazonSSMManagedInstanceCore".

3. Go to Systems Manager > Session Manager > Preferences > Edit.  Enable "Run As Support" and set the "Run As Defualt User" to be "ec2-user" (or whatever the default user for your Elastic Beanstalk servers is).

Note that it may take some time (~10 minutes) for the IAM changes to propagate.  If you have completed the AWS setup and get a "TargetNotConnected" error, wait 10-15 minutes and try again.

### Configure your local computer

The following steps need to be done once per computer.

1. Install the AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

2. Install the Session Manager Plugin: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html

## Using EB SSM

Install eb-ssm via `pip install eb-ssm`.

Once it is installed, all you need to do is run `eb-ssm` from your repository and it will automatically hook into your repository's EB configuration (in .elasticbeanstalk/config.yml).

To ssh into a specific environment, use `eb-ssm ENVIRONMENT_NAME`.

You can also optionally pass other parameters, such as an AWS CLI profile or a region to eb-ssm.  See `eb-ssm --help` for a full list of options.

## Config

eb-ssm uses the EB CLI configuration files.  If you have not used the EB CLI to set up a project, here is the minimal configruation needed by eb-ssm; this configraution lives in `.elasticbeanstalk/config.yml`:

```
global:
  application_name: EB_APPLICATION_NAME
  default_region: REGION_NAME
  profile: PROFILE_NAME
```
