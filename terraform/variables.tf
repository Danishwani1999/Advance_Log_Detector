variable "region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "ap-south-1"
}

variable "name" {
  description = "Name prefix for every resource."
  type        = string
  default     = "log-detector"
}

variable "instance_type" {
  description = "EC2 instance type. The stack runs five containers, so 2 GiB of memory is comfortable."
  type        = string
  default     = "t3.small"
}

variable "allowed_cidr" {
  description = "Your public IP as a /32 CIDR, for example 203.0.113.10/32. Only this range can reach Grafana."
  type        = string

  validation {
    condition     = can(cidrhost(var.allowed_cidr, 0)) && var.allowed_cidr != "0.0.0.0/0"
    error_message = "allowed_cidr must be a valid CIDR block and must not be 0.0.0.0/0."
  }
}

variable "repo_url" {
  description = "Git repository the instance clones and runs with Docker Compose."
  type        = string
  default     = "https://github.com/Danishwani1999/Advance_Log_Detector.git"
}

variable "git_ref" {
  description = "Branch or tag to deploy."
  type        = string
  default     = "main"
}

variable "compose_version" {
  description = "Docker Compose release installed on the instance."
  type        = string
  default     = "v2.40.3"
}

variable "compose_sha256" {
  description = "SHA-256 of docker-compose-linux-x86_64 for compose_version. The install fails if it does not match."
  type        = string
  default     = "dba9d98e1ba5bfe11d88c99b9bd32fc4a0624a30fafe68eea34d61a3e42fd372"
}

variable "vpc_cidr" {
  description = "CIDR block of the VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block of the public subnet."
  type        = string
  default     = "10.20.1.0/24"
}
