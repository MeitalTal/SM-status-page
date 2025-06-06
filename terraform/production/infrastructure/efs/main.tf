# EFS File System

provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "sharon-meital-terraform-state-bucket"
    key    = "efs/terraform.tfstate"
    region = "us-east-1"
  }
}


data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "sharon-meital-terraform-state-bucket"
    key    = "vpc/terraform.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "security_groups" {
  backend = "s3"
  config = {
    bucket = "sharon-meital-terraform-state-bucket"
    key    = "security_groups/terraform.tfstate"
    region = "us-east-1"
  }
}

# Get the current AWS caller identity
data "aws_caller_identity" "current" {}

# Get the IAM user details based on the caller identity
data "aws_iam_user" "current_user" {
  user_name = element(split("/", data.aws_caller_identity.current.arn), 1)
}

# Define the owner dynamically
locals {
  owner = data.aws_iam_user.current_user.user_name
}

resource "aws_efs_file_system" "efs" {
  creation_token = var.efs_name
  encrypted      = true
  tags = {
    Name = var.efs_name
    Owner = local.owner
  }
}

# EFS Mount Targets
resource "aws_efs_mount_target" "efs_mount" {
  count          = length(data.terraform_remote_state.vpc.outputs.private_subnets)
  file_system_id = aws_efs_file_system.efs.id
  subnet_id      = data.terraform_remote_state.vpc.outputs.private_subnets[count.index]
  security_groups = [data.terraform_remote_state.security_groups.outputs.admin_sg_id]
}
