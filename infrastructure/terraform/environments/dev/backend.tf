terraform {
  backend "s3" {
    bucket       = "feira-tf-state-471112990922-us-east-1-an"
    key          = "feira/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}