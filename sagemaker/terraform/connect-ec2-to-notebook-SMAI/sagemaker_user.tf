resource "aws_sagemaker_user_profile" "ai_user" {
  domain_id         = aws_sagemaker_domain.my_domain.id
  user_profile_name = "ai-user"
  user_settings {
    execution_role = aws_iam_role.sagemaker_role.arn
    security_groups = [aws_security_group.sagemaker_sg.id]
  }
}
