variable "subnet_ids" {
  description = "A list of subnet IDs for the DB subnet group"
  type        = list(string)
}

variable "sg_db_id" {
  description = "The ID of the security group for the database"
  type        = string
}