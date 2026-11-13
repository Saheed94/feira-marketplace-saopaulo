# 1. The DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "feira-db-subnet-group"
  subnet_ids = var.subnet_ids # This will be a list of the two subnets from the network module

  tags = {
    Name = "feira-db-subnet-group"
  }
}

# 2. The RDS Instance
resource "aws_db_instance" "main" {
  identifier             = "feira-db"
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  storage_type           = "gp3"
  
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.sg_db_id]
  
  # Security & Access
  publicly_accessible    = false
  manage_master_user_password = true # AWS handles the secret in Secrets Manager
  
  # Database specifics
  db_name                = "feira"
  username               = "postgres"
  
  # Drill settings (Change these in production)
  skip_final_snapshot    = true
  deletion_protection    = false

  tags = {
    Name = "feira-db"
  }
}