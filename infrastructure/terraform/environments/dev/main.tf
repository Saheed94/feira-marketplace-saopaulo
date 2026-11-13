module "network" {
  source = "../../modules/network"

  vpc_cidr              = "10.0.0.0/16"
  private_subnet_1_cidr = "10.0.1.0/24"
  private_subnet_2_cidr = "10.0.2.0/24"
  az_1                  = "us-east-1a"
  az_2                  = "us-east-1b"
}

output "vpc_id" {
  value = module.network.vpc_id
}

output "subnet_ids" {
  value = [module.network.subnet_1_id, module.network.subnet_2_id]
}

module "database" {
  source = "../../modules/database"

  # Pass the outputs from the network module into the database module
  subnet_ids = [module.network.subnet_1_id, module.network.subnet_2_id]
  sg_db_id   = module.network.sg_db_id
}

output "db_endpoint" {
  value = module.database.db_endpoint
}

module "compute" {
  source = "../../modules/compute"

  subnet_id  = module.network.subnet_1_id
  sg_task_id = module.network.sg_task_id
  vpc_id     = module.network.vpc_id
}