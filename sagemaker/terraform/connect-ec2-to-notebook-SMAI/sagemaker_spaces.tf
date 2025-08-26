# Private Space
resource "aws_sagemaker_space" "private_space" {
  domain_id  = aws_sagemaker_domain.my_domain.id
  space_name = "private-notebook"

  ownership_settings {
    owner_user_profile_name = aws_sagemaker_user_profile.ai_user.user_profile_name
  }

  space_settings {
    app_type = "JupyterLab"

    jupyter_lab_app_settings {
      default_resource_spec {
        instance_type = "ml.t3.medium"
      }
    }
  }

  space_sharing_settings {
    sharing_type = "Private"
  }
}

# Shared Space
resource "aws_sagemaker_space" "shared_space" {
  domain_id  = aws_sagemaker_domain.my_domain.id
  space_name = "shared-notebook"

  ownership_settings {
    owner_user_profile_name = aws_sagemaker_user_profile.ai_user.user_profile_name
  }

  space_settings {
    app_type = "JupyterLab"

    jupyter_lab_app_settings {
      default_resource_spec {
        instance_type = "ml.t3.medium"
      }
    }
  }

  space_sharing_settings {
    sharing_type = "Shared"
  }
}
