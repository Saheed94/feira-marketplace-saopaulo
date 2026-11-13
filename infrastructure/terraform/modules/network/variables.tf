variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnet_1_cidr" {
  description = "The CIDR block for the first private subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_2_cidr" {
  description = "The CIDR block for the second private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "az_1" {
  description = "The first Availability Zone"
  type        = string
  default     = "us-east-1a"
}

variable "az_2" {
  description = "The second Availability Zone"
  type        = string
  default     = "us-east-1b"
}