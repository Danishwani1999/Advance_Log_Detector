output "instance_id" {
  description = "ID of the EC2 instance."
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "Elastic IP of the instance."
  value       = aws_eip.app.public_ip
}

output "grafana_url" {
  description = "Grafana UI. Reachable only from allowed_cidr. The page can take a few minutes after apply while the stack builds."
  value       = "http://${aws_eip.app.public_ip}:3000"
}

output "session_manager_command" {
  description = "Open a shell on the instance without SSH."
  value       = "aws ssm start-session --target ${aws_instance.app.id} --region ${var.region}"
}

output "grafana_password_command" {
  description = "Read the generated Grafana admin password."
  value       = "aws ssm get-parameter --name ${aws_ssm_parameter.grafana_password.name} --with-decryption --query Parameter.Value --output text --region ${var.region}"
}
