variable "subnet_id" {
  description = "Subnet ID for the EC2 instance"
  type        = string
}

variable "sg_task_id" {
  description = "Security group ID for the task"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for the endpoints"
  type        = string
}