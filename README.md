# EB SSM

This simple script helps you SSH into an Elastic Beanstalk server using AWS SSM.

While `eb ssh` exists, it requires each individual user to have the EC2 instance private keys locally. This is unideal
from both an information security and access management standpoint. If you've configured SSM, users will no longer need
the EC2 instance private keys to SSH into Elastic Beanstalk instances and instead have their access managed via IAM.

## Usage

Simply run `eb-ssm` from your repository and it will automatically hook into your local EB configuration.
