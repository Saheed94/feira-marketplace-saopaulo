# 1. The VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "feira-vpc"
  }
}

# 2. The Subnets
resource "aws_subnet" "private_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.private_subnet_1_cidr
  availability_zone       = var.az_1
  map_public_ip_on_launch = false

  tags = {
    Name = "feira-private-subnet-1"
  }
}

resource "aws_subnet" "private_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.private_subnet_2_cidr
  availability_zone       = var.az_2
  map_public_ip_on_launch = false

  tags = {
    Name = "feira-private-subnet-2"
  }
}

# 3. The Route Table
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "feira-private-rt"
  }
}

# 4. Route Table Associations
resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.private.id
}

# 1. Inbound 443 from itself (For SSM VPC Endpoints)
resource "aws_vpc_security_group_ingress_rule" "task_https_self" {
  security_group_id            = aws_security_group.sg_task.id
  referenced_security_group_id = aws_security_group.sg_task.id
  from_port                    = 443
  ip_protocol                  = "tcp"
  to_port                      = 443
}

# 2. Outbound 443 to itself (To reach SSM VPC Endpoints)
resource "aws_vpc_security_group_egress_rule" "task_https_self" {
  security_group_id            = aws_security_group.sg_task.id
  referenced_security_group_id = aws_security_group.sg_task.id
  from_port                    = 443
  ip_protocol                  = "tcp"
  to_port                      = 443
}

# 3. Outbound 5432 to the DB (To talk to RDS)
resource "aws_vpc_security_group_egress_rule" "task_db" {
  security_group_id            = aws_security_group.sg_task.id
  referenced_security_group_id = aws_security_group.sg_db.id
  from_port                    = 5432
  ip_protocol                  = "tcp"
  to_port                      = 5432
}

# 4. Outbound DNS (UDP 53) to the VPC CIDR
resource "aws_vpc_security_group_egress_rule" "task_dns" {
  security_group_id = aws_security_group.sg_task.id
  cidr_ipv4         = aws_vpc.main.cidr_block
  from_port         = 53
  ip_protocol       = "udp"
  to_port           = 53
}

# 5. Inbound 5432 from SG-task only
resource "aws_vpc_security_group_ingress_rule" "db_from_task" {
  security_group_id            = aws_security_group.sg_db.id
  referenced_security_group_id = aws_security_group.sg_task.id
  from_port                    = 5432
  ip_protocol                  = "tcp"
  to_port                      = 5432
}