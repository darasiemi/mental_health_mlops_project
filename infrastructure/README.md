First create a state bucket in S3 manually with name `tf-state-mlops-zoomcamp-dara`.

To check if configuration file is valid
```bash
terraform validate
```
To initialize terraform
```bash
terraform init
```
To format terraform files, run
```bash
terraform fmt
```
To send state file to S3 bucket
```bash
terraform apply
```

To initialize terraform with certain AWS user profile
```bash
terraform init --profile profile
```

To configure terraform with variable file
```bash
terraform plan -var-file=vars/stg.tfvars
```
Similarly, to create the files in AWS
```bash
terraform apply -var-file=vars/stg.tfvars
```

To destroy resources
```bash
terraform destroy -var-file=vars/stg.tfvars
```
