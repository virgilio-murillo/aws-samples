resource "aws_sagemaker_domain" "my_domain" {
  domain_name = "my-domain"
  auth_mode   = "IAM"
  vpc_id      = aws_vpc.my_vpc.id
  subnet_ids  = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]

  default_user_settings {
    execution_role  = aws_iam_role.sagemaker_role.arn
    security_groups = [aws_security_group.sagemaker_sg.id]
  }
  default_space_settings {
    execution_role  = aws_iam_role.sagemaker_role.arn
    security_groups = [aws_security_group.sagemaker_sg.id]
  }
  app_network_access_type = "VpcOnly"
}
