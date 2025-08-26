output "vpc_id" {
  value = aws_vpc.my_vpc.id
}

output "sagemaker_domain_id" {
  value = aws_sagemaker_domain.my_domain.id
}

output "ec2_private_ip" {
  value = aws_instance.my_ec2.private_ip
}

output "mongodb_port" {
  value = var.mongodb_port
}

output "user_profile_name" {
  value = aws_sagemaker_user_profile.ai_user.user_profile_name
}

output "private_space_name" {
  value = aws_sagemaker_space.private_space.space_name
}

output "shared_space_name" {
  value = aws_sagemaker_space.shared_space.space_name
}
