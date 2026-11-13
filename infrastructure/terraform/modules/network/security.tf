resource "aws_security_group" "sg_task" {
  name        = "feira-sg-task"
  description = "Security group for ECS/EC2 tasks"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "feira-sg-task"
  }
}

resource "aws_security_group" "sg_db" {
  name        = "feira-sg-db"
  description = "Security group for RDS database"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "feira-sg-db"
  }
}

