data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

# The Grafana admin password is generated here and stored encrypted in Parameter Store.
# The instance reads it at boot, so it never appears in the repository or in user data.
resource "random_password" "grafana" {
  length  = 24
  special = false
}

resource "aws_ssm_parameter" "grafana_password" {
  #checkov:skip=CKV_AWS_337:The AWS-managed key is enough for a lab. A customer-managed key would be the next step.
  name  = "/${var.name}/grafana-admin-password"
  type  = "SecureString"
  value = random_password.grafana.result
}

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "instance" {
  name               = "${var.name}-instance-role"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

# Session Manager replaces SSH, so port 22 is never opened.
resource "aws_iam_role_policy_attachment" "ssm_core" {
  role       = aws_iam_role.instance.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

data "aws_iam_policy_document" "read_password" {
  statement {
    actions   = ["ssm:GetParameter"]
    resources = [aws_ssm_parameter.grafana_password.arn]
  }
}

resource "aws_iam_role_policy" "read_password" {
  name   = "read-grafana-password"
  role   = aws_iam_role.instance.id
  policy = data.aws_iam_policy_document.read_password.json
}

resource "aws_iam_instance_profile" "instance" {
  name = "${var.name}-instance-profile"
  role = aws_iam_role.instance.name
}

resource "aws_instance" "app" {
  #checkov:skip=CKV_AWS_126:Detailed monitoring is a paid feature and is not needed for this lab.
  ami                         = data.aws_ami.al2023.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.app.id]
  iam_instance_profile        = aws_iam_instance_profile.instance.name
  associate_public_ip_address = false
  ebs_optimized               = true
  monitoring                  = false

  # IMDSv2 only, and one hop, so containers on the instance cannot reach the metadata service.
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  root_block_device {
    volume_type = "gp3"
    volume_size = 20
    encrypted   = true
  }

  user_data = templatefile("${path.module}/user_data.sh.tftpl", {
    compose_version = var.compose_version
    compose_sha256  = var.compose_sha256
    repo_url        = var.repo_url
    git_ref         = var.git_ref
    ssm_parameter   = aws_ssm_parameter.grafana_password.name
    region          = var.region
  })
  user_data_replace_on_change = true

  tags = {
    Name = "${var.name}-app"
  }
}

resource "aws_eip" "app" {
  domain   = "vpc"
  instance = aws_instance.app.id

  tags = {
    Name = "${var.name}-eip"
  }

  depends_on = [aws_internet_gateway.main]
}
