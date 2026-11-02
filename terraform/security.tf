resource "aws_security_group" "app" {
  name        = "${var.name}-sg"
  description = "Grafana from one IP address, outbound HTTPS only"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.name}-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "grafana" {
  security_group_id = aws_security_group.app.id
  description       = "Grafana UI from the allowed IP only"
  cidr_ipv4         = var.allowed_cidr
  from_port         = 3000
  to_port           = 3000
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "https" {
  security_group_id = aws_security_group.app.id
  description       = "HTTPS for packages, container images, GitHub and Systems Manager"
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
}
