output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "subnet_1_id" {
  description = "The ID of the first private subnet"
  value       = aws_subnet.private_1.id
}

output "subnet_2_id" {
  description = "The ID of the second private subnet"
  value       = aws_subnet.private_2.id
}

output "sg_db_id" {
  description = "The ID of the DB security group"
  value       = aws_security_group.sg_db.id
}

output "sg_task_id" {
  description = "The ID of the task security group"
  value       = aws_security_group.sg_task.id
}