data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "my_ec2" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.private_subnet_1.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_ssm_profile.name
  associate_public_ip_address = false

  user_data = base64encode(<<-EOF
              #!/bin/bash
              yum update -y
              sudo tee /etc/yum.repos.d/mongodb-org-8.0.repo <<EOT
              [mongodb-org-8.0]
              name=MongoDB Repository
              baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/8.0/x86_64/
              gpgcheck=1
              enabled=1
              gpgkey=https://pgp.mongodb.com/server-8.0.asc
              EOT
              sudo yum install -y mongodb-org
              sudo sed -i "s/port: 27017/port: ${var.mongodb_port}/" /etc/mongod.conf
              sudo sed -i "s/bindIp: 127.0.0.1/bindIp: 0.0.0.0/" /etc/mongod.conf
              sudo systemctl daemon-reload
              sudo systemctl start mongod
              sudo systemctl enable mongod
              EOF
  )

  tags = {
    Name = "my-ec2"
  }
}
