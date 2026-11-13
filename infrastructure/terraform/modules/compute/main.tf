# --- IAM ROLE FOR SSM ---
resource "aws_iam_role" "ssm_role" {
  name = "feira-ec2-ssm-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_policy" {
  role       = aws_iam_role.ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ssm_profile" {
  name = "feira-ec2-ssm-profile"
  role = aws_iam_role.ssm_role.name
}

# --- VPC ENDPOINTS FOR SSM ---
resource "aws_vpc_endpoint" "ssm" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.us-east-1.ssm"
  vpc_endpoint_type = "Interface"
  subnet_ids        = [var.subnet_id]
  security_group_ids = [var.sg_task_id]
  private_dns_enabled = true
  
  tags = { Name = "feira-ssm-endpoint" }
}

resource "aws_vpc_endpoint" "ssmmessages" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.us-east-1.ssmmessages"
  vpc_endpoint_type = "Interface"
  subnet_ids        = [var.subnet_id]
  security_group_ids = [var.sg_task_id]
  private_dns_enabled = true
  
  tags = { Name = "feira-ssmmessages-endpoint" }
}

resource "aws_vpc_endpoint" "ec2messages" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.us-east-1.ec2messages"
  vpc_endpoint_type = "Interface"
  subnet_ids        = [var.subnet_id]
  security_group_ids = [var.sg_task_id]
  private_dns_enabled = true
  
  tags = { Name = "feira-ec2messages-endpoint" }
}

# --- THE EC2 INSTANCE ---
# We use a data source to get the latest Amazon Linux 2023 AMI automatically
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

resource "aws_instance" "test_client" {
  ami           = data.aws_ami.amazon_linux_2023.id
  instance_type = "t3.micro"
  subnet_id     = var.subnet_id
  
  vpc_security_group_ids = [var.sg_task_id]
  iam_instance_profile   = aws_iam_instance_profile.ssm_profile.name

  tags = {
    Name = "feira-test-client"
  }
}